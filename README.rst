Introduction
============

A `guillotina` application to automatically generate swagger interfaces for
APIs defined with `guillotina`.


Configuration
-------------

Available config.json options::

    {
        "swagger": {
            "authentication_allowed": false,
            "base_configuration": {
                "swagger": "2.0",
                "info": {
                    "version": "",
                    "title": "Guillotina",
                    "description": "The REST Resource API"
                },
                "host": "",
                "basePath": "",
                "schemes": [],
                "produces": [
                    "application/json"
                ],
                "consumes": [
                    "application/json"
                ],
                "paths": {},
                "definitions": {}
            },
            "index_html": null
        }
    }


Viewing swagger for resource
----------------------------

Append `@docs` onto any url: `http://localhost:8080/@docs`.


Generating swagger docs
-----------------------

`guillotina_swagger` reads service configuration.

You can provide additional swagger configuration hints by providing a swagger
configuration with any of the following options:

- ignore: to prevent swagger from aggregating it
- additional_paths: provide a list of additional paths this configuration is used for(think routing here)
- display_permission: if you do not want to show permission setting, set this to false
- tags: what tags to use for it
