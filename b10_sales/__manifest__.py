{
    'name': 'B10 Sales',
    'summary': 'Personalització Vendes Batista10',
    'version': '18.0.1.1.0',
    'category': 'Sales',
    'author': 'Batista10',
    'website': 'https://www.batista10.cat',
    'license': 'AGPL-3',
    'depends': [
        'sale_management',
        'sale_order_report_product_image',
        'account_payment_sale',
        "l10n_es_partner",
        "l10n_es_partner_mercantil",
    ],
    'data': [
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
        'views/show_product_image.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
