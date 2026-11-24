{
    'name': "Field Encryption",
    'summary': """Encrypted fields data in database.""",
    'category': 'Technical Settings',
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "author": "Shah Alam Sumon",
    "website": "https://github.com/ShahAlamSumon/field_encryption",
    "images": ["static/description/banner.gif"],
    "depends": ["base"],
    "external_dependencies": {
        "python": [
            'cryptography'
        ],
    },
    "installable": True,
}
