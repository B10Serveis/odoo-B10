{
    'name': "Field Encryption",
    'summary': """Encrypted fields data in database.""",
    'category': 'Technical Settings',
    "version": "17.0.0.2",
    "license": "AGPL-3",
    "author": "Marc Tormo i Bochaca <marc@batista10.cat>",
    "website": "https://github.com/ShahAlamSumon/field_encryption",
    "images": ["static/description/banner.gif"],
    "depends": ["base"],
    "post_init_hook": "post_init_hook",
    "external_dependencies": {
        "python": [
            'cryptography'
        ],
    },
}
