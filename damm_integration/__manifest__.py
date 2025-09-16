# Copyright 2022, 2023, 2024, 2025 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Integració amb Damm",
    "summary": "Integració de dades amb Damm",
    "version": "18.0.0.9.0",
    "development_status": "Beta",
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
    "depends": [
        "base_setup",  # res.config.settings view
        "base_vat",  # res.partner.vat
        "l10n_es_partner",  # res.partner.comercial
        "account",  # account.move, reports menu
    ],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/res_company_view.xml",
        "views/res_config_settings_view.xml",
        "wizards/reports_view.xml",
    ],
}
