# -*- coding: utf-8 -*-
# Copyright 2022 - Marc Tormo i Bochaca - Batista10
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'IBEE',
    'summary': 'IBEE - Impost Begudes Ensucrades Envasades',
    'author': 'Batista10',
    'website': "https://github.com/B10Serveis/odoo-B10/tree/12.0/IBEE",
    'depends': ['account', 'product', 'sale', 'Dissenys_generics'],
    'version': '12.0.0.2.1',
    'license': 'AGPL-3',
    'application': True,
    'category': 'Account',
    'data': [
            'views/report_comanda_IBEE.xml',
            'views/report_pressupost_IBEE.xml',
            'views/report_proforma_IBEE.xml',
            'views/report_factura_IBEE.xml',
            'views/product_IBEE.xml',
            'views/sale_IBEE.xml',
            'views/invoice_IBEE.xml',
            'views/model520.xml',
            'views/model520_report.xml',
            'wizard/model520_wizard.xml'
    ],
}
