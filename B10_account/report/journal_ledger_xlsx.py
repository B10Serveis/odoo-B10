from odoo import _, models


class B10JournalLedgerXlsx(models.AbstractModel):
    _name = "report.b10_account.journal_ledger_xlsx"
    _description = "Mercantile Registry General Ledger XLSX Report"
    _inherit = "report.account_financial_report.abstract_report_xlsx"

    def _get_report_name(self, report, data=False):
        return _("Mercantile Registry General Ledger - %(year)s - %(company)s") % {
            "year": report.year,
            "company": report.company_id.name,
        }

    def _get_report_columns(self, report):
        columns = [
            {"header": _("Number"), "field": "sequence", "width": 9},
            {"header": _("Date"), "field": "date", "width": 12},
            {"header": _("Journal entry"), "field": "entry", "width": 22},
            {"header": _("Account"), "field": "account_code", "width": 14},
        ]
        if report.with_account_name:
            columns.append(
                {"header": _("Account name"), "field": "account_name", "width": 30}
            )
        columns += [
            {"header": _("Partner"), "field": "partner", "width": 28},
            {"header": _("Label"), "field": "label", "width": 42},
            {"header": _("Debit"), "field": "debit", "type": "amount", "width": 15},
            {"header": _("Credit"), "field": "credit", "type": "amount", "width": 15},
        ]
        return {index: column for index, column in enumerate(columns)}

    def _get_report_filters(self, report):
        return [
            [_("Company"), report.company_id.display_name],
            [_("Fiscal year"), str(report.year)],
            [_("Moves"), _("Posted entries only")],
            [_("Order"), _("Date, entry number, and journal")],
        ]

    def _get_col_count_filter_name(self):
        return 2

    def _get_col_count_filter_value(self):
        return 4

    def _generate_report_content(self, workbook, report, data, report_data):
        _, lines = self.env[
            "report.b10_account.journal_ledger"
        ]._get_book_lines(report, data)
        amount_format = "#,##0." + ("0" * report.company_id.currency_id.decimal_places)
        report_data["formats"]["format_amount"].set_num_format(amount_format)
        sheet = report_data["sheet"]
        self.write_array_header(report_data)
        header_row = report_data["row_pos"] - 1
        first_data_row = report_data["row_pos"]

        for line in lines:
            self.write_line_from_dict(line, report_data)

        sheet.freeze_panes(first_data_row, 0)
        if report_data["row_pos"] > first_data_row:
            sheet.autofilter(
                header_row,
                0,
                report_data["row_pos"] - 1,
                len(report_data["columns"]) - 1,
            )
