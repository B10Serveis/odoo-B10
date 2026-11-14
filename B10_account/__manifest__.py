{
    "name": "Batista10 - Account",
    "summary": """Personalitzacions de Facturació""",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "category": "Personalization",
    "version": "17.0.1.6.0",
    "depends": [
        "account",
        "account_financial_report",  # Trial balance partner report and XLSX export
        "account_payment_partner",  # account.move:payment_mode_id
        "Dissenys_generics",  # account_payment_method_bank_transfer (ref)
        "l10n_es_mis_report",  # Spanish PGCE MIS report templates and MIS Builder
    ],
    "license": "AGPL-3",
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "wizard/trial_balance_partner_views.xml",
        "report/trial_balance_partner.xml",
        "views/partner_form_inherit.xml",
        "data/mis_report_styles.xml",
        "data/mis_report_balance_abreviated_3digits.xml",
        "data/mis_report_pyg_abreviated_3digits.xml",
    ],
}
