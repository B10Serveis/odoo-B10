# -*- coding: utf-8 -*-
# Copyright 2022 - Marc Tormo i Bochaca - Batista10
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'IBEE',
    'summary': 'IBEE - Impost Begudes Ensucrades Envasades',
    'author': 'Marc Tormo - Batista10',
    'website': "https://github.com/B10Serveis/Odoo-addons/IBEE",
    'depends': ['account', 'product', 'sale'],
    'version': '12.0.0.1.0',
    'license': 'AGPL-3', 
    'application': True,
    'category': 'Account',
    'data': [
            'views/product_IBEE.xml',
            'views/sale_IBEE.xml',
            'views/invoice_IBEE.xml',
            'views/model520.xml',
            'views/model520_report.xml',
            'wizard/model520_wizard.xml',
    ],
}
