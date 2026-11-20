# Copyright (C) 2026 Batista10 (https://www.batista10.cat/).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestSubscription(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.groups_id |= cls.env.ref("analytic.group_analytic_accounting")
        cls.product_a.write(
            {
                "type": "service",
                "invoice_policy": "order",
                "taxes_id": [Command.clear()],
            }
        )
        cls.template = cls.env["sale.subscription.template"].create(
            {"name": "Monthly subscription"}
        )
        cls.payment_mode = cls.env["account.payment.mode"].create(
            {
                "name": "Subscription payment",
                "bank_account_link": "variable",
                "payment_method_id": cls.env.ref(
                    "account.account_payment_method_manual_in"
                ).id,
            }
        )
        cls.plan = cls.env["account.analytic.plan"].create({"name": "Subscriptions"})
        cls.analytic_a, cls.analytic_b = cls.env["account.analytic.account"].create(
            [
                {"name": name, "plan_id": cls.plan.id}
                for name in ("Subscription A", "Subscription B")
            ]
        )
        cls.distribution_a = {str(cls.analytic_a.id): 100.0}
        cls.distribution_b = {str(cls.analytic_b.id): 100.0}
        cls.subscription = cls.env["sale.subscription"].create(
            {
                "partner_id": cls.partner_a.id,
                "template_id": cls.template.id,
                "pricelist_id": cls.pricelist.id,
                "payment_mode_id": cls.payment_mode.id,
                "journal_id": cls.company_data["default_journal_sale"].id,
            }
        )

    def _add_lines(self):
        # Create out of sequence, including duplicate products with distinct analytics.
        self.subscription.sale_subscription_line_ids = [
            Command.create(
                {
                    "product_id": self.product_a.id,
                    "name": "Second product",
                    "price_unit": 40,
                    "sequence": 30,
                    "analytic_distribution": self.distribution_b,
                }
            ),
            Command.create(
                {"display_type": "line_note", "name": "A note", "sequence": 40}
            ),
            Command.create(
                {"display_type": "line_section", "name": "A section", "sequence": 10}
            ),
            Command.create(
                {
                    "product_id": self.product_a.id,
                    "name": "First product",
                    "price_unit": 60,
                    "sequence": 20,
                    "analytic_distribution": self.distribution_a,
                }
            ),
        ]

    def _assert_document_lines(self, lines, invoice=False):
        self.assertEqual(
            # Odoo may prefix invoice descriptions with the product name.
            [line.name.splitlines()[-1] for line in lines],
            ["A section", "First product", "Second product", "A note"],
        )
        # Sale invoicing renumbers sequences while preserving the line order.
        self.assertEqual(lines.mapped("sequence"), sorted(lines.mapped("sequence")))
        self.assertEqual(lines[0].display_type, "line_section")
        self.assertEqual(lines[3].display_type, "line_note")
        product_lines = lines.filtered(
            lambda line: line.display_type == ("product" if invoice else False)
        )
        self.assertEqual(len(product_lines), 2)
        self.assertEqual(product_lines[0].analytic_distribution, self.distribution_a)
        self.assertEqual(product_lines[1].analytic_distribution, self.distribution_b)
        self.assertAlmostEqual(sum(lines.mapped("price_subtotal")), 100)

    def test_sections_and_notes_in_form(self):
        with Form(self.subscription) as subscription:
            with subscription.sale_subscription_line_ids.new() as line:
                line.display_type = "line_section"
                line.name = "Support"
            with subscription.sale_subscription_line_ids.new() as line:
                line.product_id = self.product_a
            with subscription.sale_subscription_line_ids.new() as line:
                line.display_type = "line_note"
                line.name = "Monthly service"
        display_lines = self.subscription.sale_subscription_line_ids.filtered(
            "display_type"
        )
        self.assertEqual(display_lines.mapped("name"), ["Support", "Monthly service"])
        self.assertFalse(display_lines.product_id)
        self.assertFalse(display_lines.tax_ids)
        for line in display_lines:
            self.assertEqual(line.price_unit, 0)
            self.assertEqual(line.discount, 0)
            self.assertEqual(line.price_subtotal, 0)
            self.assertEqual(line.price_total, 0)
            self.assertEqual(line.amount_tax_line_amount, 0)

    def test_product_distribution_models(self):
        account = self.product_a.property_account_income_id
        self.env["account.analytic.distribution.model"].create(
            [
                {
                    "product_id": self.product_a.id,
                    "account_prefix": account.code,
                    "analytic_distribution": self.distribution_a,
                },
                {
                    "product_id": self.product_a.id,
                    "account_prefix": "EXPENSE-ONLY",
                    "analytic_distribution": self.distribution_b,
                },
            ]
        )
        with Form(self.subscription) as subscription:
            with subscription.sale_subscription_line_ids.new() as line:
                line.product_id = self.product_a
                self.assertEqual(line.analytic_distribution, self.distribution_a)
                line.analytic_distribution = self.distribution_b
        self.assertEqual(
            self.subscription.sale_subscription_line_ids.analytic_distribution,
            self.distribution_b,
        )

    def test_category_distribution_model(self):
        self.env["account.analytic.distribution.model"].create(
            {
                "product_categ_id": self.product_a.categ_id.id,
                "analytic_distribution": self.distribution_a,
            }
        )
        with Form(self.subscription) as subscription:
            with subscription.sale_subscription_line_ids.new() as line:
                line.product_id = self.product_a
                self.assertEqual(line.analytic_distribution, self.distribution_a)

    def test_direct_invoice(self):
        self._add_lines()
        invoice = self.subscription.create_invoice()
        self.assertEqual(invoice.payment_mode_id, self.payment_mode)
        self._assert_document_lines(invoice.invoice_line_ids, invoice=True)
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")

    def test_recurring_sale_and_invoice(self):
        self._add_lines()
        # These rules would replace both manually entered distributions on the order.
        self.env["account.analytic.distribution.model"].create(
            {
                "product_id": self.product_a.id,
                "analytic_distribution": self.distribution_b,
            }
        )
        order = self.subscription.create_sale_order()
        self.assertEqual(order.payment_mode_id, self.payment_mode)
        self._assert_document_lines(order.order_line)
        order.action_confirm()
        invoice = order._create_invoices()
        self.assertEqual(invoice.payment_mode_id, self.payment_mode)
        self._assert_document_lines(invoice.invoice_line_ids, invoice=True)
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")

    def test_empty_distribution_overrides_order_rules(self):
        self._add_lines()
        self.subscription.sale_subscription_line_ids.analytic_distribution = False
        self.env["account.analytic.distribution.model"].create(
            {
                "product_id": self.product_a.id,
                "analytic_distribution": self.distribution_a,
            }
        )
        order = self.subscription.create_sale_order()
        for line in order.order_line:
            self.assertFalse(line.analytic_distribution)

    def test_empty_payment_mode_overrides_partner_default(self):
        self._add_lines()
        self.partner_a.customer_payment_mode_id = self.payment_mode
        self.subscription.payment_mode_id = False
        self.assertFalse(self.subscription.create_invoice().payment_mode_id)
        order = self.subscription.create_sale_order()
        self.assertFalse(order.payment_mode_id)
        order.action_confirm()
        self.assertFalse(order._create_invoices().payment_mode_id)
