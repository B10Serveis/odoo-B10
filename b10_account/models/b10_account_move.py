from odoo import api, models, fields, _


class B10AccountMove(models.Model):
    _inherit = "account.move"

    group_by_origin = fields.Boolean(string="Group Invoice Lines by Origin")

    # Estableix la plantilla de correu electrònic per defecte de Factura
    def _get_mail_template(self):
        if self.move_type in ("out_invoice", "out_refund"):
            template = self.env.ref("b10_account.factura_email_template", raise_if_not_found=False)
            if template:
                return template.id
        # Per la resta, deleguem al mètode original
        return super(B10AccountMove, self)._get_mail_template()
    
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

    @api.depends("bank_partner_id")
    def _compute_partner_bank_id(self):
        for move in self:
            # This will get the bank account from the partner in an order with the trusted first
            bank_ids = move.bank_partner_id.bank_ids.filtered(
                lambda bank: not bank.company_id or bank.company_id == move.company_id
            ).sorted(lambda bank: not bank.allow_out_payment)
            # B10: Afegim condicional perque no reescrigui si ja n'hi ha
            if not move.partner_bank_id:
                move.partner_bank_id = bank_ids[:1]

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        # Aplica la configuració
        setting = self.env["res.config.settings"].sudo()
        group = setting.get_invoice_lines_by_origin()
        for inv in records:
            inv.group_by_origin = group
        return records

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
                    moves = sale_line.move_ids.filtered(lambda m: m.state == 'done')
                    # i per cadascun dels stock.move.line (operacions de lot)
                    for sml in moves.mapped('move_line_ids'):
                        lot = sml.lot_id
                        if lot:
                            lot_values.append({
                                'product_name': line.product_id.display_name,
                                'lot_name': lot.name,
                            })
        return lot_values
