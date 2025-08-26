from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # Només visual: calcula l'IBEE de la línia
    ibee_amount = fields.Float(string='IBEE línia', compute='_compute_ibee_amount')

    @api.depends('price_unit','discount','tax_ids','quantity','product_id','move_id.partner_id','move_id.currency_id')
    def _compute_ibee_amount(self):
        IBEE_GROUP_NAME = 'IBEE'
        for line in self:
            if line.display_type or not line.product_id:
                line.ibee_amount = 0.0
                continue
            base_price = (line.price_unit or 0.0) * (1 - (getattr(line, 'discount', 0.0) or 0.0)/100.0)
            res = line.tax_ids.compute_all(
                base_price,
                currency=line.move_id.currency_id,
                quantity=line.quantity or 0.0,
                product=line.product_id,
                partner=line.move_id.partner_id
            )
            # Map per identificar el grup d'impost a partir de l'id retornat al compute_all
            tax_map = {t.id: t for t in line.tax_ids.flatten_taxes_hierarchy()}
            amt = 0.0
            for t in res.get('taxes', []):
                tax = tax_map.get(t['id'])
                if tax and tax.tax_group_id and tax.tax_group_id.name == IBEE_GROUP_NAME:
                    amt += t.get('amount', 0.0)
            line.ibee_amount = amt
