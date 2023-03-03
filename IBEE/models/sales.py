from odoo import models, fields, api
from functools import partial
from odoo.tools.misc import formatLang


class sale_order_line_IBEE(models.Model):
    _inherit = 'sale.order.line'

    PuntoVerde_sale = fields.Float(string='PuntoVerde', compute='_compute_amount')
    IBEE_sale = fields.Float(string='IBEE', compute='_compute_amount')

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
       
        for line in self:
            IBEE_unit=line.product_id.litres_IBEE * float(line.product_id.IBEE)
            PuntoVerde_unit=float(line.product_id.PuntoVerde)
            
            Line_PuntoVerde = PuntoVerde_unit * line.product_uom_qty
            Line_IBEE = IBEE_unit * line.product_uom_qty
            
            price = (line.price_unit * (1 - (line.discount or 0.0) / 100.0)) + PuntoVerde_unit + IBEE_unit

            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'IBEE_sale': Line_IBEE,
                'PuntoVerde_sale': Line_PuntoVerde,
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {}
        product = self.product_id.with_context(force_company=self.company_id.id)
        account = product.property_account_income_id or product.categ_id.property_account_income_categ_id

        if not account and self.product_id:
            raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                            (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

        fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
        if fpos and account:
            account = fpos.map_account(account)

        res = {
            'name': self.name,
            'sequence': self.sequence,
            'origin': self.order_id.name,
            'account_id': account.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'discount': self.discount,
            'uom_id': self.product_uom.id,
            'product_id': self.product_id.id or False,
            'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
            'account_analytic_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'display_type': self.display_type,
            'IBEE_invoice': self.IBEE_sale,
            'PuntoVerde_invoice': self.PuntoVerde_sale,
        }
        return res
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def _amount_by_group(self):
        for order in self:
            currency = order.currency_id or order.company_id.currency_id
            fmt = partial(formatLang, self.with_context(lang=order.partner_id.lang).env, currency_obj=currency)
            res = {}
            for line in order.order_line:
                IBEE_unit=line.product_id.litres_IBEE * float(line.product_id.IBEE)
                PuntoVerde_unit=float(line.product_id.PuntoVerde)
                
                price_reduce = (line.price_unit * (1 - (line.discount or 0.0) / 100.0)) + PuntoVerde_unit + IBEE_unit
                taxes = line.tax_id.compute_all(price_reduce, quantity=line.product_uom_qty, product=line.product_id, partner=order.partner_shipping_id)['taxes']
                for tax in line.tax_id:
                    group = tax.tax_group_id
                    res.setdefault(group, {'amount': 0.0, 'base': 0.0})
                    for t in taxes:
                        if t['id'] == tax.id or t['id'] in tax.children_tax_ids.ids:
                            res[group]['amount'] += t['amount']
                            res[group]['base'] += t['base']
            res = sorted(res.items(), key=lambda l: l[0].sequence)
            order.amount_by_group = [(
                l[0].name, l[1]['amount'], l[1]['base'],
                fmt(l[1]['amount']), fmt(l[1]['base']),
                len(res),
            ) for l in res]
   
    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        invoice_ids = super(SaleOrder, self).action_invoice_create(
            grouped=grouped, final=final
        )
        invoices = self.env['account.invoice'].browse(invoice_ids)
        for inv in invoices:
            inv._onchange_invoice_line_ids()
        return invoice_ids
    

class account_invoice_line_IBEE(models.Model):
    _inherit = 'account.invoice.line'

    PuntoVerde_invoice = fields.Float(string='PuntoVerde', compute='_compute_price')
    IBEE_invoice = fields.Float(string='IBEE', compute='_compute_price')

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        IBEE_unit=self.product_id.litres_IBEE * float(self.product_id.IBEE)
        PuntoVerde_unit=float(self.product_id.PuntoVerde)
        
        self.PuntoVerde_invoice = PuntoVerde_unit * self.quantity
        self.IBEE_invoice = IBEE_unit * self.quantity

        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = (self.price_unit * (1 - (self.discount or 0.0) / 100.0)) + PuntoVerde_unit + IBEE_unit
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            currency = self.invoice_id.currency_id
            date = self.invoice_id._get_currency_rate_date()
            price_subtotal_signed = currency._convert(
                price_subtotal_signed, self.invoice_id.company_id.currency_id, self.company_id or self.env.user.company_id, date or fields.Date.today())
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign

class account_invoice_IBEE(models.Model):
    _inherit = 'account.invoice'
            
    @api.multi
    def get_taxes_values(self):
        
        tax_grouped = {}
        round_curr = self.currency_id.round
        for line in self.invoice_line_ids:
            IBEE_unit=line.product_id.litres_IBEE * float(line.product_id.IBEE)
            PuntoVerde_unit=float(line.product_id.PuntoVerde)
            if not line.account_id or line.display_type:
                continue
            price_unit = (line.price_unit * (1 - (line.discount or 0.0) / 100.0)) + PuntoVerde_unit + IBEE_unit
            taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity, line.product_id, self.partner_id)['taxes']
            for tax in taxes:
                val = self._prepare_tax_line_vals(line, tax)
                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                    tax_grouped[key]['base'] = round_curr(val['base'])
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += round_curr(val['base'])
        return tax_grouped