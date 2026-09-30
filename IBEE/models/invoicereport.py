from odoo import models, fields, tools


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    total_ibee = fields.Float("Total IBEE", readonly=True)

    def _select(self):
        tax_010 = self.env.ref("IBEE.tax_ibee_010", raise_if_not_found=False)
        tax_015 = self.env.ref("IBEE.tax_ibee_015", raise_if_not_found=False)
        variant_litres = (
            "NULLIF(product.litres_ibee, 0)"
            if tools.column_exists(self.env.cr, "product_product", "litres_ibee")
            else "NULL"
        )
        template_litres = (
            "template.litres_ibee"
            if tools.column_exists(self.env.cr, "product_template", "litres_ibee")
            else "NULL"
        )
        # L'informe té una fila per línia de factura: calcular només l'IBEE
        # d'aquesta línia evita repetir tota la quota en cada producte.
        return super()._select() + f"""
            , CASE WHEN move.move_type IN ('out_invoice', 'out_refund', 'out_receipt')
                AND EXISTS (
                    SELECT 1
                    FROM res_partner delivery
                    JOIN res_country_state province ON province.id = delivery.state_id
                    JOIN res_country country ON country.id = province.country_id
                    WHERE delivery.id = COALESCE(move.partner_shipping_id, move.partner_id)
                      AND country.code = 'ES'
                      AND province.code IN ('B', 'GI', 'L', 'T')
                )
                THEN line.quantity
                     * COALESCE({variant_litres}, {template_litres}, 0)
                     * COALESCE((
                         SELECT SUM(CASE tax_rel.account_tax_id
                             WHEN {tax_010.id if tax_010 else 0} THEN 0.10
                             WHEN {tax_015.id if tax_015 else 0} THEN 0.15
                             ELSE 0 END)
                         FROM account_move_line_account_tax_rel tax_rel
                         WHERE tax_rel.account_move_line_id = line.id
                     ), 0)
                     * currency_table.rate
                     * CASE WHEN move.move_type = 'out_refund' THEN -1 ELSE 1 END
                ELSE 0 END AS total_ibee
        """
