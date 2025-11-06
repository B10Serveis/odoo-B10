# Copyright 2024, 2025 Batista10
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'Andorra - Accounting',
    'summary': ('Creation of account groups, general chart of accounts'
                ' and Andorran taxes (IGI, IRPF)'),
    'version': '17.0.1.0.0',
    'icon': '/account/static/description/l10n.png',
    'countries': ['ad'],
    # TODO: Add ", Odoo Community Association (OCA)" when part of OCA.
    'author': 'Batista10',
    # TODO: Replace with "https://github.com/OCA/<repo>/tree/17.0/<addon>"
    # when part of OCA.
    'website': 'https://batista10.cat',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
Andorran Charts of Accounts
===========================

    * Creation of account groups
    * Creation of general chart of accounts
    * Creation of Andorran taxes (IGI, IRPF)
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
