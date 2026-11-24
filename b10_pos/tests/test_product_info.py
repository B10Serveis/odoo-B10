from datetime import timedelta

from odoo import Command, fields
from odoo.addons.point_of_sale.tests.common import TestPointOfSaleCommon
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestProductInfo(TestPointOfSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_company = cls.company_data_2["company"]
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                allowed_company_ids=(cls.company | cls.other_company).ids,
            )
        )
        cls.tax = cls.env["account.tax"].create(
            {
                "name": "POS company tax",
                "amount": 10,
                "company_id": cls.company.id,
                "price_include_override": "tax_excluded",
            }
        )
        cls.other_tax = cls.env["account.tax"].with_company(cls.other_company).create(
            {
                "name": "Other company tax",
                "amount": 21,
                "company_id": cls.other_company.id,
                "price_include_override": "tax_excluded",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "POS information test",
                "is_storable": True,
                "list_price": 100,
                "taxes_id": [Command.set((cls.tax | cls.other_tax).ids)],
            }
        )

    def test_taxes_use_pos_company(self):
        info = (
            self.product.product_tmpl_id.with_company(self.other_company)
            .get_product_info_pos(100, 2, self.pos_config.id)
        )
        self.assertAlmostEqual(info["all_prices"]["price_without_tax"], 100)
        self.assertAlmostEqual(info["all_prices"]["price_with_tax"], 110)
        self.assertEqual(
            info["all_prices"]["tax_details"],
            [{"name": self.tax.name, "amount": 10}],
        )

    def test_parent_company_taxes(self):
        branch = self.env["res.company"].create(
            {"name": "POS branch", "parent_id": self.company.id}
        )
        config = self.env["pos.config"].with_company(branch).create(
            {
                "name": "Branch POS",
                "company_id": branch.id,
                "payment_method_ids": [Command.clear()],
            }
        )
        info = self.product.product_tmpl_id.get_product_info_pos(100, 1, config.id)
        self.assertAlmostEqual(info["all_prices"]["price_with_tax"], 110)
        self.assertEqual(info["all_prices"]["tax_details"][0]["name"], self.tax.name)

    def test_dated_suppliers_and_pricelist_ids(self):
        today = fields.Date.today()
        sellers = self.env["product.supplierinfo"].create([
            {
                "partner_id": self.env["res.partner"].create({"name": name}).id,
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "date_start": today + timedelta(days=start),
                "date_end": today + timedelta(days=end),
                "min_qty": min_qty,
                "price": 50,
            }
            for name, start, end, min_qty in [
                ("Valid supplier A", -1, 1, 1),
                ("Valid supplier B", -1, 1, 1),
                ("Expired supplier", -3, -1, 1),
                ("Future supplier", 1, 3, 1),
                ("Bulk supplier", -1, 1, 10),
            ]
        ])
        pricelists = self.env["product.pricelist"].create([
            {
                "name": "POS price %s" % price,
                "currency_id": self.company.currency_id.id,
                "item_ids": [Command.create({
                    "applied_on": "1_product",
                    "product_tmpl_id": self.product.product_tmpl_id.id,
                    "compute_price": "fixed",
                    "fixed_price": price,
                })],
            }
            for price in (80, 90)
        ])
        self.pos_config.write({
            "use_pricelist": True,
            "available_pricelist_ids": [Command.set(pricelists.ids)],
            "pricelist_id": pricelists[0].id,
        })
        info = self.product.product_tmpl_id.get_product_info_pos(
            100, 2, self.pos_config.id
        )
        self.assertEqual(
            {supplier["id"] for supplier in info["suppliers"]}, set(sellers[:2].ids)
        )
        self.assertEqual(
            {row["id"]: row["price"] for row in info["pricelists"]},
            dict(zip(pricelists.ids, (80, 90))),
        )

    def test_stock_locations_company_order_and_quantities(self):
        source = self.pos_config.picking_type_id.default_location_src_id
        self.assertTrue(source)
        other_location = self.company_data_2["default_warehouse"].lot_stock_id
        shared_location = self.env["stock.location"].create(
            {"name": "Shared POS stock", "usage": "internal", "company_id": False}
        )
        # Use another warehouse to check that an inherited context does not
        # restrict the stock calculation to that warehouse.
        warehouse = self.env["stock.warehouse"].create(
            {
                "name": "Secondary POS warehouse",
                "code": "B10T",
                "company_id": self.company.id,
            }
        )
        for location, quantity in ((source, 7), (warehouse.lot_stock_id, 3)):
            self.env["stock.quant"]._update_available_quantity(
                self.product, location, quantity
            )
        info = (
            self.product.product_tmpl_id.with_context(warehouse_id=warehouse.id)
            .get_product_info_pos(100, 1, self.pos_config.id)
        )
        rows = {row["id"]: row for row in info["warehouses"]}
        self.assertEqual(info["warehouses"][0]["id"], source.id)
        self.assertNotIn(other_location.id, rows)
        self.assertIn(shared_location.id, rows)
        for location, quantity in ((source, 7), (warehouse.lot_stock_id, 3)):
            self.assertEqual(rows[location.id]["name"], location.complete_name)
            self.assertAlmostEqual(rows[location.id]["available_quantity"], quantity)
            self.assertAlmostEqual(rows[location.id]["forecasted_quantity"], quantity)
