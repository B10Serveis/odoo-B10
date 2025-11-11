from odoo import api, exceptions, models, fields, _


class B10AccountMove(models.Model):
    _inherit = "account.move"

    # Similar to `b10_sales:sale.order:_check_nonempty_payment_journal()`,
    # but checking the actual value as the field has no domain restrictions.
    @api.constrains("partner_bank_id")
    def _check_transfer_partner_bank(self):
        bank_transfer = self.env.ref(
            "Dissenys_generics.account_payment_method_bank_transfer",
            raise_if_not_found=False,
        )
        if not bank_transfer:
            return  # the constraint only applies to bank transfer payments

        for move in self:
            payment_mode = move.payment_mode_id
            assert (not payment_mode or not payment_mode.bank_account_link
                    or payment_mode.bank_account_link in ["fixed", "variable"])
            partner_bank = move.partner_bank_id
            if (
                    not payment_mode
                    or payment_mode.payment_method_id != bank_transfer
                    or (payment_mode.bank_account_link == "fixed"
                        and partner_bank == payment_mode.fixed_journal_id.bank_account_id)
                    or (payment_mode.bank_account_link == "variable"
                        and partner_bank
                        and partner_bank in payment_mode.variable_journal_ids.mapped("bank_account_id"))
            ):
                continue
            raise models.ValidationError(
                _("A recipient bank must be set which is valid for "
                  "the current bank transfer payment mode."))

    # Similar to `b10_sales:sale.order:_set_payment_journal()`.
    @api.onchange("payment_mode_id")
    def _onchange_payment_mode_id_b10(self):
        payment_mode = self.payment_mode_id
        old_partner_bank = self.partner_bank_id

        assert (not payment_mode or not payment_mode.bank_account_link
                or payment_mode.bank_account_link in ["fixed", "variable"])

        if not payment_mode or not payment_mode.bank_account_link:
            new_partner_bank = False
        elif payment_mode.bank_account_link == "fixed":
            new_partner_bank = payment_mode.fixed_journal_id.bank_account_id
        elif not payment_mode.variable_journal_ids:
            new_partner_bank = False
        elif not old_partner_bank:
            new_partner_bank = payment_mode.variable_journal_ids[0].bank_account_id
        elif old_partner_bank in payment_mode.variable_journal_ids.bank_account_id:
            new_partner_bank = old_partner_bank
        else:  # old bank not among variable ones
            new_partner_bank = payment_mode.variable_journal_ids[0].bank_account_id

        is_bank_transfer = False
        bank_transfer = self.env.ref(
            "Dissenys_generics.account_payment_method_bank_transfer",
            raise_if_not_found=False,
        )
        if bank_transfer and payment_mode and payment_mode.payment_method_id == bank_transfer:
            # The check only applies to bank transfer payments.
            is_bank_transfer = True

        if is_bank_transfer and old_partner_bank and new_partner_bank != old_partner_bank:
            raise exceptions.ValidationError(
                _("The current recipient bank cannot be used "
                  "with the selected payment mode; "
                  "please unset the bank first if you are sure."))
        self.partner_bank_id = new_partner_bank

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
