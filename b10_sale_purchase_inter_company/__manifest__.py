{
    "name": "Batista10 - Inter Company Module for Sale to Purchase Order",
    "summary": "Intercompany SO/PO rules",
    # TODO: Replace with "17.0.X.Y.Z" when part of OCA.
    "version": "1.0.1",
    "category": "Sales Management",
    # TODO: Replace with "https://github.com/OCA/multi-company" when part of OCA.
    "website": "https://www.batista10.cat",
    # TODO: Add ", Odoo Community Association (OCA)" when part of OCA.
    "author": "Batista10",
    "license": "AGPL-3",
    "application": True,
    "depends": ["sale_management", "sale", "purchase", "account_invoice_inter_company"],
    "data": ["views/res_config_view.xml"],
}
