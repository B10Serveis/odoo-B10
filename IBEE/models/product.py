from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    IBEE = fields.Selection(
        selection=[('0','Exempt'),('0.1','0.10'),('0.15','0.15')],
        string='IBEE',
        default='0'
    )

    litres_IBEE = fields.Float('Litres x Unitat', default=0.0)

    @api.onchange('IBEE')
    def _onchange_ibee_tax(self):
        self.ensure_one()
        tax_010 = self.env.ref('IBEE.tax_ibee_010', raise_if_not_found=False)
        tax_015 = self.env.ref('IBEE.tax_ibee_015', raise_if_not_found=False)
        # conserva tots els impostos de venda que no siguin del grup IBEE
        keep = self.taxes_id.filtered(
            lambda t: t.type_tax_use == 'sale' and (not t.tax_group_id or t.tax_group_id.name != 'IBEE')
        )
        if self.IBEE == '0.1' and tax_010:
            self.taxes_id = [(6, 0, (keep | tax_010).ids)]
        elif self.IBEE == '0.15' and tax_015:
            self.taxes_id = [(6, 0, (keep | tax_015).ids)]
        else:
            # Exempt: treu qualsevol impost IBEE
            self.taxes_id = [(6, 0, keep.ids)]

class ProductVariant(models.Model):
    _inherit = 'product.product'
    litres_IBEE = fields.Float('Litres x Unitat', default=0.0)
