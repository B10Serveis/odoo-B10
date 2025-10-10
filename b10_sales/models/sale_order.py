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
            "&", ("type", "=", "bank"),
            "&", ("bank_account_id", "!=", False),
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
            if fixed_journal := (acct_link == "fixed"
                                 and payment_mode.fixed_journal_id):
                domain[-1] = ("id", "=", fixed_journal.id)
            elif variable_journals := (acct_link == "variable"
                                       and payment_mode.variable_journal_ids):
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

    @api.onchange("payment_mode_id")
    def _set_payment_journal(self):
        payment_mode = self.payment_mode_id
        new_payment_journal = (
            payment_mode.fixed_journal_id
            if payment_mode.bank_account_link == "fixed" else False
        )

        if self.payment_journal_id and new_payment_journal != self.payment_journal_id:
            raise exceptions.ValidationError(
                _("The current payment journal cannot be used "
                  "with the selected payment mode; "
                  "please unset the journal first if you are sure."))
        self.payment_journal_id = new_payment_journal

    show_product_image = fields.Boolean("Show product image", required=False)

    def _get_default_mail_template_id(self):
        self.ensure_one()
        # Proforma?
        if self.env.context.get("proforma"):
            return self.env.ref(
                "b10_sales.proforma_email_template",
                raise_if_not_found=False,
            ).id
        # Pressupost
        if self.state in ("draft", "sent"):
            return self.env.ref(
                "b10_sales.pressupost_email_template",
                raise_if_not_found=False,
            ).id
        # Comanda confirmada
        if self.state in ("sale", "done"):
            return self.env.ref(
                "b10_sales.comanda_email_template",
                raise_if_not_found=False,
            ).id
        # Caigui pel genèric
        return super()._get_default_mail_template_id()
