# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# List of contributors:
# Marc Tormo <marc@batista10.cat>

{
    "name" : "WooCommerce Spain TAX compatibility",
    "version" : "0.1",
    "author" : "Batista10",
    'category': 'Localization',
    "description": """
WooCommerce Spain TAX 
==========================

    * Creació de plantilles i impostos de woocommerce a Odoo
    * Compatibilitzar amb llibre de IVA i model 303
""",
    "depends" : [
        'account',
        'l10n_es',
        'base_vat',
        'l10n_es_aeat_mod303',
        'l10n_es_vat_book',
    ],
    "data" : [
        'data/account_tax_data.xml',
    ],
}
