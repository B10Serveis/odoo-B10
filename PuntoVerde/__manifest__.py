# -*- coding: utf-8 -*-
# Copyright 2022 - Marc Tormo i Bochaca - Batista10
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'PuntoVerde',
    'summary': 'PuntoVerde - Impost de punt verd i plàstics',
    'author': 'Batista10',
    'website': "https://github.com/B10Serveis/odoo-B10/tree/12.0/PuntoVerde",
    'depends': ['account', 'product', 'sale', 'Dissenys_generics'],
    'version': '12.0.0.1.1',
    'license': 'AGPL-3',
    'application': True,
    'category': 'Account',
    'data': [
            'views/report_comanda_PuntoVerde.xml',
            'views/report_pressupost_PuntoVerde.xml',
            'views/report_proforma_PuntoVerde.xml',
            'views/report_factura_PuntoVerde.xml',
            'views/product_PuntoVerde.xml',
            'views/sale_PuntoVerde.xml',
            'views/invoice_PuntoVerde.xml'
    ],
}
