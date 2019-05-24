from guillotina import configure


configure.permission("guillotina_swagger.View", "View swagger definition")
configure.grant(
    permission="guillotina_swagger.View", role="guillotina.Anonymous"
)
configure.grant(
    permission="guillotina_swagger.View", role="guillotina.Authenticated"
)


app_settings = {
    "static": {"swagger_static": "guillotina_swagger:static"},
    "swagger": {
        "authentication_allowed": True,
        "base_url": None,
        "auth_storage_search_keys": ["auth"],
        "base_configuration": {
            "openapi": "3.0.0",
            "info": {
                "version": "1.0",
                "title": "Guillotina",
                "description": "The REST Resource API",
            },
            "servers": [
                    {
                        "url": "http://localhost:8080"
                    }
                ],
            "paths": {},
            "security": {"basicaAuth":[]},
            "components":{},
        },
    },
}


def includeme(root):
    configure.scan("guillotina_swagger.services")
    configure.scan("guillotina_swagger.content")
