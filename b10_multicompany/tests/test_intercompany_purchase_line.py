from odoo import Command, fields
from odoo.tests import TransactionCase, tagged
from odoo.tests.common import new_test_user


@tagged("post_install", "-at_install")
class TestIntercompanyPurchaseLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.source_company = cls.env.company
        cls.destination_company = cls.env["res.company"].create(
            {"name": "Intercompany Purchase Line Destination"}
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Intercompany shared product", "company_id": False}
        )
        cls.sale = cls.env["sale.order"].create(
            {
                "company_id": cls.source_company.id,
                "partner_id": cls.destination_company.partner_id.id,
                "order_line": [
                    Command.create({"product_id": cls.product.id}),
                    Command.create({"product_id": cls.product.id}),
                ],
            }
        )
        cls.linked_line, cls.unlinked_line = cls.sale.order_line
        cls.purchase = cls.env["purchase.order"].with_company(
            cls.destination_company
        ).create(
            {
                "company_id": cls.destination_company.id,
                "partner_id": cls.source_company.partner_id.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "name": cls.product.name,
                            "product_uom_id": cls.product.uom_id.id,
                            "product_qty": 1,
                            "price_unit": 10,
                            "date_planned": fields.Datetime.now(),
                            "auto_sale_line_id": cls.linked_line.id,
                        }
                    )
                ],
            }
        )
        cls.purchase_line = cls.purchase.order_line

    def test_purchase_line_is_found_from_source_sale_line(self):
        self.assertFalse(self.linked_line.auto_purchase_line_id)
        self.assertEqual(
            self.linked_line.intercompany_purchase_line_id, self.purchase_line
        )

    def test_unlinked_sale_line_has_no_purchase_line(self):
        self.assertFalse(self.unlinked_line.intercompany_purchase_line_id)

    def test_multiple_sale_lines_are_computed_together(self):
        values = self.sale.order_line.read(["intercompany_purchase_line_id"])
        purchase_ids = {
            value["id"]: value["intercompany_purchase_line_id"][0]
            if value["intercompany_purchase_line_id"]
            else False
            for value in values
        }
        self.assertEqual(
            purchase_ids,
            {self.linked_line.id: self.purchase_line.id, self.unlinked_line.id: False},
        )

    def test_purchase_line_is_found_for_sales_user_in_source_company(self):
        user = new_test_user(
            self.env,
            login="intercompany_source_sales_user",
            groups="sales_team.group_sale_salesman_all_leads",
            context={"no_reset_password": True},
            company_id=self.source_company.id,
            company_ids=[Command.set(self.source_company.ids)],
        )
        self.assertFalse(
            self.env["purchase.order.line"].with_user(user).has_access("read")
        )
        line = self.linked_line.with_user(user).with_context(
            allowed_company_ids=self.source_company.ids
        )
        self.assertEqual(line.intercompany_purchase_line_id.id, self.purchase_line.id)

    def test_new_sale_line_has_no_purchase_line(self):
        line = self.env["sale.order.line"].new(
            {"order_id": self.sale.id, "product_id": self.product.id}
        )
        self.assertFalse(line.intercompany_purchase_line_id)
