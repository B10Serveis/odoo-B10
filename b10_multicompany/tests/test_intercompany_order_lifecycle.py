from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestIntercompanyOrderLifecycle(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.source_company = cls.env.company
        cls.destination_company = cls.env["res.company"].create(
            {
                "name": "Intercompany Lifecycle Destination",
                "currency_id": cls.source_company.currency_id.id,
                "po_from_so": True,
                "purchase_auto_validation": False,
            }
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Intercompany lifecycle product", "company_id": False}
        )

    def _create_sale(self):
        return self.env["sale.order"].create(
            {
                "company_id": self.source_company.id,
                "partner_id": self.destination_company.partner_id.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "price_unit": 100,
                        }
                    )
                ],
            }
        )

    def test_purchase_creation_is_idempotent(self):
        sale = self._create_sale()
        sale.action_confirm()
        purchase = sale.auto_purchase_order_id

        repeated = sale.with_company(
            self.destination_company
        )._inter_company_create_purchase_order(self.destination_company)

        self.assertEqual(repeated, purchase)
        self.assertEqual(
            self.env["purchase.order"].search([("auto_sale_order_id", "=", sale.id)]),
            purchase,
        )

    def test_sale_cancellation_cancels_draft_purchase(self):
        sale = self._create_sale()
        sale.action_confirm()
        purchase = sale.auto_purchase_order_id

        sale.with_context(disable_cancel_warning=True).action_cancel()

        self.assertEqual(sale.state, "cancel")
        self.assertEqual(purchase.state, "cancel")
        self.assertFalse(sale.auto_purchase_order_id)

    def test_existing_purchase_is_reused_if_forward_link_is_missing(self):
        sale = self._create_sale()
        sale.action_confirm()
        purchase = sale.auto_purchase_order_id
        sale.auto_purchase_order_id = False

        recovered = sale.with_company(
            self.destination_company
        )._inter_company_create_purchase_order(self.destination_company)

        self.assertEqual(recovered, purchase)
        self.assertEqual(sale.auto_purchase_order_id, purchase)
        self.assertEqual(
            self.env["purchase.order"].search([("auto_sale_order_id", "=", sale.id)]),
            purchase,
        )

    def test_cancellation_wizard_does_not_cancel_purchase(self):
        sale = self._create_sale()
        sale.action_confirm()
        purchase = sale.auto_purchase_order_id

        action = sale.action_cancel()

        self.assertEqual(action["res_model"], "sale.order.cancel")
        self.assertEqual(sale.state, "sale")
        self.assertEqual(purchase.state, "draft")
        self.assertEqual(sale.auto_purchase_order_id, purchase)

    def test_confirmed_purchase_still_blocks_sale_cancellation(self):
        sale = self._create_sale()
        sale.action_confirm()
        purchase = sale.auto_purchase_order_id
        purchase.button_confirm()

        with self.assertRaises(UserError):
            sale.with_context(disable_cancel_warning=True).action_cancel()

        self.assertEqual(sale.state, "sale")
        self.assertEqual(purchase.state, "purchase")
        self.assertEqual(sale.auto_purchase_order_id, purchase)

    def test_reconfirmation_creates_new_purchase_after_cancellation(self):
        sale = self._create_sale()
        sale.action_confirm()
        previous_purchase = sale.auto_purchase_order_id
        sale.with_context(disable_cancel_warning=True).action_cancel()

        sale.action_draft()
        sale.action_confirm()

        self.assertEqual(previous_purchase.state, "cancel")
        self.assertNotEqual(sale.auto_purchase_order_id, previous_purchase)
        self.assertEqual(sale.auto_purchase_order_id.state, "draft")
