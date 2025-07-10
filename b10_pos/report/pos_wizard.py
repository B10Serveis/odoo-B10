from datetime import timedelta
import pytz
from odoo import api, fields, models

class ReportPosReportClosing(models.AbstractModel):
    _name = 'report.b10_pos.report_pos_closing_report'
    _description = 'POS Closing Report'

    @api.model
    def get_session(self, date_ini=False, date_fi=False, config_id=False):
        # Obtenim el record de configuració
        if isinstance(config_id, int):
            config = self.env['pos.config'].browse(config_id)
        else:
            config = config_id or self.env['pos.config']

        # Timezone de l'usuari
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
        today_local = fields.Datetime.context_timestamp(
            self, 
            fields.Datetime.from_string(fields.Date.context_today(self))
        )
        today_utc = today_local.astimezone(pytz.UTC)

        # Dates d'inici i fi
        if date_ini:
            dt_ini = fields.Datetime.from_string(date_ini)
        else:
            dt_ini = today_utc
        if date_fi:
            dt_fi = fields.Datetime.from_string(date_fi) + timedelta(days=1, seconds=-1)
        else:
            dt_fi = today_utc + timedelta(days=1, seconds=-1)
        
        # Ens assegurem que fi >= ini
        dt_fi = max(dt_fi, dt_ini)
        date_ini_str = fields.Datetime.to_string(dt_ini)
        date_fi_str  = fields.Datetime.to_string(dt_fi)

        # Cerquem les sessions POS en l'interval
        session_domain = [
            ('start_at', '>=', date_ini_str),
            ('start_at', '<=', date_fi_str),
        ]
        if config and config.id:
            session_domain.append(('config_id', '=', config.id))
        sessions = self.env['pos.session'].search(session_domain)

        # Nom de la configuració
        name_pos = config.name if config and config.id else ''

        # Cerquem moviments bancaris de POS
        bank_domain = [
            ('create_date', '>=', date_ini_str),
            ('create_date', '<=', date_fi_str),
        ]
        if config and config.id:
            bank_domain.append(('pos_session_id.config_id', '=', config.id))
        bank_statements = self.env['account.bank.statement'].search(bank_domain)

        # Agrupar imports per sessió
        amount_map = {}
        for stmt in bank_statements:
            key = stmt.pos_session_id.name
            amount_map.setdefault(key, 0.0)
            amount_map[key] += stmt.total_entry_encoding

        return {
            'ident': config.id if config and config.id else False,
            'name': name_pos,
            'date_ini': date_ini_str,
            'date_fi':  date_fi_str,
            'sessions': [{
                'session_id':   s.id,
                'session_name': s.name,
                'session_stat': dict(
                    self.env['pos.session']
                        ._fields['state']
                        ._description_selection(self.env)
                )[s.state],
                'session_ini':  s.start_at,
                'session_fi':   s.stop_at,
                'session_amount': amount_map.get(s.name, 0.0),
            } for s in sessions],
            'linies': [{
                'fpago':      stmt.journal_id.name,
                'declarat':   stmt.balance_end,
                'canvi':      stmt.balance_start,
                'total':      stmt.total_entry_encoding,
                'session_nom': stmt.pos_session_id.name,
            } for stmt in bank_statements],
        }

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})

        report_data = self.get_session(
            data.get('date_start'),
            data.get('date_stop'),
            data.get('session_id')
        )

        context = {
            'doc_ids':    docids,
            'doc_model':  'pos.config',
            'docs':       self.env['pos.config'].browse(data.get('session_id')),
            'date_start': data.get('date_start'),
            'date_stop':  data.get('date_stop'),
            **report_data,
        }
        return context

