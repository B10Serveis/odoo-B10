from odoo import Command
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestIntercompanyOrderRules(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.env.company
        cls.company_b = cls.env["res.company"].create(
            {
                "name": "B10 / OCA Intercompany Destination",
                "currency_id": cls.company_a.currency_id.id,
            }
        )
        (cls.company_a | cls.company_b).write(
            {
                "po_from_so": True,
                "purchase_auto_validation": True,
                "so_from_po": True,
                "sale_auto_validation": True,
                "intercompany_purchase_user_id": cls.env.user.id,
                "intercompany_sale_user_id": cls.env.user.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "B10 / OCA intercompany product",
                "company_id": False,
                "type": "service",
                "list_price": 100,
            }
        )

    def _create_sale(self):
        return self.env["sale.order"].create(
            {
                "company_id": self.company_a.id,
                "partner_id": self.company_b.partner_id.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 2,
                            "price_unit": 100,
                        }
                    )
                ],
            }
        )

    def _create_purchase(self):
        return self.env["purchase.order"].create(
            {
                "company_id": self.company_a.id,
                "partner_id": self.company_b.partner_id.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_qty": 2,
                            "price_unit": 100,
                        }
                    )
                ],
            }
        )

    def _purchase_sale(self, purchase):
        return self.env["sale.order"].search(
            [("auto_purchase_order_id", "=", purchase.id), ("state", "!=", "cancel")]
        )

    def _assert_one_pair(self, sale, purchase):
        self.assertEqual(
            self.env["sale.order"].search(
                [("order_line.product_id", "=", self.product.id)]
            ),
            sale,
        )
        self.assertEqual(
            self.env["purchase.order"].search(
                [("order_line.product_id", "=", self.product.id)]
            ),
            purchase,
        )
        self.assertNotEqual(sale.company_id, purchase.company_id)
        self.assertEqual(sale.auto_purchase_order_id, purchase)
        self.assertEqual(sale.order_line.auto_purchase_line_id, purchase.order_line)

    def test_sale_first_with_auto_validation_creates_one_pair(self):
        sale = self._create_sale()

        sale.action_confirm()

        purchase = sale.auto_purchase_order_id
        self._assert_one_pair(sale, purchase)
        self.assertEqual(purchase.auto_sale_order_id, sale)
        self.assertEqual(purchase.state, "purchase")

    def test_purchase_first_with_auto_validation_creates_one_pair(self):
        purchase = self._create_purchase()

        purchase.button_confirm()

        sale = self._purchase_sale(purchase)
        self._assert_one_pair(sale, purchase)
        self.assertFalse(purchase.auto_sale_order_id)
        self.assertEqual(sale.state, "sale")

    def test_manual_confirmation_of_generated_sale_creates_no_purchase(self):
        self.company_b.sale_auto_validation = False
        purchase = self._create_purchase()
        purchase.button_confirm()
        sale = self._purchase_sale(purchase)
        self.assertEqual(sale.state, "draft")

        sale.action_confirm()

        self._assert_one_pair(sale, purchase)
        self.assertEqual(sale.state, "sale")

    def test_manual_confirmation_of_generated_purchase_creates_no_sale(self):
        self.company_b.purchase_auto_validation = False
        sale = self._create_sale()
        sale.action_confirm()
        purchase = sale.auto_purchase_order_id
        self.assertEqual(purchase.state, "draft")

        purchase.button_confirm()

        self._assert_one_pair(sale, purchase)
        self.assertEqual(purchase.state, "purchase")

    def test_cancel_source_sale_cancels_draft_purchase_without_recursion(self):
        self.company_b.purchase_auto_validation = False
        sale = self._create_sale()
        sale.action_confirm()
        purchase = sale.auto_purchase_order_id

        sale.with_context(disable_cancel_warning=True).action_cancel()

        self.assertEqual(sale.state, "cancel")
        self.assertEqual(purchase.state, "cancel")
        self.assertFalse(sale.auto_purchase_order_id)

    def test_cancel_draft_mirror_purchase_cancels_source_sale(self):
        self.company_b.purchase_auto_validation = False
        sale = self._create_sale()
        sale.action_confirm()
        purchase = sale.auto_purchase_order_id

        purchase.button_cancel()

        self.assertEqual(sale.state, "cancel")
        self.assertEqual(purchase.state, "cancel")
        self.assertFalse(sale.auto_purchase_order_id)

    def test_cancel_confirmed_mirror_purchase_cancels_source_sale(self):
        sale = self._create_sale()
        sale.action_confirm()
        purchase = sale.auto_purchase_order_id

        purchase.button_cancel()

        self.assertEqual(sale.state, "cancel")
        self.assertEqual(purchase.state, "cancel")

    def test_cancel_oca_source_purchase_preserves_generated_sale_origin(self):
        purchase = self._create_purchase()
        purchase.button_confirm()
        sale = self._purchase_sale(purchase)

        purchase.button_cancel()

        self.assertEqual(purchase.state, "cancel")
        self.assertEqual(sale.state, "cancel")
        self.assertEqual(sale.auto_purchase_order_id, purchase)
        self.assertEqual(sale.order_line.auto_purchase_line_id, purchase.order_line)

    def test_cancel_oca_generated_sale_keeps_source_purchase(self):
        purchase = self._create_purchase()
        purchase.button_confirm()
        sale = self._purchase_sale(purchase)

        sale.with_context(disable_cancel_warning=True).action_cancel()

        self.assertEqual(sale.state, "cancel")
        self.assertEqual(purchase.state, "purchase")
        self.assertEqual(sale.auto_purchase_order_id, purchase)

    def test_repeated_oca_generation_reuses_existing_sale(self):
        purchase = self._create_purchase()
        purchase.button_confirm()
        sale = self._purchase_sale(purchase)

        repeated = purchase.with_company(
            self.company_b
        )._inter_company_create_sale_order(self.company_b)

        self.assertEqual(repeated, sale)
        self._assert_one_pair(sale, purchase)

    def test_confirm_batch_of_source_and_generated_sales(self):
        self.company_b.sale_auto_validation = False
        purchase = self._create_purchase()
        purchase.button_confirm()
        generated_sale = self._purchase_sale(purchase)
        source_sale = self._create_sale()

        (source_sale | generated_sale).action_confirm()

        self.assertEqual(generated_sale.auto_purchase_order_id, purchase)
        self.assertEqual(source_sale.auto_purchase_order_id.auto_sale_order_id, source_sale)
        self.assertEqual(
            self.env["purchase.order"].search_count(
                [("order_line.product_id", "=", self.product.id)]
            ),
            2,
        )
        self.assertEqual(
            self.env["sale.order"].search_count(
                [("order_line.product_id", "=", self.product.id)]
            ),
            2,
        )

    def test_cancel_batch_of_source_and_mirror_purchases(self):
        self.company_b.purchase_auto_validation = False
        source_purchase = self._create_purchase()
        source_purchase.button_confirm()
        generated_sale = self._purchase_sale(source_purchase)
        source_sale = self._create_sale()
        source_sale.action_confirm()
        mirror_purchase = source_sale.auto_purchase_order_id

        (source_purchase | mirror_purchase).button_cancel()

        self.assertEqual(source_purchase.state, "cancel")
        self.assertEqual(mirror_purchase.state, "cancel")
        self.assertEqual(source_sale.state, "cancel")
        self.assertEqual(generated_sale.state, "cancel")
        self.assertFalse(source_sale.auto_purchase_order_id)
        self.assertEqual(generated_sale.auto_purchase_order_id, source_purchase)
