# -*- coding: utf-8 -*-
{
    "name": "Batista10 - Mail",
    "summary": "Override del layout d’email per mostrar només logo propi i eliminar el footer de Odoo",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "license": "AGPL-3",
    "depends": [
        "mail",
    ],
    "data": [
        "views/debrand_odoo_mail.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
