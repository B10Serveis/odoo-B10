{
    "name": "B10 Commission Report",
    "version": "16.0.1.0.0",
    "summary": "Commission report per account move line (one row per agent)",
    "category": "Accounting/Accounting",
    "author": "Batista10",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_commission",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/b10_commission_report_views.xml",
    ],
    "installable": True,
    "application": False,
}
