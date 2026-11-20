from odoo import Command
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestIntercompanyPurchaseUom(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.source_company = cls.env.company
        cls.destination_company = cls.env["res.company"].create(
            {
                "name": "Intercompany UoM Destination",
                "currency_id": cls.source_company.currency_id.id,
                "po_from_so": True,
                "purchase_auto_validation": False,
            }
        )
        cls.unit = cls.env.ref("uom.product_uom_unit")
        cls.dozen = cls.env.ref("uom.product_uom_dozen")
        cls.product = cls.env["product.product"].create(
            {
                "name": "Intercompany product with purchase dozens",
                "company_id": False,
                "uom_id": cls.unit.id,
                "uom_po_id": cls.dozen.id,
            }
        )

    def _create_sale(self, uom, quantity, price):
        return self.env["sale.order"].create(
            {
                "company_id": self.source_company.id,
                "partner_id": self.destination_company.partner_id.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom": uom.id,
                            "product_uom_qty": quantity,
                            "price_unit": price,
                            "tax_id": [Command.clear()],
                        }
                    )
                ],
            }
        )

    def _assert_purchase_matches_sale(self, sale):
        sale_line = sale.order_line.filtered(lambda line: not line.display_type)
        purchase = sale.auto_purchase_order_id
        purchase_line = purchase.order_line.filtered(lambda line: not line.display_type)
        self.assertEqual(purchase.company_id, self.destination_company)
        self.assertRecordValues(
            purchase_line,
            [
                {
                    "product_uom": sale_line.product_uom.id,
                    "product_qty": sale_line.product_uom_qty,
                    "price_unit": sale_line.price_unit,
                    "price_subtotal": sale_line.price_subtotal,
                    "auto_sale_line_id": sale_line.id,
                }
            ],
        )
        self.assertEqual(sale_line.auto_purchase_line_id, purchase_line)

    def test_sale_units_are_preserved_when_purchase_default_is_dozens(self):
        sale = self._create_sale(self.unit, quantity=12, price=10)

        sale.action_confirm()

        self._assert_purchase_matches_sale(sale)

    def test_sale_dozens_are_preserved_when_purchase_default_is_units(self):
        self.product.uom_po_id = self.unit
        sale = self._create_sale(self.dozen, quantity=2, price=120)

        sale.action_confirm()

        self._assert_purchase_matches_sale(sale)

    def test_matching_sale_and_purchase_units_are_preserved(self):
        sale = self._create_sale(self.dozen, quantity=2, price=120)

        sale.action_confirm()

        self._assert_purchase_matches_sale(sale)

    def test_sections_and_notes_keep_no_unit(self):
        sale = self._create_sale(self.unit, quantity=12, price=10)
        sale.write(
            {
                "order_line": [
                    Command.create({"display_type": "line_section", "name": "Section"}),
                    Command.create({"display_type": "line_note", "name": "Note"}),
                ]
            }
        )

        sale.action_confirm()

        self.assertRecordValues(
            sale.auto_purchase_order_id.order_line.filtered("display_type"),
            [
                {
                    "display_type": "line_section",
                    "name": "Section",
                    "product_uom": False,
                    "product_qty": 0,
                    "price_unit": 0,
                },
                {
                    "display_type": "line_note",
                    "name": "Note",
                    "product_uom": False,
                    "product_qty": 0,
                    "price_unit": 0,
                },
            ],
        )
