from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAnonymousCustomer(TransactionCase):
    def test_creation_marks_only_individuals_without_vat(self):
        individual, with_vat, company, already_anonymous = self.env[
            "res.partner"
        ].create(
            [
                {"name": "Individual without VAT"},
                {"name": "Individual with VAT", "vat": "BE0477472701"},
                {"name": "Company without VAT", "is_company": True},
                {"name": "Already anonymous", "aeat_anonymous_cash_customer": True},
            ]
        )
        self.assertTrue(individual.aeat_anonymous_cash_customer)
        self.assertFalse(with_vat.aeat_anonymous_cash_customer)
        self.assertFalse(company.aeat_anonymous_cash_customer)
        self.assertTrue(already_anonymous.aeat_anonymous_cash_customer)

    def test_update_marks_company_changed_to_individual(self):
        partner = self.env["res.partner"].create(
            {"name": "Company", "is_company": True}
        )
        partner.is_company = False
        self.assertTrue(partner.aeat_anonymous_cash_customer)

    def test_batch_update_checks_conditions(self):
        individual, company = self.env["res.partner"].create(
            [
                {"name": "Individual with VAT", "vat": "BE0477472701"},
                {
                    "name": "Company with VAT",
                    "vat": "BE0477472701",
                    "is_company": True,
                },
            ]
        )
        (individual | company).write({"vat": False})
        self.assertTrue(individual.aeat_anonymous_cash_customer)
        self.assertFalse(company.aeat_anonymous_cash_customer)

    def test_update_of_marked_contact(self):
        partner = self.env["res.partner"].create({"name": "Individual"})
        partner.name = "Updated individual"
        self.assertTrue(partner.aeat_anonymous_cash_customer)
        partner.write({"vat": "BE0477472701", "is_company": True})
        self.assertFalse(partner.aeat_anonymous_cash_customer)

    def test_creation_unmarks_individuals_and_companies_with_vat(self):
        partners = self.env["res.partner"].create(
            [
                {
                    "name": "Identified individual",
                    "vat": "BE0477472701",
                    "aeat_anonymous_cash_customer": True,
                },
                {
                    "name": "Identified company",
                    "vat": "BE0477472701",
                    "is_company": True,
                    "aeat_anonymous_cash_customer": True,
                },
            ]
        )
        self.assertFalse(any(partners.mapped("aeat_anonymous_cash_customer")))

    def test_batch_update_unmarks_with_vat_and_remarks_without_vat(self):
        individual, company = self.env["res.partner"].create(
            [
                {"name": "Individual without VAT"},
                {
                    "name": "Anonymous company without VAT",
                    "is_company": True,
                    "aeat_anonymous_cash_customer": True,
                },
            ]
        )
        partners = individual | company
        self.assertTrue(all(partners.mapped("aeat_anonymous_cash_customer")))
        partners.write({"vat": "BE0477472701"})
        self.assertFalse(any(partners.mapped("aeat_anonymous_cash_customer")))
        # Further edits keep the mark off, and removing VAT marks only individuals.
        partners.write({"comment": "Updated identified contact"})
        self.assertFalse(any(partners.mapped("aeat_anonymous_cash_customer")))
        partners.write({"vat": False})
        self.assertTrue(individual.aeat_anonymous_cash_customer)
        self.assertFalse(company.aeat_anonymous_cash_customer)

    def test_automated_action(self):
        for suffix in ("anonymous_customers", "identified_customers"):
            with self.subTest(automation=suffix):
                automation = self.env.ref(f"b10_website.automation_{suffix}")
                self.assertTrue(automation.active)
                self.assertEqual(automation.trigger, "on_create_or_write")
                self.assertEqual(automation.model_id.model, "res.partner")
                self.assertEqual(
                    automation.action_server_ids,
                    self.env.ref(f"b10_website.action_{suffix}"),
                )
