from odoo import Command
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestIntercompanyPurchaseDiscount(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.source_company = cls.env.company
        cls.destination_company = cls.env["res.company"].create(
            {
                "name": "Intercompany Discount Destination",
                "currency_id": cls.source_company.currency_id.id,
                "po_from_so": True,
                "purchase_auto_validation": False,
            }
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Intercompany discounted product", "company_id": False}
        )

    def _confirm_sale(self, discount, supplier_discount=None, auto_validate=False):
        self.destination_company.purchase_auto_validation = auto_validate
        if supplier_discount is not None:
            self.env["product.supplierinfo"].create(
                {
                    "partner_id": self.source_company.partner_id.id,
                    "product_tmpl_id": self.product.product_tmpl_id.id,
                    "company_id": self.destination_company.id,
                    "currency_id": self.source_company.currency_id.id,
                    "price": 250,
                    "discount": supplier_discount,
                }
            )
        sale = self.env["sale.order"].create(
            {
                "company_id": self.source_company.id,
                "partner_id": self.destination_company.partner_id.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 2,
                            "price_unit": 100,
                            "discount": discount,
                            "tax_id": [Command.clear()],
                        }
                    )
                ],
            }
        )
        sale.action_confirm()
        return sale

    def _assert_purchase_discount(self, sale, discount):
        self.assertEqual(sale.order_line.discount, discount)
        self.assertRecordValues(
            sale.auto_purchase_order_id.order_line,
            [
                {
                    "product_qty": 2,
                    "price_unit": 100,
                    "discount": discount,
                    "price_subtotal": 200 * (1 - discount / 100),
                }
            ],
        )
        self.assertEqual(
            sale.auto_purchase_order_id.amount_untaxed, sale.amount_untaxed
        )

    def test_fractional_sale_discount_is_copied(self):
        sale = self._confirm_sale(discount=12.5)

        self._assert_purchase_discount(sale, 12.5)

    def test_sale_discount_overrides_supplier_discount(self):
        sale = self._confirm_sale(discount=10, supplier_discount=25)

        self._assert_purchase_discount(sale, 10)

    def test_zero_sale_discount_overrides_supplier_discount(self):
        sale = self._confirm_sale(discount=0, supplier_discount=25)

        self._assert_purchase_discount(sale, 0)

    def test_full_discount_keeps_zero_subtotal(self):
        sale = self._confirm_sale(discount=100)

        self._assert_purchase_discount(sale, 100)

    def test_auto_validated_purchase_keeps_sale_discount(self):
        sale = self._confirm_sale(
            discount=10, supplier_discount=25, auto_validate=True
        )

        self.assertEqual(sale.auto_purchase_order_id.state, "purchase")
        self._assert_purchase_discount(sale, 10)
