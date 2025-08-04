{
    'name': 'Andorra - Accounting',
    'summary': '""Creació de grups comptables, Pla General Comptable i taxes Andorranes (IGI, IRPF)""',
    "version": "18.0.0.1",
    'icon': '/account/static/description/l10n.png',
    'countries': ['ad'],
    'author': 'Batista10',
    'website': 'https://batista10.cat',    
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
Andorra Comptes Comptables 
==========================

    * Creació de grups comptables
    * Creació del Pla General Comptable
    * Creació de taxes Andorranes (IGI, IRPF)
""",
    'depends': [
        'account',
        'base_iban',
        'base_vat',
    ],
    'data': [        
        'data/res_partner_data.xml',
    ],
    'license': 'LGPL-3',
}
