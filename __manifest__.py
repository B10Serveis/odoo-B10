# Copyright 2022, 2023, 2024, 2025 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Integració amb Damm",
    "summary": "Integració de dades amb Damm",
    "version": "15.0.0.0.0",
    "development_status": "Alpha",
    "category": "Sales",
    "website": "https://batista10.cat/",
    "author": "Batista10",
    "license": "AGPL-3",
    "description": """
Integració amb Damm
===================

Aquest mòdul facilita als distribuïdors de productes de S.A. Damm la integració de dades amb aquesta.

En particular, permet generar els següents informes en el format necessari per a enviar a Damm:

    * Dades dels clients de productes Damm
    * Dades de les condicions comercials dels clients
    * Vendes als clients
""",
    "depends": ["base_setup"],
    "data": [
        "security/groups.xml",
        "views/res_company_view.xml",
        "views/res_config_settings_view.xml",
    ],
}
