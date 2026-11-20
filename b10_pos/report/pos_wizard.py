from datetime import datetime, time, timedelta

import pytz

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


class ReportPosClosing(models.AbstractModel):
    _name = "report.b10_pos.report_pos_closing_report"
    _description = "POS Closing Report"

    @api.model
    def _date_to_utc(self, date_value, timezone, end=False):
        date_value = fields.Date.to_date(date_value)
        if end:
            date_value += timedelta(days=1)
        local_datetime = timezone.localize(
            datetime.combine(date_value, time.min), is_dst=False
        )
        return local_datetime.astimezone(pytz.UTC).replace(tzinfo=None)

    @api.model
    def get_session(self, date_start, date_stop, config_id):
        if not self.env.user.has_group("point_of_sale.group_pos_user"):
            raise AccessError(_("Only Point of Sale users can print this report."))
        config = self.env["pos.config"].browse(config_id).exists()
        if not config:
            raise UserError(_("Select a point of sale to print the closing report."))
        config.ensure_one()
        config.check_access("read")
        timezone = pytz.timezone(
            self.env.context.get("tz") or self.env.user.tz or "UTC"
        )
        date_start = fields.Date.to_date(date_start or fields.Date.context_today(self))
        date_stop = fields.Date.to_date(date_stop or date_start)
        if date_stop < date_start:
            date_stop = date_start

        start_utc = self._date_to_utc(date_start, timezone)
        stop_utc = self._date_to_utc(date_stop, timezone, end=True)
        sessions = self.env["pos.session"].search(
            [
                ("state", "=", "closed"),
                ("config_id", "=", config_id),
                ("stop_at", ">=", fields.Datetime.to_string(start_utc)),
                ("stop_at", "<", fields.Datetime.to_string(stop_utc)),
            ],
            order="stop_at, id",
        )

        payment_groups = self.env["pos.payment"]._read_group(
            [
                ("session_id", "in", sessions.ids),
                ("pos_order_id.state", "in", ["paid", "invoiced", "done"]),
            ],
            ["session_id", "payment_method_id"],
            ["amount:sum"],
        )
        payments_by_session = {}
        for session, payment_method, amount in payment_groups:
            payments_by_session.setdefault(session.id, {})[
                payment_method.id
            ] = {"method": payment_method, "sold": amount or 0.0}

        # POS users can read these sessions without having accounting access.
        # Elevate only this aggregation, scoped to the sessions found above.
        declared_groups = self.env["account.payment"].sudo()._read_group(
            [
                ("pos_session_id", "in", sessions.ids),
                ("company_id", "=", config.company_id.id),
                ("state", "in", ["in_process", "paid"]),
                ("pos_payment_method_id", "!=", False),
            ],
            ["pos_session_id", "pos_payment_method_id", "currency_id", "payment_type"],
            ["amount:sum"],
        )
        declared_by_session = {}
        for session, payment_method, currency, payment_type, amount in declared_groups:
            signed_amount = (amount or 0.0) * (-1 if payment_type == "outbound" else 1)
            signed_amount = currency._convert(
                signed_amount, session.currency_id, session.company_id, session.stop_at
            )
            declared = declared_by_session.setdefault(session.id, {})
            declared[payment_method.id] = (
                declared.get(payment_method.id, 0.0) + signed_amount
            )

        rows = []
        for session in sessions:
            session_payments = payments_by_session.get(session.id, {})

            # Split bank payments record counting differences in a separate
            # move, even when account payments exist for the same method.
            for payment in session_payments.values():
                method = payment["method"]
                if method.type != "bank" or not method.split_transactions:
                    continue
                difference = self._get_counting_difference(session, method)
                if difference is not None:
                    declared_by_session.setdefault(session.id, {})[
                        method.id
                    ] = payment["sold"] + difference

            payment_rows = []
            for payment in session_payments.values():
                method = payment["method"]
                declared = None
                if method.is_cash_count:
                    declared = session.cash_register_balance_end_real
                elif method.id in declared_by_session.get(session.id, {}):
                    declared = declared_by_session[session.id][method.id]
                payment_rows.append(
                    {
                        "name": method.name,
                        "sold": payment["sold"],
                        "declared": declared,
                    }
                )
            payment_rows.sort(key=lambda payment: payment["name"].casefold())

            rows.append({"session": session, "payments": payment_rows})

        return {
            "date_start": date_start,
            "date_stop": date_stop,
            "config": config,
            "sessions": rows,
        }

    @api.model
    def _get_counting_difference(self, session, method):
        # Odoo does not link these moves to the session. Reconstruct the
        # standard reference in every installed language, including English
        # references from older versions, independently of the report language.
        languages = {code for code, _name in self.env["res.lang"].get_installed()}
        languages.add("en_US")
        references = {
            session.with_context(lang=code)._get_diff_account_move_ref(
                method.with_context(lang=code)
            )
            for code in languages
        }
        moves = self.env["account.move"].sudo().search(
            [
                ("ref", "in", list(references)),
                ("journal_id", "=", method.journal_id.id),
                ("company_id", "=", session.company_id.id),
                ("state", "=", "posted"),
            ]
        )
        journal = method.sudo().journal_id
        accounts = journal.profit_account_id | journal.loss_account_id
        lines = moves.line_ids.filtered(lambda line: line.account_id in accounts)
        if not lines:
            return None
        return sum(
            -line.amount_currency
            if line.currency_id == session.currency_id
            else session.company_id.currency_id._convert(
                -line.balance, session.currency_id, session.company_id, session.stop_at
            )
            for line in lines
        )

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        report_data = self.get_session(
            data.get("date_start"),
            data.get("date_stop"),
            data.get("config_id") or (docids[0] if docids and len(docids) == 1 else False),
        )
        return {
            "doc_ids": report_data["config"].ids,
            "doc_model": "pos.config",
            "docs": report_data["config"],
            **report_data,
        }
