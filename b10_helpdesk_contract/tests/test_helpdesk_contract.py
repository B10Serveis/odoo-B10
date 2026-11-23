from datetime import timedelta

from lxml import etree

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged
from odoo.tools.safe_eval import safe_eval


@tagged("post_install", "-at_install")
class TestHelpdeskContract(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.customer = cls.env["res.partner"].create(
            {"name": "B10 contract customer", "is_company": True}
        )
        cls.contact = cls.env["res.partner"].create(
            {"name": "B10 contract contact", "parent_id": cls.customer.id}
        )
        cls.other_customer = cls.env["res.partner"].create(
            {"name": "Other contract customer"}
        )
        cls.ticket = cls.env["helpdesk.ticket"].create(
            {"name": "B10 contract ticket", "partner_id": cls.contact.id}
        )

    def _create_contract(self, partner=None, **values):
        vals = {
            "name": "B10 contract",
            "partner_id": (partner or self.customer).id,
            "company_id": self.company.id,
        }
        vals.update(values)
        company = self.env["res.company"].browse(vals["company_id"])
        return self.env["contract.contract"].with_company(company).create(vals)

    def test_contract_domain_includes_contracts_ending_today(self):
        today = fields.Date.context_today(self.ticket)
        self.assertEqual(self.ticket.current_date, today)

        valid = self._create_contract(date_end=today)
        open_ended = self._create_contract(date_end=False)
        expired = self._create_contract(date_end=today - timedelta(days=1))
        unrelated = self._create_contract(partner=self.other_customer, date_end=today)

        view = self.env["helpdesk.ticket"].get_view(
            view_id=self.env.ref("helpdesk_mgmt.ticket_view_form").id,
            view_type="form",
        )
        arch = etree.fromstring(view["arch"].encode())
        domain_text = arch.xpath("//field[@name='related_contract']/@domain")[0]
        domain = safe_eval(
            domain_text,
            {
                "partner_id": self.contact.id,
                "commercial_partner_id": self.customer.id,
                "company_id": self.company.id,
                "current_date": today,
            },
        )
        available = self.env["contract.contract"].search(domain)
        self.assertIn(valid, available)
        self.assertIn(open_ended, available)
        self.assertNotIn(expired, available)
        self.assertNotIn(unrelated, available)

    def test_contract_partner_and_company_are_validated(self):
        valid = self._create_contract()
        self.ticket.related_contract = valid

        wrong_partner = self._create_contract(partner=self.other_customer)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.ticket.related_contract = wrong_partner

        other_company = self.env["res.company"].create({"name": "Other B10 company"})
        wrong_company = self._create_contract(company_id=other_company.id)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.ticket.related_contract = wrong_company
