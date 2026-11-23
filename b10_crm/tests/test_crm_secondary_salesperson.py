from lxml import etree
from psycopg2.errors import CheckViolation

from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestCrmSecondarySalesperson(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.primary_user = cls.env.ref("base.user_admin")
        cls.secondary_user = cls.env.ref("base.user_root")

    def test_secondary_salesperson_must_differ_from_primary(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "Lead with two salespeople",
                "user_id": self.primary_user.id,
                "secondary_user_id": self.secondary_user.id,
            }
        )
        self.assertEqual(lead.secondary_user_id, self.secondary_user)

        with self.assertRaises(CheckViolation), mute_logger("odoo.sql_db"):
            with self.env.cr.savepoint():
                lead.secondary_user_id = self.primary_user

        with self.assertRaises(CheckViolation), mute_logger("odoo.sql_db"):
            with self.env.cr.savepoint():
                self.env["crm.lead"].create(
                    {
                        "name": "Lead with duplicate salesperson",
                        "user_id": self.primary_user.id,
                        "secondary_user_id": self.primary_user.id,
                    }
                )

    def test_secondary_salesperson_appears_on_leads_and_opportunities(self):
        view = self.env["crm.lead"].get_view(
            view_id=self.env.ref("crm.crm_lead_view_form").id,
            view_type="form",
        )
        arch = etree.fromstring(view["arch"].encode())
        for hidden_type in ("lead", "opportunity"):
            field = arch.xpath(
                "//form/sheet/group/group[@invisible=$invisible]"
                "/field[@name='user_id']/following-sibling::*[1]"
                "[self::field[@name='secondary_user_id']]",
                invisible=f"type == '{hidden_type}'",
            )
            self.assertEqual(len(field), 1)
