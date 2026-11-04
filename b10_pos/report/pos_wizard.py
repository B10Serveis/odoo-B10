from datetime import datetime, time, timedelta

import pytz

from odoo import api, fields, models


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
        timezone = pytz.timezone(
            self.env.context.get("tz") or self.env.user.tz or "UTC"
        )
        date_start = fields.Date.to_date(date_start)
        date_stop = fields.Date.to_date(date_stop)
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

        declared_groups = self.env["account.payment"]._read_group(
            [("pos_session_id", "in", sessions.ids)],
            ["pos_session_id", "pos_payment_method_id"],
            ["amount:sum"],
        )
        declared_by_session = {}
        for session, payment_method, amount in declared_groups:
            if payment_method:
                declared_by_session.setdefault(session.id, {})[
                    payment_method.id
                ] = amount or 0.0

        rows = []
        for session in sessions:
            session_payments = payments_by_session.get(session.id, {})

            # A recorded accounting difference is also a declared amount in
            # Odoo's standard POS details report when no account payment exists.
            for payment in session_payments.values():
                method = payment["method"]
                if method.is_cash_count or method.id in declared_by_session.get(
                    session.id, {}
                ):
                    continue
                difference_move = self.env["account.move"].search(
                    [
                        (
                            "ref",
                            "=",
                            "Closing difference in %s (%s)" % (method.name, session.name),
                        ),
                        ("journal_id", "=", method.journal_id.id),
                    ],
                    limit=1,
                )
                if difference_move:
                    is_loss = any(
                        line.account_id == method.journal_id.loss_account_id
                        for line in difference_move.line_ids
                    )
                    difference = (
                        -difference_move.amount_total
                        if is_loss
                        else difference_move.amount_total
                    )
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
            "config": self.env["pos.config"].browse(config_id),
            "sessions": rows,
        }

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        report_data = self.get_session(
            data.get("date_start"),
            data.get("date_stop"),
            data.get("config_id"),
        )
        return {
            "doc_ids": report_data["config"].ids,
            "doc_model": "pos.config",
            "docs": report_data["config"],
            **report_data,
        }
