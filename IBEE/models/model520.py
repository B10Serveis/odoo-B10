from odoo import api, fields, models
from datetime import timedelta
import pytz

class Model520(models.AbstractModel):
    _name = 'report.model520_report'
    _description = 'Informe Model 520 IBEE'

    @api.model
    def _get_report_values(self, date_start=False, date_end=False):
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
        today_utc = user_tz.localize(fields.Datetime.to_datetime(fields.Date.context_today(self))).astimezone(pytz.timezone('UTC'))
        date_start = fields.Datetime.to_datetime(date_start) if date_start else today_utc
        date_end = fields.Datetime.to_datetime(date_end) if date_end else (today_utc + timedelta(days=1, seconds=-1))
        date_end = max(date_end, date_start)

        company = self.env.user.company_id

        # Impostos IBEE
        tax010 = self.env.ref('IBEE.tax_ibee_010', raise_if_not_found=False)
        tax015 = self.env.ref('IBEE.tax_ibee_015', raise_if_not_found=False)
        tax_ids = [t.id for t in (tax010, tax015) if t]

        quota_IBEE5 = quota_IBEE8 = 0.0

        if tax_ids:
            tax_lines = self.env['account.move.line'].search([
                ('move_id.date', '>=', date_start),
                ('move_id.date', '<=', date_end),
                ('move_id.state', '=', 'posted'),
                ('move_id.move_type', 'in', ['out_invoice', 'out_refund']),
                ('tax_line_id', 'in', tax_ids),
                ('company_id', '=', company.id),
            ])

            if tax010:
                quota_IBEE5 = sum(abs(l.balance) for l in tax_lines if l.tax_line_id.id == tax010.id)
            if tax015:
                quota_IBEE8 = sum(abs(l.balance) for l in tax_lines if l.tax_line_id.id == tax015.id)

        IBEE5_litres = quota_IBEE5 / 0.10 if tax010 else 0.0
        IBEE8_litres = quota_IBEE8 / 0.15 if tax015 else 0.0

        total = quota_IBEE5 + quota_IBEE8

        return {
            'NIF': company.vat,
            'name': company.name,
            'street': company.street,
            'codpostal': company.zip,
            'pais': company.country_id.name,
            'provincia': company.state_id.name,
            'municipi': company.city,
            'IBEE8': round(IBEE8_litres, 2),         
            'IBEE5': round(IBEE5_litres, 2),          
            'quota_IBEE8': round(quota_IBEE8, 2),
            'quota_IBEE5': round(quota_IBEE5, 2),
            'total': round(total, 2),
        }
