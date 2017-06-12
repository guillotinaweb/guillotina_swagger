from guillotina import app_settings
from guillotina import configure
from guillotina.api.service import Service
from guillotina.component import getMultiAdapter
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IInteraction
from guillotina.utils import resolve_dotted_name
from guillotina_swagger.utils import get_full_content_path
from guillotina_swagger.utils import get_scheme
from jinja2 import Template
from zope.interface import Interface
from zope.interface.interfaces import ComponentLookupError

import copy
import os
import pkg_resources


here = os.path.dirname(os.path.realpath(__file__))


@configure.service(
    method='GET', context=Interface, name="@swagger",
    permission="guillotina_swagger.View",
    ignore=True)
class SwaggerDefinitionService(Service):
    __allow_access__ = True

    def get_data(self, data):
        if callable(data):
            data = data(self.context)
        return data

    def load_swagger_info(self, api_def, path, method, tags, service_def):
        path = path.rstrip('/')
        if path not in api_def:
            api_def[path or '/'] = {}
        api_def[path or '/'][method.lower()] = {
            "tags": tags or [''],
            "parameters": self.get_data(service_def.get('parameters', {})),
            "produces": self.get_data(service_def.get('produces', [])),
            "summary": self.get_data(service_def.get('summary', '')),
            "description": self.get_data(service_def.get('description', '')),
            "responses": self.get_data(service_def.get('responses', {})),
        }

    def get_endpoints(self, iface_conf, base_path, api_def, tags=[]):
        for method in iface_conf.keys():
            if method == 'endpoints':
                for name in iface_conf['endpoints']:
                    self.get_endpoints(
                        iface_conf['endpoints'][name],
                        os.path.join(base_path, name),
                        api_def,
                        tags=[name.strip('@')])
            else:
                if method.lower() == 'options':
                    continue

                service_def = iface_conf[method]
                if service_def.get('ignore'):
                    continue

                if not self.interaction.check_permission(
                        service_def['permission'], self.context):
                    continue

                for sub_path in [''] + service_def.get('extra_paths', []):
                    path = os.path.join(base_path, sub_path)
                    if 'traversed_service_definitions' in service_def:
                        trav_defs = service_def['traversed_service_definitions']
                        if isinstance(trav_defs, dict):
                            for sub_path, sub_service_def in trav_defs.items():
                                self.load_swagger_info(
                                    api_def,
                                    os.path.join(path, sub_path),
                                    method, tags, sub_service_def)
                    else:
                        self.load_swagger_info(api_def, path, method, tags, service_def)

    async def __call__(self):
        self.interaction = IInteraction(self.request)
        definition = copy.deepcopy(app_settings['swagger']['base_configuration'])
        definition['host'] = self.request.host
        definition['schemes'] = [get_scheme(self.request)]
        definition["info"]["version"] = pkg_resources.get_distribution("guillotina").version

        api_defs = app_settings['api_definition']

        path = get_full_content_path(self.request, self.context)

        for dotted_iface in api_defs.keys():
            iface = resolve_dotted_name(dotted_iface)
            if iface.providedBy(self.context):
                iface_conf = api_defs[dotted_iface]
                self.get_endpoints(iface_conf, path, definition['paths'])

        definition["definitions"] = app_settings['json_schema_definitions']
        return definition


@configure.service(
    method='GET', context=Interface, name="@docs",
    permission="guillotina_swagger.View",
    ignore=True)
async def render_docs_index(context, request):
    fi = open(os.path.join(here, 'index.html'))
    html = fi.read()
    fi.close()
    template = Template(html)
    swagger_settings = app_settings['swagger']
    url = swagger_settings['base_url']
    if url is None:
        try:
            url = getMultiAdapter((context, request), IAbsoluteURL)()
        except ComponentLookupError:
            url = '{}://{}'.format(
                get_scheme(request),
                request.host
            )
    swagger_settings['initial_swagger_url'] = url
    return template.render(
        app_settings=app_settings,
        request=request,
        swagger_settings=swagger_settings,
        base_url=url,
        static_url='{}/swagger_static/'.format(url if url != '/' else '')
    )
