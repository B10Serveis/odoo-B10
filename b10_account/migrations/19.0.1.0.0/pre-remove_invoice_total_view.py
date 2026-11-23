"""Remove the obsolete pivot extension before its field disappears from the registry."""


def migrate(cr, version):
    del version
    cr.execute(
        """
        DELETE FROM ir_ui_view
         WHERE id IN (
            SELECT res_id
              FROM ir_model_data
             WHERE module = 'b10_account'
               AND model = 'ir.ui.view'
               AND name = 'view_account_invoice_report_pivot_inherit'
         )
        """
    )
    cr.execute(
        """
        DELETE FROM ir_model_data
         WHERE module = 'b10_account'
           AND model = 'ir.ui.view'
           AND name = 'view_account_invoice_report_pivot_inherit'
        """
    )
