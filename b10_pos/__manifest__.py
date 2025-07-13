{
    "name": "Batista10 - POS",
    "summary": """Personalització POS Batista10""",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "category": "Personalization",
    "version": "17.0.1.0.0",
    "depends": ["point_of_sale"],
    "license": "AGPL-3",
    "application": True,
    'data': [
            'security/ir.model.access.csv',
            'views/pos_closing.xml',
        	'views/pos_closing_report.xml',
			'wizard/pos_wizard_report.xml'
			],
	'installable': True,
}
