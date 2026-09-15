from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    total_ibee = fields.Float("Total IBEE", readonly=True)

    def _select(self):
        tax_010 = self.env.ref("IBEE.tax_ibee_010", raise_if_not_found=False)
        tax_015 = self.env.ref("IBEE.tax_ibee_015", raise_if_not_found=False)
        # L'informe té una fila per línia de factura: calcular només l'IBEE
        # d'aquesta línia evita repetir tota la quota en cada producte.
        return super()._select() + f"""
            , CASE WHEN move.move_type IN ('out_invoice', 'out_refund', 'out_receipt')
                THEN line.quantity
                     * COALESCE(NULLIF(product.litres_IBEE, 0), template.litres_IBEE, 0)
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
