from odoo import api, models, fields, _


class B10AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange("payment_mode_id")
    def _onchange_payment_mode_id_b10(self):
        for move in self:
            # Que fem si la factura ja te ficat un num de compte i canviem el mètode de pagament?
            if (
                move.payment_mode_id.payment_method_id.code == "bank_transfer"
                and move.payment_mode_id.bank_account_link == "fixed"
                and move.payment_mode_id.fixed_journal_id
            ):
                if move.payment_mode_id.fixed_journal_id.bank_account_id.acc_number:
                    move.invoice_partner_bank_id = (
                        move.payment_mode_id.fixed_journal_id.bank_account_id
                    )

    @api.depends("bank_partner_id")
    def _compute_invoice_invoice_partner_bank_id(self):
        for move in self:
            filtered_bank_partner_id = move.bank_partner_id.bank_ids.filtered(
                lambda bank: bank.company_id is False
                or bank.company_id == move.company_id
            )
            if not move.invoice_invoice_partner_bank_id:
                move.invoice_partner_bank_id = (
                    filtered_bank_partner_id and filtered_bank_partner_id[0]
                )
