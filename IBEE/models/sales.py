from odoo import models, fields, api
from .tax import delivery_partner

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _convert_to_tax_base_line_dict(self):
        base_line = super()._convert_to_tax_base_line_dict()
        base_line['partner'] = delivery_partner(self.order_id)
        return base_line

    @api.depends(
        'product_uom_qty', 'discount', 'price_unit', 'tax_id',
        'order_id.partner_shipping_id', 'order_id.partner_shipping_id.state_id',
        'order_id.partner_id', 'order_id.partner_id.state_id',
    )
    def _compute_amount(self):
        return super()._compute_amount()

    # Import d'IBEE per línia (només visual, no toca totals)
    ibee_amount = fields.Float(
        string='IBEE línia',
        compute='_compute_ibee_amount',
    )


    @api.depends(
        'product_uom_qty', 'discount', 'price_unit', 'tax_id', 'product_id',
        'order_id.partner_shipping_id', 'order_id.partner_shipping_id.state_id',
        'order_id.partner_id', 'order_id.partner_id.state_id', 'order_id.currency_id',
    )
    def _compute_ibee_amount(self):
        group = self.env.ref('IBEE.tax_group_ibee', raise_if_not_found=False)
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
                partner=delivery_partner(line.order_id),
            )
            # Identifica els impostos del grup 'IBEE'
            tax_map = {t.id: t for t in line.tax_id.flatten_taxes_hierarchy()}
            amt = 0.0
            for t in res.get('taxes', []):
                tax = tax_map.get(t['id'])
                if tax and group and tax.tax_group_id == group:
                    amt += t.get('amount', 0.0)
            line.ibee_amount = amt
