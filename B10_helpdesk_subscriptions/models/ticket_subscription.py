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
