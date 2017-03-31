from guillotina import app_settings
from guillotina import configure
from guillotina.api.service import Service
from guillotina.interfaces import IApplication
from guillotina.interfaces import IInteraction
from guillotina.utils import get_content_path
from guillotina.utils import resolve_dotted_name
from guillotina_swagger.utils import get_scheme
from zope.interface import Interface

import copy
import os
import pkg_resources


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

    def get_endpoints(self, iface_conf, path, api_def, tags=[]):
        for method in iface_conf.keys():
            if method == 'endpoints':
                for name in iface_conf['endpoints']:
                    self.get_endpoints(
                        iface_conf['endpoints'][name],
                        os.path.join(path, name),
                        api_def,
                        tags=[name.strip('@')])
            else:
                if method.lower() == 'options':
                    continue

                if path not in api_def:
                    api_def[path] = {}

                service_def = iface_conf[method]
                if service_def.get('ignore'):
                    continue

                if not self.interaction.check_permission(
                        service_def['permission'], self.context):
                    continue

                api_def[path][method.lower()] = {
                    "tags": tags or [''],
                    "parameters": self.get_data(service_def.get('parameters', {})),
                    "produces": self.get_data(service_def.get('produces', [])),
                    "summary": self.get_data(service_def.get('summary', '')),
                    "description": self.get_data(service_def.get('description', '')),
                    "responses": self.get_data(service_def.get('responses', {})),
                }

    async def __call__(self):
        self.interaction = IInteraction(self.request)
        definition = copy.deepcopy(app_settings['swagger']['base'])
        definition['host'] = self.request.host
        definition['schemes'] = [get_scheme(self.request)]
        definition["info"]["version"] = pkg_resources.get_distribution("guillotina").version

        api_defs = app_settings['api_definition']

        if IApplication.providedBy(self.context):
            path = '/'
        else:
            path = '/{}'.format(self.request._db_id)
            content_path = get_content_path(self.context)
            if content_path not in (None, '/', ''):
                path += content_path

        for dotted_iface in api_defs.keys():
            iface = resolve_dotted_name(dotted_iface)
            if iface.providedBy(self.context):
                iface_conf = api_defs[dotted_iface]
                self.get_endpoints(iface_conf, path, definition['paths'])

        definition["definitions"] = app_settings['json_schema_definitions']
        return definition
