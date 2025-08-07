# Copyright (C) 2016-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Batista10 - Products",
    "version": "18.0.1.0.0",
    "category": "Account",
    "author": "GRAP,Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/OCA/sale-workflow",
    "license": "AGPL-3",
    "depends": ["sale", "sale_management"],
    "data": [
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "data/decimal_precision.xml",
        "views/view_product_product.xml",
        "views/view_product_template.xml",
        "views/view_product_margin_classification.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/product_margin_classification.xml",
        "demo/product_product.xml",
    ],
    'assets': {
    'web.assets_backend': [
        'b10_products/static/src/css/form_stats.scss',
        ],
    },

    "installable": True,
    "application": True,
}
