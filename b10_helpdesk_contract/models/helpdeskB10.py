from odoo import api, models, fields, _


class helpdeskB10(models.Model):
    _inherit = "helpdesk.ticket"

    related_contract = fields.Many2one("contract.contract", string="Contract")

    # Fer servir per ticket de Contractes Caducats
    current_time = fields.Datetime(string="Current time", compute="_get_current_time")

    def _get_current_time(self):
        for li in self:
            li.current_time = fields.Datetime.now()
