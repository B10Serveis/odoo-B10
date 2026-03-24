# Copyright (C) 2025 Batista10 (https://www.batista10.cat/).
# @author: Joan Llimiñana <joan@batista10.cat>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Batista10 - Helpdesk Subscriptions",
    "summary": ("Hides contract relation in tickets"
                " and adds subscription relation"),
    "author": "Batista10",
    "version": "1.0.2",
    "application": False,
    "installable": True,
    "license": "AGPL-3",
    "depends": [
        "base",
        "helpdesk_mgmt",
        "subscription_oca",
        "b10_helpdesk",
    ],
    "data": [
        "views/ticket_view.xml",
    ],
}
