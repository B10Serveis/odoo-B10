from odoo import api, fields, models

class PosClosingWizard(models.TransientModel):
    _name = 'pos.closing.wizard'
    _description = 'Wizard POS Closing Report'

    start_date = fields.Date(required=True, default=fields.Date.context_today)
    end_date   = fields.Date(required=True, default=fields.Date.context_today)
    pos_session_id = fields.Many2one(
        'pos.config',
        string='Point of Sale Configuration',
        required=True,
    )

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    def generate_report(self):
        data = {
            'date_start': self.start_date,
            'date_stop':  self.end_date,
            'session_id': self.pos_session_id.id,
        }
        return self.env.ref('b10_pos.pos_closing_report') \
                   .report_action(self, data=data)
