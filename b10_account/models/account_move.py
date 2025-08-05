from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    group_by_origin = fields.Boolean(string="Group Invoice Lines by Origin")

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

