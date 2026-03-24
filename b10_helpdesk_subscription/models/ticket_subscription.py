# Copyright (C) 2025 Batista10 (https://www.batista10.cat/).
# @author: Joan Llimiñana <joan@batista10.cat>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, exceptions, api, _


class helpdeksB10Subscription(models.Model):
    _inherit = "helpdesk.ticket"
    related_subscription = fields.Many2one(
        "sale.subscription",
        string="Subscription",
    )

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        return {
            "domain": {
                "related_subscription": [("partner_id", "=", self.partner_id.id)]
            }
        }
