from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    invoice_lines_by_origin = fields.Boolean(
        string="Group invoice lines by origin",
        config_parameter="b10_account.invoice_lines_by_origin",
        help="Groups invoice lines by origin on the standard designs",
    )
    b10_display_payment_term_table = fields.Boolean(
        string="Display payment term table",
        config_parameter="b10_account.b10_display_payment_term_table",
        help="Displays the payment term table on the standard designs",
    )

    # Modificacions per error de cron:
    # -Creem get_invoice_lines_by_origin() per poder obtenir el valor sense request.
    def get_invoice_lines_by_origin(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("b10_account.invoice_lines_by_origin", False)
        )

    def get_b10_display_payment_term_table(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("b10_account.b10_display_payment_term_table", False)
        )
