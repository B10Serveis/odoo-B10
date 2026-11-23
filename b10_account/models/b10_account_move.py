from odoo import api, exceptions, models, fields, _


class B10AccountMove(models.Model):
    _inherit = "account.move"

    group_by_origin = fields.Boolean(string="Group Invoice Lines by Origin")
    b10_display_payment_term_table = fields.Boolean(string="Display Payment Term Table")

    # Estableix la plantilla de correu electrònic per defecte de Factura
    def _get_mail_template(self):
        if self.move_type in ("out_invoice", "out_refund"):
            template = self.env.ref(
                "b10_account.factura_email_template", raise_if_not_found=False
            )
            if template:
                return template  # Canviat de template.id a template perque el mètode original pot retornar un registre i no un ID.
        # Per la resta, deleguem al mètode original
        return super(B10AccountMove, self)._get_mail_template()

    # Similar to `b10_sales:sale.order:_check_nonempty_payment_journal()`,
    # but checking the actual value as the field has no domain restrictions.
    @api.constrains("partner_bank_id", "payment_mode_id")
    def _check_transfer_partner_bank(self):
        bank_transfer = self.env.ref(
            "b10_account.account_payment_method_bank_transfer",
            raise_if_not_found=False,
        )
        if not bank_transfer:
            return  # the constraint only applies to bank transfer payments

        for move in self:
            payment_mode = move.payment_mode_id
            assert (
                not payment_mode
                or not payment_mode.bank_account_link
                or payment_mode.bank_account_link in ["fixed", "variable"]
            )
            partner_bank = move.partner_bank_id
            if (
                not payment_mode
                or payment_mode.payment_method_id != bank_transfer
                or (
                    payment_mode.bank_account_link == "fixed"
                    and payment_mode.fixed_journal_id.bank_account_id
                    and partner_bank == payment_mode.fixed_journal_id.bank_account_id
                )
                or (
                    payment_mode.bank_account_link == "variable"
                    and partner_bank
                    and partner_bank
                    in payment_mode.variable_journal_ids.mapped("bank_account_id")
                )
            ):
                continue
            raise exceptions.ValidationError(
                _(
                    "A recipient bank must be set which is valid for "
                    "the current bank transfer payment mode."
                )
            )

    # Similar to `b10_sales:sale.order:_set_payment_journal()`.
    @api.onchange("payment_mode_id")
    def _onchange_payment_mode_id_b10(self):
        payment_mode = self.payment_mode_id
        bank_transfer = self.env.ref(
            "b10_account.account_payment_method_bank_transfer",
            raise_if_not_found=False,
        )
        if (
            not self.is_inbound(include_receipts=True)
            or not bank_transfer
            or not payment_mode
            or payment_mode.payment_method_id != bank_transfer
        ):
            return

        old_partner_bank = self.partner_bank_id

        assert (
            not payment_mode
            or not payment_mode.bank_account_link
            or payment_mode.bank_account_link in ["fixed", "variable"]
        )

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

        if old_partner_bank and new_partner_bank != old_partner_bank:
            raise exceptions.ValidationError(
                _(
                    "The current recipient bank cannot be used "
                    "with the selected payment mode; "
                    "please unset the bank first if you are sure."
                )
            )
        self.partner_bank_id = new_partner_bank

    @api.depends(
        "bank_partner_id", "currency_id", "preferred_payment_method_line_id",
        "payment_mode_id",
    )
    def _compute_partner_bank_id(self):
        super()._compute_partner_bank_id()
        bank_transfer = self.env.ref(
            "b10_account.account_payment_method_bank_transfer",
            raise_if_not_found=False,
        )
        for move in self:
            payment_mode = move.payment_mode_id
            if not bank_transfer or payment_mode.payment_method_id != bank_transfer:
                continue
            if payment_mode.bank_account_link == "fixed":
                move.partner_bank_id = payment_mode.fixed_journal_id.bank_account_id
            elif payment_mode.bank_account_link == "variable":
                allowed_banks = payment_mode.variable_journal_ids.bank_account_id
                if move.partner_bank_id not in allowed_banks:
                    move.partner_bank_id = allowed_banks[:1]

    @api.model_create_multi
    def create(self, vals_list):
        setting = self.env["res.config.settings"].sudo()
        group = setting.get_invoice_lines_by_origin()
        display_payment_terms = setting.get_b10_display_payment_term_table()
        for vals in vals_list:
            vals.setdefault("group_by_origin", group)
            vals.setdefault("b10_display_payment_term_table", display_payment_terms)
        return super().create(vals_list)

    def _get_invoiced_lot_values(self):
        """
        Retorna una llista de diccionaris amb
        {'product_name': ..., 'lot_name': ...}
        per a cada lot facturat a les línies.
        """
        lot_values = []
        for inv in self:
            for line in inv.invoice_line_ids:
                # per cada línia de venda associada
                for sale_line in line.sale_line_ids:
                    # filtre els stock moves fets (delivered/done)
                    moves = sale_line.move_ids.filtered(lambda m: m.state == "done")
                    # i per cadascun dels stock.move.line (operacions de lot)
                    for sml in moves.mapped("move_line_ids"):
                        lot = sml.lot_id
                        if lot:
                            lot_values.append(
                                {
                                    "product_name": line.product_id.display_name,
                                    "lot_name": lot.name,
                                }
                            )
        return lot_values
