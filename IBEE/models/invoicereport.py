from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    total_ibee = fields.Float("Total IBEE", readonly=True)

    def _select(self):
        group = self.env.ref("IBEE.tax_group_ibee", raise_if_not_found=False)
        group_id = group.id if group else 0

        return (
            super()._select()
            + f"""
            , COALESCE((
                SELECT SUM(sub_line.balance)
                FROM account_move_line sub_line
                WHERE sub_line.move_id = line.move_id
                  AND sub_line.tax_line_id IN (
                      SELECT at.id
                      FROM account_tax at
                      WHERE at.tax_group_id = {group_id}
                  )
            ), 0.0) AS total_ibee
            """
        )

    def _group_by(self):
        # No afegim res perquè total_ibee és un SUM agregat per factura dins subquery
        return super()._group_by()
