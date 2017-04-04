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
            }
        }
    }


Viewing swagger for resource
----------------------------

Append `@docs` onto any url: `http://localhost:8080/@docs`.
