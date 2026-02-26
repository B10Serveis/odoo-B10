from odoo import _, api, exceptions, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    allowed_pay_journal_ids = fields.Many2many(
        "account.journal",
        string="Allowed Payment Journals",
        compute="_compute_allowed_pay_journal_ids",
        help="Technical field used to constrain the valid choices of "
        "payment journal depending on the chosen payment mode.",
    )

    @api.depends("payment_mode_id")
    def _compute_allowed_pay_journal_ids(self):
        bank_transfer = self.env.ref(
            "b10_account.account_payment_method_bank_transfer",
            raise_if_not_found=False,
        )
        domain_tmpl = [
            "&",
            ("type", "=", "bank"),
            "&",
            ("bank_account_id", "!=", False),
            "REPLACE: JOURNAL ID CONDITION",
        ]
        journals = self.env["account.journal"]

        for order in self:
            order.allowed_pay_journal_ids = False

            payment_mode = order.payment_mode_id
            if (
                not bank_transfer
                or not payment_mode
                or bank_transfer != payment_mode.payment_method_id
            ):
                continue

            domain = domain_tmpl.copy()
            acct_link = payment_mode.bank_account_link
            if fixed_journal := (
                acct_link == "fixed" and payment_mode.fixed_journal_id
            ):
                domain[-1] = ("id", "=", fixed_journal.id)
            elif variable_journals := (
                acct_link == "variable" and payment_mode.variable_journal_ids
            ):
                domain[-1] = ("id", "in", variable_journals.mapped("id"))
            else:
                continue

            order.allowed_pay_journal_ids = journals.search(domain)

    payment_journal_id = fields.Many2one(
        "account.journal",
        string="Payment Journal",
        domain="[('id', 'in', allowed_pay_journal_ids)]",
        required=False,
        help="For sale orders with a payment method having a fixed bank account, "
        "this is the account associated with the method. "
        "When the method othewise has a set of bank accounts to choose from, "
        "this allows you to chose one of the accounts for paying the sale order.",
    )

    @api.constrains("payment_journal_id")
    def _check_nonempty_payment_journal(self):
        bank_transfer = self.env.ref(
            "b10_account.account_payment_method_bank_transfer",
            raise_if_not_found=False,
        )
        if not bank_transfer:
            return  # the constraint only applies to bank transfer payments

        for order in self:
            payment_mode = order.payment_mode_id
            assert (
                not payment_mode
                or not payment_mode.bank_account_link
                or payment_mode.bank_account_link in ["fixed", "variable"]
            )
            if (
                order.payment_journal_id
                or not payment_mode
                or payment_mode.payment_method_id != bank_transfer
                or (
                    payment_mode.bank_account_link == "fixed"
                    and not payment_mode.fixed_journal_id
                )
                or (
                    payment_mode.bank_account_link == "variable"
                    and not payment_mode.variable_journal_ids
                )
            ):
                continue
            raise models.ValidationError(
                _(
                    "A payment journal must be set with bank transfer payment modes "
                    "that have associated bank accounts."
                )
            )

    @api.onchange("payment_mode_id")
    def _set_payment_journal(self):
        payment_mode = self.payment_mode_id
        old_payment_journal = self.payment_journal_id

        assert (
            not payment_mode
            or not payment_mode.bank_account_link
            or payment_mode.bank_account_link in ["fixed", "variable"]
        )

        if not payment_mode or not payment_mode.bank_account_link:
            new_payment_journal = False
        elif payment_mode.bank_account_link == "fixed":
            new_payment_journal = payment_mode.fixed_journal_id
        elif not payment_mode.variable_journal_ids:
            new_payment_journal = False
        elif not old_payment_journal:
            new_payment_journal = payment_mode.variable_journal_ids[0]
        elif old_payment_journal in payment_mode.variable_journal_ids:
            new_payment_journal = old_payment_journal
        else:  # old journal not among variable ones
            new_payment_journal = payment_mode.variable_journal_ids[0]

        is_bank_transfer = False
        bank_transfer = self.env.ref(
            "b10_account.account_payment_method_bank_transfer",
            raise_if_not_found=False,
        )
        if (
            bank_transfer
            and payment_mode
            and payment_mode.payment_method_id == bank_transfer
        ):
            # The check only applies to bank transfer payments.
            is_bank_transfer = True

        if (
            is_bank_transfer
            and old_payment_journal
            and new_payment_journal != old_payment_journal
        ):
            raise exceptions.ValidationError(
                _(
                    "The current payment journal cannot be used "
                    "with the selected payment mode; "
                    "please unset the journal first if you are sure."
                )
            )
        self.payment_journal_id = new_payment_journal

    def _add_payment_to_invoice_vals(self, invoice_vals):
        self.ensure_one()
        if payment_mode := self.payment_mode_id:
            invoice_vals["payment_mode_id"] = payment_mode.id
        if payment_journal := self.payment_journal_id:
            invoice_vals["partner_bank_id"] = payment_journal.bank_account_id.id

    # Set invoice bank account if payment journal is set in sale order.
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        self._add_payment_to_invoice_vals(invoice_vals)
        return invoice_vals

    show_product_image = fields.Boolean("Show product image", required=False)

    # Override to set B10 email templates depending on the state of the SO (quotation vs sales order).
    def _find_mail_template(self):
        """Get the appropriate mail template for the current sales order based on its state.

        If the SO is confirmed, we return the mail template for the sale confirmation.
        Otherwise, we return the quotation email template.

        :return: The correct mail template based on the current status
        :rtype: record of `mail.template` or `None` if not found
        """
        self.ensure_one()
        # Proforma?
        if self.env.context.get("proforma"):
            return self.env.ref(
                "b10_sales.proforma_email_template",
                raise_if_not_found=False,
            )
        # Pressupost
        if self.state in ("draft", "sent"):
            return self.env.ref(
                "b10_sales.pressupost_email_template",
                raise_if_not_found=False,
            )
        else:
            return self._get_confirmation_template()

    # Override to set B10 email templates depending on the state of the SO (quotation vs sales order).
    def _get_confirmation_template(self):
        """Get the mail template sent on SO confirmation (or for confirmed SO's).

        :return: `mail.template` record or None if default template wasn't found
        """
        self.ensure_one()
        default_confirmation_template = self.env.ref(
            "b10_sales.comanda_email_template",
            raise_if_not_found=False,
        )
        if default_confirmation_template:
            return default_confirmation_template
        else:
            return self.env.ref(
                "sale.mail_template_sale_confirmation", raise_if_not_found=False
            )
