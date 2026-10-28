# Copyright 2026 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo import Command
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestDammReports(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.groups_id += cls.env.ref(
            "damm_integration.res_groups_damm_integration"
        )
        cls.damm = cls.env["res.partner"].create({"name": "S.A. Damm"})
        cls.env.company.write({
            "damm_dealer_code": "12345",
            "damm_partner_id": cls.damm.id,
        })
        cls.product_a.default_code = "DAMM001"
        cls.env["product.supplierinfo"].create({
            "partner_id": cls.damm.id,
            "product_tmpl_id": cls.product_a.product_tmpl_id.id,
        })
        cls.wizard = cls.env["damm.reports.wizard"].create({
            "date_start": "2026-01-01",
            "date_end": "2026-01-31",
        })

    def _invoice(self, partner=None, move_type="out_invoice", company=None):
        company = company or self.env.company
        account = (
            self.company_data_2 if company == self.company_data_2["company"]
            else self.company_data
        )["default_account_revenue"]
        move = self.env["account.move"].with_company(company).create({
            "move_type": move_type,
            "partner_id": (partner or self.partner_a).id,
            "invoice_date": "2026-01-15",
            "date": "2026-01-15",
            "invoice_line_ids": [Command.create({
                "product_id": self.product_a.id,
                "account_id": account.id,
                "quantity": 2,
                "price_unit": 10,
                "discount": 10,
                "tax_ids": [Command.clear()],
            }), Command.create({
                "display_type": "line_note", "name": "Ignored note",
            })],
        })
        move.action_post()
        return move

    def test_sales_and_refunds(self):
        invoice = self._invoice()
        refund = self._invoice(move_type="out_refund")
        # A product from another supplier must not be included.
        other = self._invoice()
        other.button_draft()
        other.invoice_line_ids.filtered("product_id").product_id = self.product_b
        other.action_post()
        items = self.wizard._search_report_items()
        self.assertEqual(
            set(items),
            set((invoice + refund).invoice_line_ids.filtered("product_id").ids),
        )
        lines = self.wizard._format_report_items(items)
        by_number = {line["Nº Documento"].strip(): line for line in lines}
        for move, sign in [(invoice, 1), (refund, -1)]:
            line = by_number[move.name]
            self.assertEqual(int(line["Cantidad"]), sign * 200000)
            self.assertEqual(int(line["Importe albarán"]), sign * 20000)
            self.assertEqual(int(line["Importe Dto"]), sign * 2000)
        action = self.wizard.generate_report()
        self.assertIn("/web/content?", action["url"])
        self.assertEqual(self.wizard.report_name, "12345_VENTAS_Factura_202601.txt")
        data = base64.b64decode(self.wizard.report_data).decode()
        self.assertEqual(len(data.splitlines()), 2)
        self.assertTrue(all(len(line) == 280 for line in data.splitlines()))

    def test_invoice_contact_matches_customer_report(self):
        self.partner_a.comercial = "Establishment"
        contact = self.env["res.partner"].create({
            "name": "Damm establishment", "parent_id": self.partner_a.id,
            "type": "invoice",
        })
        invoice = self._invoice(partner=contact)
        line = invoice.invoice_line_ids.filtered("product_id")
        self.assertEqual(line.partner_id, self.partner_a)
        sales = self.wizard._format_report_items(self.wizard._search_report_items())
        self.assertEqual(sales[0]["Nº Cliente"].strip(), str(contact.id))
        self.wizard.report_type = "customers"
        customers = self.wizard._format_report_items(self.wizard._search_report_items())
        self.assertEqual(customers[0]["cod_Detallista"], str(contact.id))
        self.assertEqual(customers[0]["Nombre"], "Establishment")
        self.wizard.generate_report()
        self.assertTrue(self.wizard.report_name.startswith("Det_12345_"))

    def test_report_uses_current_company(self):
        invoice = self._invoice()
        self._invoice(company=self.company_data_2["company"])
        self.assertEqual(
            set(self.wizard._search_report_items()),
            set(invoice.invoice_line_ids.filtered("product_id").ids),
        )

    def test_conditions_keep_customers_with_same_pricelist(self):
        pricelists = self.env["product.pricelist"].create([
            {"name": "Damm A"}, {"name": "Damm B"},
        ])
        for pricelist in pricelists:
            self.env["product.pricelist.item"].create({
                "pricelist_id": pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "compute_price": "percentage", "percent_price": 10,
            })
        customers = self.env["res.partner"].create([
            {"name": "Establishment %s" % index,
             "property_product_pricelist": pricelists[index % 2].id}
            for index in range(3)
        ])
        for customer in customers:
            self._invoice(partner=customer)
        self.wizard.report_type = "conditions"
        items = self.wizard._search_report_items()
        self.assertEqual(len(items), 3)
        lines = self.wizard._format_report_items(items)
        self.assertEqual({line["cod_detallista"] for line in lines}, set(map(str, customers.ids)))
        self.assertTrue(all(line["Descuento_M"] == "10" for line in lines))
        self.wizard.generate_report()
        self.assertTrue(self.wizard.report_name.startswith("CondCiales_12345_"))

    def test_validation_and_batch_create(self):
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.wizard.date_end = "2025-12-31"
        with self.assertRaises(UserError):
            self.wizard.generate_report()
        wizards = self.env["damm.reports.wizard"].create([{}, {}])
        self.assertEqual(len(wizards), 2)
        self.env.company.damm_dealer_code = False
        with self.assertRaises(UserError):
            self.env["damm.reports.wizard"].create({})
