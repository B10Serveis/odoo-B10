# Copyright 2025 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "POS Choose Product then Search",
    "summary": ("Makes POS activate the search box again"
                " right after clicking on a product."),
    "version": "18.0.0.0.0",
    "development_status": "Alpha",
    "category": "Point of Sale",
    "website": "https://batista10.cat/",
    "author": "Batista10",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "point_of_sale",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_choose_then_search/static/src/**/*",
        ],
    },
}
