{
    "name": "Batista10 - Account",
    "summary": """Personalitzacions de Facturació""",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "category": "Personalization",
    "version": "16.0.1.4.0",
    "depends": [
        "account",
        "account_payment_partner",  # account.move:payment_mode_id
        "Dissenys_generics",  # account_payment_method_bank_transfer (ref)
        "l10n_es_mis_report",  # Spanish PGCE MIS templates and MIS Builder
    ],
    "license": "AGPL-3",
    "application": True,
    "data": [
        "views/invoice_report_pivot.xml",
        "views/partner_form_inherit.xml",
        "data/mis_report_styles.xml",
        "data/mis_report_balance_abreviated_3digits.xml",
        "data/mis_report_pyg_abreviated_3digits.xml",
    ],
}
