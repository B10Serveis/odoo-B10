from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Import d'IBEE per línia (només visual, no toca totals)
    ibee_amount = fields.Float(
        string='IBEE línia',
        compute='_compute_ibee_amount',
    )


    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'product_id', 'order_id.partner_shipping_id', 'order_id.currency_id')
    def _compute_ibee_amount(self):
        IBEE_GROUP_NAME = 'IBEE'
        for line in self:
            if line.display_type or not line.product_id:
                line.ibee_amount = 0.0
                continue

            base_price = (line.price_unit or 0.0) * (1 - (line.discount or 0.0)/100.0)
            res = line.tax_id.compute_all(
                base_price,
                currency=line.order_id.currency_id,
                quantity=line.product_uom_qty or 0.0,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id,
            )
            # Identifica els impostos del grup 'IBEE'
            tax_map = {t.id: t for t in line.tax_id.flatten_taxes_hierarchy()}
            amt = 0.0
            for t in res.get('taxes', []):
                tax = tax_map.get(t['id'])
                if tax and tax.tax_group_id and tax.tax_group_id.name == IBEE_GROUP_NAME:
                    amt += t.get('amount', 0.0)
            line.ibee_amount = amt
