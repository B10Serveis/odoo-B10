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
                    move.partner_bank_id = (
                        move.payment_mode_id.fixed_journal_id.bank_account_id
                    )

    @api.depends("bank_partner_id", "payment_mode_id")
    def _compute_partner_bank_id(self):
        bank_transfer = self.env.ref(
            "Dissenys_generics.account_payment_method_bank_transfer",
            raise_if_not_found=False,
        )
        for move in self:
            # This will get the bank account from the partner in an order with the trusted first
            payment_mode = move.payment_mode_id
            def get_bank_id():
                if not payment_mode:
                    return False
                if (
                        not bank_transfer
                        or payment_mode.payment_method_id != bank_transfer
                ):
                    return fields.first(move.bank_partner_id.bank_ids.filtered(
                        lambda bank: not bank.company_id or bank.company_id == move.company_id
                    ).sorted(lambda bank: not bank.allow_out_payment))
                if payment_mode.bank_account_link == "fixed":
                    return payment_mode.fixed_journal_id.bank_account_id
                assert payment_mode.bank_account_link == "variable"
                return payment_mode.variable_journal_ids[0].bank_account_id
            # B10: Afegim condicional perque no reescrigui si ja n'hi ha
            if not move.partner_bank_id:
                move.partner_bank_id = get_bank_id()
