{
    'name': 'Andorra - Accounting',
    'summary': ('Creació de grups comptables, Pla General Comptable'
                ' i taxes andorranes (IGI, IRPF)'),
    # TODO: Replace with "17.0.1.0.0" when part of OCA.
    'version': '1.0',
    'icon': '/account/static/description/l10n.png',
    'countries': ['ad'],
    # TODO: Add ", Odoo Community Association (OCA)" when part of OCA.
    'author': 'Batista10',
    # TODO: Replace with "https://github.com/OCA/<repo>/tree/17.0/<addon>"
    # when part of OCA.
    'website': 'https://batista10.cat',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
Andorra Comptes Comptables
==========================

    * Creació de grups comptables
    * Creació del Pla General Comptable
    * Creació de taxes andorranes (IGI, IRPF)
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
