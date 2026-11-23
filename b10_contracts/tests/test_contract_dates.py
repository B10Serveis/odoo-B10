from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestContractDates(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "B10 Contract Partner"})

    def _create_contract(self, line_recurrence=False):
        return self.env["contract.contract"].create(
            {
                "name": "B10 Contract",
                "partner_id": self.partner.id,
                "date_start": "2026-01-01",
                "last_date_invoiced": "2026-01-31",
                "line_recurrence": line_recurrence,
            }
        )

    def test_fixed_lines_follow_header_without_erasing_manual_edits(self):
        contract = self._create_contract()
        line = self.env["contract.line"].create(
            {"name": "Service", "contract_id": contract.id, "date_start": "2026-01-01"}
        )
        self.assertEqual(line.last_date_invoiced, fields.Date.to_date("2026-01-31"))

        contract.last_date_invoiced = "2026-02-28"
        self.assertEqual(line.last_date_invoiced, fields.Date.to_date("2026-02-28"))

        line.last_date_invoiced = "2026-02-15"
        contract.name = "Renamed contract"
        self.assertEqual(line.last_date_invoiced, fields.Date.to_date("2026-02-15"))

        contract.last_date_invoiced = False
        self.assertFalse(line.last_date_invoiced)

    def test_line_recurrence_preserves_individual_billing_date(self):
        contract = self._create_contract(line_recurrence=True)
        line = self.env["contract.line"].create(
            {
                "name": "Service",
                "contract_id": contract.id,
                "date_start": "2026-01-01",
                "last_date_invoiced": "2026-01-15",
            }
        )

        contract.last_date_invoiced = "2026-02-28"
        self.assertEqual(line.last_date_invoiced, fields.Date.to_date("2026-01-15"))

    def test_switching_to_contract_recurrence_syncs_billing_date(self):
        contract = self._create_contract(line_recurrence=True)
        line = self.env["contract.line"].create(
            {
                "name": "Service",
                "contract_id": contract.id,
                "date_start": "2026-01-01",
                "last_date_invoiced": "2026-01-15",
            }
        )

        contract.line_recurrence = False
        self.assertEqual(line.last_date_invoiced, fields.Date.to_date("2026-01-31"))

    def test_expiration_tracks_contract_end_date(self):
        contract = self._create_contract()

        contract.date_end = "2026-12-31"
        self.assertEqual(contract.contract_expiration, fields.Date.to_date("2026-12-31"))

        contract.date_end = False
        self.assertFalse(contract.contract_expiration)
