from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestIntercompanyProductCompany(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.destination_company = cls.env["res.company"].create(
            {"name": "Intercompany Destination"}
        )
        cls.other_company = cls.env["res.company"].create(
            {"name": "Intercompany Other"}
        )
        cls.destination_product = cls._create_product(
            "Destination product", cls.destination_company
        )
        cls.other_company_product = cls._create_product(
            "Other company product", cls.other_company
        )
        cls.shared_product = cls._create_product("Shared product", False)

    @classmethod
    def _create_product(cls, name, company):
        template = cls.env["product.template"].create(
            {"name": name, "company_id": company.id if company else False}
        )
        return template.product_variant_id

    def _sale_with_product(self, product):
        return self.env["sale.order"].new(
            {"order_line": [Command.create({"product_id": product.id})]}
        )

    def test_destination_company_product_is_allowed(self):
        sale = self._sale_with_product(self.destination_product)

        sale._check_intercompany_product(self.destination_company)

    def test_shared_product_is_allowed(self):
        sale = self._sale_with_product(self.shared_product)

        sale._check_intercompany_product(self.destination_company)

    def test_product_owned_by_another_company_is_rejected(self):
        sale = self._sale_with_product(self.other_company_product)

        with self.assertRaises(UserError):
            sale._check_intercompany_product(self.destination_company)
