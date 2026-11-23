from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAccountMove(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.partner = cls.env["res.partner"].create({"name": "Bank transfer customer"})
        cls.sale_journal = cls.env["account.journal"].create({
            "name": "B10 Sales", "code": "B10S", "type": "sale",
            "company_id": cls.company.id,
        })

    def _invoice(self, **values):
        return self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner.id,
            "journal_id": self.sale_journal.id,
            "company_id": self.company.id,
            **values,
        })

    def test_configuration_defaults_and_explicit_values(self):
        params = self.env["ir.config_parameter"].sudo()
        params.set_param("b10_account.invoice_lines_by_origin", "False")
        params.set_param("b10_account.b10_display_payment_term_table", "False")
        invoice = self._invoice()
        self.assertFalse(invoice.group_by_origin)
        self.assertFalse(invoice.b10_display_payment_term_table)

        params.set_param("b10_account.invoice_lines_by_origin", "True")
        params.set_param("b10_account.b10_display_payment_term_table", "True")
        invoice = self._invoice()
        self.assertTrue(invoice.group_by_origin)
        self.assertTrue(invoice.b10_display_payment_term_table)
        invoice = self._invoice(group_by_origin=False, b10_display_payment_term_table=False)
        self.assertFalse(invoice.group_by_origin)
        self.assertFalse(invoice.b10_display_payment_term_table)

    def test_invoice_report_renders(self):
        invoice = self._invoice()
        report = self.env.ref("account.account_invoices")
        html, _ = report._render_qweb_html(report.report_name, invoice.ids)
        self.assertIn(b"Bank transfer customer", html)

    def test_email_templates_render(self):
        invoice = self._invoice()
        for xmlid in (
            "b10_account.factura_email_template",
            "b10_account.pdening_payment_email_template",
        ):
            template = self.env.ref(xmlid)
            body = template._render_field("body_html", invoice.ids)[invoice.id]
            self.assertIn("Bank transfer customer", body)

    def test_variable_bank_transfer_selection_and_validation(self):
        bank = self.env["res.partner.bank"].create({
            "acc_number": "1234567890", "partner_id": self.company.partner_id.id,
            "company_id": self.company.id,
        })
        other_bank = self.env["res.partner.bank"].create({
            "acc_number": "1234567891", "partner_id": self.company.partner_id.id,
            "company_id": self.company.id,
        })
        bank_journal = self.env["account.journal"].create({
            "name": "B10 Bank", "code": "B10B", "type": "bank",
            "company_id": self.company.id, "bank_account_id": bank.id,
        })
        mode = self.env["account.payment.mode"].create({
            "name": "B10 bank transfer", "company_id": self.company.id,
            "payment_method_id": self.env.ref(
                "b10_account.account_payment_method_bank_transfer"
            ).id,
            "bank_account_link": "variable",
            "variable_journal_ids": [Command.set(bank_journal.ids)],
        })
        invoice = self._invoice(payment_mode_id=mode.id)
        self.assertEqual(invoice.partner_bank_id, bank)
        with self.assertRaises(ValidationError):
            invoice.partner_bank_id = other_bank
