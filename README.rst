Introduction
============

This project is an attempt to provide easy swagger integration for your
guillotina application.


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
