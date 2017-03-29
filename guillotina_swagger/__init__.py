from guillotina import configure


configure.permission('guillotina_swagger.View', 'View swagger definition')
configure.grant(
    permission="guillotina_swagger.View",
    role="guillotina.Anonymous")
configure.grant(
    permission="guillotina_swagger.View",
    role="guillotina.Authenticated")


def includeme(root):
    configure.scan("guillotina_swagger.services")
    configure.scan("guillotina_swagger.content")
