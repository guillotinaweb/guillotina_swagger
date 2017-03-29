from guillotina import configure


configure.permission('guillotina_swagger.View', 'View swagger definition')
configure.grant(
    permission="guillotina_swagger.View",
    role="guillotina.Anonymous")
configure.grant(
    permission="guillotina_swagger.View",
    role="guillotina.Authenticated")


app_settings = {
    "static": [{
        "swagger_static": 'guillotina_swagger:static'
    }]
}


def includeme(root):
    configure.scan("guillotina_swagger.services")
    configure.scan("guillotina_swagger.content")
