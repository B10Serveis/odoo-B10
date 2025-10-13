# Copyright (C) 2016-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Batista10 - Sales',
    'summary': 'Personalització Vendes Batista10',
    'version': '18.0.1.4.0',
    'category': 'Sales',
    'author': 'Batista10',
    'website': 'https://www.batista10.cat',
    'license': 'AGPL-3',
    'depends': [
        'b10_account',  # account_payment_method_bank_transfer (ref)
        'b10_mail',
        'sale_management',
        'sale_order_report_product_image',
        'account_payment_sale',
        "l10n_es_partner",
        "l10n_es_partner_mercantil",
        "b10_settings_hub",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/product_margin_classification.xml",
        "demo/product_product.xml",
    ],
    'data': [
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "data/decimal_precision.xml",
        "views/view_product_product.xml",
        "views/view_product_template.xml",
        "views/view_product_margin_classification.xml",
        # Reports
        'report/comanda_batista.xml',
        'report/pressupost_batista.xml',
        'report/pressupost_st_batista.xml',
        'report/proforma_batista.xml',
        'report/report_comanda_batista.xml',
        'report/report_pressupost_batista.xml',
        'report/report_pressupost_st_batista.xml',
        'report/report_proforma_batista.xml',
        # Views
        'views/B10_sale_order_expired_filter.xml',
        'views/sale_order_payment_journal.xml',
        'views/show_product_image.xml',
    ],
    'assets': {
    'web.assets_backend': [
        'b10_sales/static/src/css/form_stats.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
