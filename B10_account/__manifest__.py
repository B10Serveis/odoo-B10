{
    "name": "Batista10 - Account",
    "summary": """Personalitzacions de Facturació""",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "category": "Personalization",
    "version": "15.0.1.3.2",
    "depends": [
        "account",
        "account_payment_partner",  # account.move:payment_mode_id
        "Dissenys_generics",  # account_payment_method_bank_transfer (ref)
    ],
    "license": "AGPL-3",
    "application": True,
    "data": [
        "views/partner_form_inherit.xml",
    ],
}
