from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestStateOriginalName(TransactionCase):
    def test_spanish_state_original_names_loaded(self):
        self.assertEqual(self.env.ref("base.state_es_a").original_name, "Alacant")
        self.assertEqual(self.env.ref("base.state_es_cs").original_name, "Castelló")
        self.assertEqual(self.env.ref("base.state_es_pm").original_name, "Illes Balears")

    def test_only_administrators_can_create_states_in_batch(self):
        country = self.env.ref("base.es")
        vals_list = [
            {"name": "Test state one", "code": "B10T1", "country_id": country.id},
            {"name": "Test state two", "code": "B10T2", "country_id": country.id},
        ]

        manager = new_test_user(
            self.env,
            login="b10_contacts_manager",
            groups="base.group_user,base.group_partner_manager",
            context={"no_reset_password": True},
        )
        with self.assertRaisesRegex(AccessError, "Only administrators can create states"):
            self.env["res.country.state"].with_user(manager).create(vals_list)

        states = self.env["res.country.state"].with_user(
            self.env.ref("base.user_admin")
        ).create(vals_list)
        self.assertEqual(len(states), 2)
        self.assertEqual(set(states.mapped("code")), {"B10T1", "B10T2"})
