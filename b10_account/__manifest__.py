{
    "name": "Batista10 - Account",
    "summary": """Personalitzacions de Facturació""",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "category": "Personalization",
    "version": "18.0.1.1.0",
    "depends": ["account", "base","account_payment"],
    "license": "AGPL-3",
    "application": True,
    "data": [
        "views/config_settings_view.xml",
        "views/account_move_inherit.xml",
        "report/factura_batista.xml",
        "report/report_factura_batista.xml",
    ],
}
