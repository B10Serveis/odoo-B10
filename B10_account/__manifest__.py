{
    "name": "Batista10 - Account",
    "summary": """Personalitzacions de Facturació""",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "category": "Personalization",
    "version": "17.0.1.8.0",
    "depends": [
        "account",
        "account_financial_report",  # Trial balance partner report and XLSX export
        "account_payment_partner",  # account.move:payment_mode_id
        "Dissenys_generics",  # account_payment_method_bank_transfer (ref)
        "l10n_es_mis_report",  # Spanish PGCE MIS report templates and MIS Builder
    ],
    "license": "AGPL-3",
    "application": True,
    "assets": {
        "web.assets_backend": [
            "B10_account/static/src/js/journal_ledger_report.esm.js",
        ],
    },
    "data": [
        "security/ir.model.access.csv",
        "wizard/trial_balance_partner_views.xml",
        "wizard/journal_ledger_views.xml",
        "report/journal_ledger.xml",
        "report/trial_balance_partner.xml",
        "views/account_journal_dashboard.xml",
        "views/partner_form_inherit.xml",
        "data/mis_report_styles.xml",
        "data/mis_report_balance_abreviated_3digits.xml",
        "data/mis_report_pyg_abreviated_3digits.xml",
    ],
}
