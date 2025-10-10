{
    "name": "B10 - Sales",
    "summary": """B10 Sales""",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "category": "Personalization",
    "version": "17.0.1.0.0",
    "depends": [
        "sale",
        "Dissenys_generics",  # account_payment_method_bank_transfer (ref), reports
    ],
    "license": "AGPL-3",
    "application": True,
    "data": [
        "views/B10_sale_order_expired_filter.xml",
        "views/sale_order_payment_journal.xml",
        "report/report_comanda_batista_iban.xml",
        "report/report_pressupost_batista_iban.xml",
        "report/report_proforma_batista_iban.xml",
    ],
}