from odoo import models, fields

class helpdeksB10(models.Model):
    _inherit = 'helpdesk.ticket'
    internal_note = fields.Html(string="Internal Note", required=False, )
    close_note = fields.Html(string="Closing Note", required=False, )
    email_ccs = fields.Many2many('res.partner', 'ticket_partner_rel', 'ticket_ids', 'partner_id',  string="CC", domain=[('email','=like','%@%')])
    related_contract = fields.Many2one('contract.contract', string="Contract")
    worked_hours = fields.Decimal(string="Worked Hours")

class partner_helpdesk_B10(models.Model):
        _inherit = 'res.partner'
        cc_email = fields.Many2many('helpdesk.ticket', 'ticket_partner_rel','partner_id','ticket_ids')