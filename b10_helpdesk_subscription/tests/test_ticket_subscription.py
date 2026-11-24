from datetime import timedelta

from lxml import etree

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged
from odoo.tools.safe_eval import safe_eval


@tagged("post_install", "-at_install")
class TestTicketSubscription(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {"name": "Subscription customer", "email": "customer@example.com"}
        )
        cls.other_partner = cls.env["res.partner"].create(
            {"name": "Other customer", "email": "other@example.com"}
        )
        cls.company = cls.env.company
        cls.other_company = cls.env["res.company"].create(
            {"name": "Other subscription company"}
        )
        cls.template = cls.env["sale.subscription.template"].create(
            {
                "name": "One day subscription",
                "recurring_rule_boundary": "limited",
                "recurring_rule_type": "days",
                "recurring_rule_count": 1,
                "recurring_interval": 1,
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {"name": "Subscription test pricelist"}
        )
        cls.today = fields.Date.context_today(cls.env["helpdesk.ticket"])
        cls.subscription = cls._create_subscription(
            cls.partner, cls.company, cls.today - timedelta(days=1)
        )

    @classmethod
    def _create_subscription(cls, partner, company, start_date):
        return cls.env["sale.subscription"].sudo().create(
            {
                "partner_id": partner.id,
                "company_id": company.id,
                "template_id": cls.template.id,
                "pricelist_id": cls.pricelist.id,
                "date_start": start_date,
            }
        )

    def test_form_domain_includes_subscription_expiring_today(self):
        view = self.env["helpdesk.ticket"].get_view(
            view_id=self.env.ref("helpdesk_mgmt.ticket_view_form").id,
            view_type="form",
        )
        arch = etree.fromstring(view["arch"].encode())
        field = arch.xpath("//field[@name='related_subscription']")
        self.assertEqual(len(field), 1)
        domain = safe_eval(
            field[0].get("domain"),
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "subscription_current_date": self.today,
            },
        )
        self.assertIn(self.subscription, self.env["sale.subscription"].search(domain))
        expired = self._create_subscription(
            self.partner, self.company, self.today - timedelta(days=2)
        )
        self.assertNotIn(expired, self.env["sale.subscription"].search(domain))

    def test_subscription_must_match_customer_and_company(self):
        self.env["helpdesk.ticket"].create(
            {
                "name": "Valid subscription ticket",
                "description": "Valid subscription ticket",
                "partner_id": self.partner.id,
                "related_subscription": self.subscription.id,
            }
        )
        other_company_subscription = self._create_subscription(
            self.partner, self.other_company, self.today - timedelta(days=1)
        )
        for values in (
            {"partner_id": self.other_partner.id},
            {"related_subscription": other_company_subscription.id},
        ):
            with self.assertRaises(ValidationError), self.cr.savepoint():
                self.env["helpdesk.ticket"].create(
                    {
                        "name": "Invalid subscription ticket",
                        "description": "Invalid subscription ticket",
                        "partner_id": self.partner.id,
                        "related_subscription": self.subscription.id,
                        **values,
                    }
                )

    def test_partner_onchange_clears_subscription_and_updates_contact(self):
        ticket = self.env["helpdesk.ticket"].new(
            {
                "name": "Changed customer",
                "partner_id": self.other_partner.id,
                "related_subscription": self.subscription.id,
            }
        )
        ticket._onchange_partner_id()
        self.assertFalse(ticket.related_subscription)
        self.assertEqual(ticket.partner_name, self.other_partner.name)
        self.assertEqual(ticket.partner_email, self.other_partner.email)

    def test_company_onchange_clears_subscription(self):
        ticket = self.env["helpdesk.ticket"].new(
            {
                "name": "Changed company",
                "partner_id": self.partner.id,
                "company_id": self.other_company.id,
                "related_subscription": self.subscription.id,
            }
        )
        ticket._onchange_subscription_company()
        self.assertFalse(ticket.related_subscription)
