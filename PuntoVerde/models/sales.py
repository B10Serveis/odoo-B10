from odoo import models, fields, api


class sale_order_line_PuntoVerde(models.Model):
    _inherit = 'sale.order.line'

    PuntoVerde_sale = fields.Float(
        string='PuntoVerde', compute='_compute_amount')

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        Line_PuntoVerde = 0.0
        for line in self:
            Line_PuntoVerde = float(
                line.product_id.PuntoVerde) * line.product_uom_qty
            price = (line.price_unit *
                     (1 - (line.discount or 0.0) / 100.0)) + line.product_id.PuntoVerde
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
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
        product = self.product_id.with_context(
            force_company=self.company_id.id)
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
            'PuntoVerde_invoice': self.PuntoVerde_sale,
        }
        return res


class account_invoice_line_PuntoVerde(models.Model):
    _inherit = 'account.invoice.line'

    PuntoVerde_invoice = fields.Float(
        string='PuntoVerde', compute='_compute_price')

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        PuntoVerde = float(self.product_id.PuntoVerde) * self.quantity
        self.PuntoVerde_invoice = PuntoVerde
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = (self.price_unit *
                 (1 - (self.discount or 0.0) / 100.0)) + self.product_id.PuntoVerde
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(
                price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes[
            'total_excluded'] if taxes else self.quantity * price
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            currency = self.invoice_id.currency_id
            date = self.invoice_id._get_currency_rate_date()
            price_subtotal_signed = currency._convert(
                price_subtotal_signed, self.invoice_id.company_id.currency_id, self.company_id or self.env.user.company_id, date or fields.Date.today())
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign
