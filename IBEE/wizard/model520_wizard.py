from odoo import models, fields, api


class model520_wizard(models.TransientModel):
    _name = 'model520.wizard'
    _description = 'Wizard Model 520 IBEE'

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)

    @api.multi
    def get_report(self):
        data = self.env['report.model520_report'].report_values(date_start=self.date_start, date_end=self.date_end)
        return self.env.ref('IBEE.model520_report').report_action(self, data=data)
        