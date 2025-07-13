from datetime import timedelta
import pytz
from odoo import api, fields, models

class ReportPosReportClosing(models.AbstractModel):
    _name = 'report.b10_pos.report_pos_closing_report'
    _description = 'POS Closing Report'

    @api.model
    def get_session(self, date_ini=False, date_fi=False, config_id=False):
        # Obtenim el POS config
        config = self.env['pos.config'].browse(config_id) if config_id else False

        # Timezone de l'usuari
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
        today_local = fields.Datetime.context_timestamp(
            self,
            fields.Datetime.from_string(fields.Date.context_today(self))
        )
        # Convertim a UTC
        today_utc = today_local.astimezone(pytz.UTC)

        # Dates d'inici i fi
        dt_ini = fields.Datetime.from_string(date_ini) if date_ini else today_utc
        dt_fi  = fields.Datetime.from_string(date_fi) + timedelta(days=1, seconds=-1)  if date_fi  else today_utc + timedelta(days=1, seconds=-1)
        dt_fi  = max(dt_fi, dt_ini)

        date_ini_str = fields.Datetime.to_string(dt_ini)
        date_fi_str  = fields.Datetime.to_string(dt_fi)

        # Cerquem sessions dins l'interval
        session_domain = [
            ('start_at', '>=', date_ini_str),
            ('start_at', '<=', date_fi_str),
        ]
        if config:
            session_domain.append(('config_id', '=', config.id))
        sessions = self.env['pos.session'].search(session_domain)

        # Cerquem pagaments per aquestes sessions
        payments = self.env['pos.payment'].search([
            ('session_id', 'in', sessions.ids),
            ('create_date', '>=', date_ini_str),
            ('create_date', '<=', date_fi_str),
        ])

        # Agrupar imports per sessió
        amount_map = {}
        lines = []
        for pay in payments:
            sess_name = pay.session_id.name
            method    = pay.payment_method_id.name
            amount_map.setdefault(sess_name, 0.0)
            amount_map[sess_name] += pay.amount
            lines.append({
                'fpago':       method,
                'declarat':    pay.amount,
                'canvi':       0.0,
                'total':       pay.amount,
                'session_nom': sess_name,
            })

        return {
            'ident':       config.id if config else False,
            'name':        config.name if config else '',
            'date_ini':    date_ini_str,
            'date_fi':     date_fi_str,
            'sessions': [{
                'session_id':     s.id,
                'session_name':   s.name,
                'session_stat':   dict(
                    self.env['pos.session']
                        ._fields['state']
                        ._description_selection(self.env)
                )[s.state],
                'session_ini':    s.start_at,
                'session_fi':     s.stop_at,
                'session_amount': amount_map.get(s.name, 0.0),
            } for s in sessions],
            'linies': lines,
        }

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        report_data = self.get_session(
            data.get('date_start'),
            data.get('date_stop'),
            data.get('session_id'),
        )
        return {
            'doc_ids':   docids,
            'doc_model': 'pos.config',
            'docs':      self.env['pos.config'].browse(data.get('session_id')),
            **report_data,
        }
