{
    "name": "Batista10 - Account",
    "summary": """Personalitzacions de Facturació""",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "category": "Personalization",
    "version": "17.0.1.2.0",
    "depends": [
        "account",
        "account_payment_partner",  # account.move:payment_mode_id
        "Dissenys_generics",  # account_payment_method_bank_transfer (ref)
    ],
    "license": "AGPL-3",
    "application": True,
    "data": ["views/invoice_report_pivot.xml"],
}
