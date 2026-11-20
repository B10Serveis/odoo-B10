from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class helpdeskB10(models.Model):
    _inherit = "helpdesk.ticket"

    related_contract = fields.Many2one("contract.contract", string="Contract")

    @api.constrains("related_contract", "partner_id", "company_id")
    def _check_related_contract(self):
        for ticket in self:
            contract = ticket.related_contract
            if not contract:
                continue
            allowed_partners = ticket.partner_id | ticket.partner_id.commercial_partner_id
            if not ticket.partner_id or contract.partner_id not in allowed_partners:
                raise ValidationError(_(
                    "The contract must belong to the ticket contact or its commercial entity."
                ))
            if contract.company_id and contract.company_id != ticket.company_id:
                raise ValidationError(_(
                    "The contract must belong to the same company as the ticket."
                ))

    # Fer servir per ticket de Contractes Caducats
    current_time = fields.Datetime(string="Current time", compute="_get_current_time")

    def _get_current_time(self):
        for li in self:
            li.current_time = fields.Datetime.now()
