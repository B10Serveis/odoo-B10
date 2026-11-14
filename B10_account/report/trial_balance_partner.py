from odoo import _, models


class TrialBalancePartner(models.AbstractModel):
    _name = "report.b10_account.trial_balance_partner"
    _inherit = "report.account_financial_report.trial_balance"
    _description = "Balanç de sumes i saldos per partner"

    def _get_report_values(self, docids, data):
        data = dict(
            data,
            partner_ids=[],
            show_partner_details=False,
            show_hierarchy=False,
            grouped_by=False,
        )
        # Keep the OCA report's fiscal-year and retained-earnings rules.
        res = super()._get_report_values(docids, data)
        common = dict(
            account_ids=data["account_ids"],
            journal_ids=data["journal_ids"],
            partner_ids=[],
            company_id=data["company_id"],
            only_posted_moves=data["only_posted_moves"],
            show_partner_details=False,
        )
        initial_bs = self._get_initial_balances_bs_ml_domain(
            **common, date_from=data["date_from"]
        )
        initial_pl = self._get_initial_balances_pl_ml_domain(
            **common,
            date_from=data["date_from"],
            fy_start_date=data["fy_start_date"],
        )
        period = self._get_period_ml_domain(
            **common, date_from=data["date_from"], date_to=data["date_to"]
        )
        amount_fields = [
            "initial_balance",
            "debit",
            "credit",
            "balance",
            "ending_balance",
            "initial_currency_balance",
            "ending_currency_balance",
        ]
        rows = {}
        account_ids = set()

        def accumulate(domain, initial=False, destination=False):
            groups = self.env["account.move.line"].read_group(
                domain,
                [
                    "account_id",
                    "partner_id",
                    "balance:sum",
                    "debit:sum",
                    "credit:sum",
                    "amount_currency:sum",
                ],
                ["account_id", "partner_id"],
                lazy=False,
            )
            for group in groups:
                account_id = destination or group["account_id"][0]
                partner = group["partner_id"]
                key = (account_id, partner[0] if partner else 0)
                account_ids.add(account_id)
                row = rows.setdefault(
                    key,
                    dict(
                        {field: 0.0 for field in amount_fields},
                        partner_id=key[1],
                        partner_name=partner[1] if partner else _("Sense partner"),
                    ),
                )
                if initial:
                    row["initial_balance"] += group["balance"]
                    row["initial_currency_balance"] += group["amount_currency"]
                else:
                    for field in ("debit", "credit", "balance"):
                        row[field] += group[field]
                row["ending_balance"] += group["balance"]
                row["ending_currency_balance"] += group["amount_currency"]

        accumulate(initial_bs, initial=True)
        accumulate(initial_pl, initial=True)
        accumulate(period)

        # OCA transfers previous fiscal years' P&L to this account only when
        # there is no explicit account selection. Preserve its partner detail.
        earnings = data["unaffected_earnings_account"]
        if earnings and not data["account_ids"]:
            accumulate(
                self._get_initial_balance_fy_pl_ml_domain(
                    **common, fy_start_date=data["fy_start_date"]
                ),
                initial=True,
                destination=earnings,
            )

        accounts = self._get_accounts_data(list(account_ids))
        currency = res["company_currency"]
        flat_rows = []
        for (account_id, partner_id), row in rows.items():
            if data["hide_account_at_0"] and all(
                currency.is_zero(row[field])
                for field in (
                    "initial_balance",
                    "debit",
                    "credit",
                    "ending_balance",
                )
            ):
                continue
            row.update(accounts[account_id])
            flat_rows.append(row)
        if not data["hide_account_at_0"]:
            # Include unused accounts, as the standard balance does.
            for account_id, account in res["accounts_data"].items():
                if account_id not in account_ids:
                    flat_rows.append(
                        dict(
                            {field: 0.0 for field in amount_fields},
                            **account,
                            partner_id=0,
                            partner_name=_("Sense partner"),
                        )
                    )
        flat_rows.sort(
            key=lambda row: (
                row["code"],
                row["partner_name"].casefold(),
                row["partner_id"],
            )
        )
        res.update(
            docs=self.env[data["wizard_name"]].browse(data["wizard_id"]),
            doc_model=data["wizard_name"],
            partner_rows=flat_rows,
            partner_totals={
                field: sum(row[field] for row in flat_rows) for field in amount_fields
            },
        )
        return res
