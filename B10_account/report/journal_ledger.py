from datetime import date

from odoo import _, models


class B10JournalLedgerReport(models.AbstractModel):
    _name = "report.b10_account.journal_ledger"
    _inherit = "report.account_financial_report.journal_ledger"
    _description = "Mercantile Registry General Ledger Data"

    def _get_moves_domain(self, wizard, journal_ids):
        return [
            ("journal_id", "in", journal_ids),
            ("date", ">=", date(wizard.year, 1, 1)),
            ("date", "<=", date(wizard.year, 12, 31)),
            ("state", "=", "posted"),
        ]

    def _get_moves_order(self, wizard, journal_ids):
        # OCA's date order does not include a deterministic tie-breaker across
        # journals. The B10 book needs stable numbering when dates coincide.
        return "date asc, name asc, journal_id asc, id asc"

    def _get_move_lines_order(self, move_ids, wizard, journal_ids):
        return "move_id asc, id asc"

    def _get_opening_lines(self, wizard):
        company = wizard.company_id
        start_date = date(wizard.year, 1, 1)
        grouped = self.env["account.move.line"].read_group(
            [
                ("company_id", "=", company.id),
                ("parent_state", "=", "posted"),
                ("date", "<", start_date),
            ],
            ["balance:sum"],
            ["account_id"],
            lazy=False,
        )
        account_ids = [row["account_id"][0] for row in grouped if row.get("account_id")]
        accounts = {
            account.id: account
            for account in self.env["account.account"].browse(account_ids)
        }
        balances = {}
        profit_loss_balance = 0.0
        for row in grouped:
            account_ref = row.get("account_id")
            if not account_ref:
                continue
            account = accounts[account_ref[0]]
            balance = row.get("balance", 0.0)
            if account.internal_group in ("income", "expense"):
                profit_loss_balance += balance
            else:
                balances[account.id] = balance

        result_account = self.env["account.account"].search(
            [
                ("company_id", "=", company.id),
                ("code", "=like", "129%"),
            ],
            order="code, id",
            limit=1,
        )
        synthetic_result_balance = 0.0
        if result_account and profit_loss_balance:
            balances[result_account.id] = (
                balances.get(result_account.id, 0.0) + profit_loss_balance
            )
        elif profit_loss_balance:
            synthetic_result_balance = profit_loss_balance

        lines = []
        opening_label = _("Opening for fiscal year %(year)s") % {
            "year": wizard.year
        }
        for account_id, balance in balances.items():
            balance = company.currency_id.round(balance)
            if company.currency_id.is_zero(balance):
                continue
            account = accounts.get(account_id) or self.env[
                "account.account"
            ].browse(account_id)
            lines.append(
                {
                    "sequence": "1",
                    "date": start_date,
                    "entry": _("Opening entry"),
                    "account_code": account.code,
                    "account_name": account.name,
                    "partner": "",
                    "label": opening_label,
                    "debit": max(balance, 0.0),
                    "credit": max(-balance, 0.0),
                }
            )

        synthetic_result_balance = company.currency_id.round(
            synthetic_result_balance
        )
        if not company.currency_id.is_zero(synthetic_result_balance):
            lines.append(
                {
                    "sequence": "1",
                    "date": start_date,
                    "entry": _("Opening entry"),
                    "account_code": "129",
                    "account_name": _("Profit or loss for the year"),
                    "partner": "",
                    "label": opening_label,
                    "debit": max(synthetic_result_balance, 0.0),
                    "credit": max(-synthetic_result_balance, 0.0),
                }
            )

        if not lines:
            lines.append(
                {
                    "sequence": "1",
                    "date": start_date,
                    "entry": _("Opening entry"),
                    "account_code": "",
                    "account_name": "",
                    "partner": "",
                    "label": _("No opening balances"),
                    "debit": 0.0,
                    "credit": 0.0,
                }
            )
        return sorted(
            lines, key=lambda line: (line["account_code"], line["account_name"])
        )

    def _get_book_lines(self, wizard, data):
        values = super()._get_report_values(wizard.ids, data)
        lines = self._get_opening_lines(wizard)
        account_data = values["account_ids_data"]
        partner_data = values["partner_ids_data"]
        sequence = 1
        for move in values["Moves"]:
            sequence += 1
            entry = values["move_ids_data"][move["move_id"]]["entry"]
            for move_line in move["report_move_lines"]:
                account = account_data.get(move_line["account_id"], {})
                partner = partner_data.get(move_line["partner_id"], {})
                lines.append(
                    {
                        "sequence": str(sequence),
                        "date": move_line["date"],
                        "entry": entry,
                        "account_code": account.get("code", ""),
                        "account_name": account.get("name", ""),
                        "partner": partner.get("name", ""),
                        "label": move_line["label"],
                        "debit": move_line["debit"],
                        "credit": move_line["credit"],
                    }
                )
        return values, lines
