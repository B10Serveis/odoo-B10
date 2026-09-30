from odoo import models, fields, api, _
from odoo.tools import frozendict
from .tax import delivery_partner

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _convert_to_tax_base_line_dict(self):
        base_line = super()._convert_to_tax_base_line_dict()
        if self.move_id.is_invoice(include_receipts=True):
            base_line['partner'] = delivery_partner(self.move_id)
        return base_line

    @api.depends(
        'quantity', 'discount', 'price_unit', 'tax_ids', 'currency_id',
        'move_id.partner_shipping_id', 'move_id.partner_shipping_id.state_id',
        'move_id.partner_id', 'move_id.partner_id.state_id',
    )
    def _compute_totals(self):
        super()._compute_totals()
        group = self.env.ref('IBEE.tax_group_ibee', raise_if_not_found=False)
        if not group:
            return
        for line in self:
            if line.display_type != 'product' or not line.tax_ids.filtered(lambda tax: tax.tax_group_id == group):
                continue
            discounted_price = line.price_unit * (1 - line.discount / 100)
            totals = line.tax_ids.compute_all(
                discounted_price,
                quantity=line.quantity,
                currency=line.currency_id,
                product=line.product_id,
                partner=delivery_partner(line.move_id),
                is_refund=line.is_refund,
            )
            line.price_subtotal = totals['total_excluded']
            line.price_total = totals['total_included']

    @api.depends(
        'tax_ids', 'currency_id', 'partner_id', 'analytic_distribution',
        'balance', 'move_id.partner_id', 'move_id.partner_shipping_id',
        'move_id.partner_shipping_id.state_id', 'move_id.partner_id.state_id',
        'price_unit', 'quantity',
    )
    def _compute_all_tax(self):
        super()._compute_all_tax()
        group = self.env.ref('IBEE.tax_group_ibee', raise_if_not_found=False)
        if not group:
            return
        for line in self:
            if line.display_type == 'tax' or not line.tax_ids.filtered(lambda tax: tax.tax_group_id == group):
                continue
            sign = line.move_id.direction_sign
            if line.display_type == 'product' and line.move_id.is_invoice(True):
                amount_currency = sign * line.price_unit * (1 - line.discount / 100)
                handle_price_include = True
                quantity = line.quantity
            else:
                amount_currency = line.amount_currency
                handle_price_include = False
                quantity = 1
            result = line.tax_ids.compute_all(
                amount_currency,
                currency=line.currency_id,
                quantity=quantity,
                product=line.product_id,
                partner=delivery_partner(line.move_id) or line.partner_id,
                is_refund=line.is_refund,
                handle_price_include=handle_price_include,
                include_caba_tags=line.move_id.always_tax_exigible,
                fixed_multiplicator=sign,
            )
            rate = line.amount_currency / line.balance if line.balance else line.currency_rate
            line.compute_all_tax_dirty = True
            line.compute_all_tax = {
                frozendict({
                    'tax_repartition_line_id': tax['tax_repartition_line_id'],
                    'group_tax_id': tax['group'] and tax['group'].id or False,
                    'account_id': tax['account_id'] or line.account_id.id,
                    'currency_id': line.currency_id.id,
                    'analytic_distribution': ((tax['analytic'] or not tax['use_in_tax_closing']) and line.move_id.state == 'draft') and line.analytic_distribution,
                    'tax_ids': [(6, 0, tax['tax_ids'])],
                    'tax_tag_ids': [(6, 0, tax['tag_ids'])],
                    'partner_id': line.move_id.partner_id.id or line.partner_id.id,
                    'move_id': line.move_id.id,
                    'display_type': line.display_type,
                }): {
                    'name': tax['name'] + (' ' + _('(Discount)') if line.display_type == 'epd' else ''),
                    'balance': tax['amount'] / rate,
                    'amount_currency': tax['amount'],
                    'tax_base_amount': tax['base'] / rate * (-1 if line.tax_tag_invert else 1),
                }
                for tax in result['taxes']
                if tax['amount']
            }
            if not line.tax_repartition_line_id:
                line.compute_all_tax[frozendict({'id': line.id})] = {
                    'tax_tag_ids': [(6, 0, result['base_tags'])],
                }

    # Només visual: calcula l'IBEE de la línia
    ibee_amount = fields.Float(string='IBEE línia', compute='_compute_ibee_amount')

    @api.depends(
        'price_unit', 'discount', 'tax_ids', 'quantity', 'product_id',
        'move_id.partner_shipping_id', 'move_id.partner_shipping_id.state_id',
        'move_id.partner_id', 'move_id.partner_id.state_id', 'move_id.currency_id',
    )
    def _compute_ibee_amount(self):
        group = self.env.ref('IBEE.tax_group_ibee', raise_if_not_found=False)
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
                partner=delivery_partner(line.move_id),
            )
            # Map per identificar el grup d'impost a partir de l'id retornat al compute_all
            tax_map = {t.id: t for t in line.tax_ids.flatten_taxes_hierarchy()}
            amt = 0.0
            for t in res.get('taxes', []):
                tax = tax_map.get(t['id'])
                if tax and group and tax.tax_group_id == group:
                    amt += t.get('amount', 0.0)
            line.ibee_amount = amt
