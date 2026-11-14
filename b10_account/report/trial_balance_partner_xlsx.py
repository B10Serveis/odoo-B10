from odoo import _, models


class TrialBalancePartnerXlsx(models.AbstractModel):
    _name = "report.b10_account.trial_balance_partner_xlsx"
    _inherit = "report.a_f_r.report_trial_balance_xlsx"
    _description = "Balanç de sumes i saldos per partner XLSX"

    def _get_report_name(self, report, data=False):
        return _("Balanç de sumes i saldos per partner")

    def _get_report_columns(self, report):
        columns = super()._get_report_columns(report.new({
            "show_partner_details": False, "foreign_currency": report.foreign_currency,
        }))
        # Resolve inherited captions in this module's translation catalog too.
        headers = {
            "code": _("Code"), "name": _("Account"),
            "initial_balance": _("Initial balance"), "debit": _("Debit"),
            "credit": _("Credit"), "balance": _("Period balance"),
            "ending_balance": _("Ending balance"),
            "initial_currency_balance": _("Initial balance in currency"),
            "ending_currency_balance": _("Ending balance in currency"),
        }
        for column in columns.values():
            column["header"] = headers[column["field"]]
        # Always use the account columns, regardless of hidden wizard values.
        columns = {index + (index >= 2): value
                   for index, value in columns.items()}
        columns[2] = {"header": _("Partner"), "field": "partner_name", "width": 40}
        if report.foreign_currency:
            columns = {index + (index >= 8): value
                       for index, value in columns.items()}
            columns[8] = {"header": _("Divisa"), "field": "currency_name", "width": 10}
        return dict(sorted(columns.items()))

    def _get_report_filters(self, report):
        return [
            [_("Company"), report.company_id.display_name],
            [_("Date range filter"), _("From: %(date_from)s To: %(date_to)s") % {
                "date_from": report.date_from, "date_to": report.date_to,
            }],
            [_("Target moves filter"), _("All posted entries")
             if report.target_move == "posted" else _("All entries")],
            [_("Account at 0 filter"), _("Hide") if report.hide_account_at_0 else _("Show")],
            [_("Show foreign currency"), _("Yes") if report.foreign_currency else _("No")],
        ]

    def _generate_report_content(self, workbook, report, data, report_data):
        values = self.env["report.b10_account.trial_balance_partner"]._get_report_values(
            report.ids, data
        )
        self.write_array_header(report_data)
        first_row = report_data["row_pos"]
        for row in values["partner_rows"]:
            self.write_line_from_dict(row, report_data)
        sheet = report_data["sheet"]
        sheet.freeze_panes(first_row, 3)
        if values["partner_rows"]:
            sheet.autofilter(first_row - 1, 0, report_data["row_pos"] - 1,
                             len(report_data["columns"]) - 1)
        totals = dict(values["partner_totals"], code="", name=_("Total"),
                      partner_name="", currency_id=False, currency_name="")
        self.write_account_footer(totals, _("Total"), report_data)
