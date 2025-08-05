# -*- coding: utf-8 -*-
{
    "name": "Batista10 - Stock Picking",
    "summary": "Personalització de la impressió de les entregues",
    "version": "18.0.1.0.0",
    "category": "Warehouse/Reporting",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "b10_mail",
    ],
    "data": [
        "report/entrega_batista.xml",
        "report/report_entrega_batista.xml",
        "views/email_entrega.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
