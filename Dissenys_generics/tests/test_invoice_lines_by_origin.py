from odoo.tests import TransactionCase


class TestInvoiceLinesByOrigin(TransactionCase):
    def test_config_parameter_is_converted_to_boolean(self):
        parameter = self.env["ir.config_parameter"].sudo()
        settings = self.env["res.config.settings"]
        key = "dissenys_generics.invoice_lines_by_origin"

        parameter.set_param(key, "False")
        self.assertIs(settings.get_invoice_lines_by_origin(), False)

        parameter.set_param(key, "True")
        self.assertIs(settings.get_invoice_lines_by_origin(), True)
