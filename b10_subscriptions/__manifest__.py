# Copyright (C) 2026 Batista10 (https://www.batista10.cat/).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Batista10 - Subscriptions",
    "summary": "Add analytic distributions and payment modes to subscriptions",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "category": "Sales/Subscriptions",
    "version": "16.0.2.0.0",
    "license": "AGPL-3",
    "depends": [
        "subscription_oca",
        "analytic",
        "product_analytic",
        "account_payment_partner",
        "account_payment_sale",
    ],
    "data": [
        "views/sale_subscription_views.xml",
    ],
    "installable": True,
    "application": False,
}
