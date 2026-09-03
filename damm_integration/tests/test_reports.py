# Copyright 2026 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.damm_integration.wizards.reports import _report_formats
from odoo.tests import common


class TestDammReports(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # El create() del wizard exige ambos campos en la compañía.
        cls.company = cls.env.company
        cls.company.damm_dealer_code = "TEST"
        cls.company.damm_partner_id = cls.company.partner_id
        cls.partner = cls.env["res.partner"].create(
            {
                "name": 'ASOC. "TEST" [UNO]',
                "street": 'C/"X"\nsegunda línea',
            }
        )

    def test_customers_report_sanitizes_fields(self):
        """Regresión: valores con comillas, corchetes o saltos de línea no
        rompen la generación del CSV (QUOTE_NONE sin escapechar)."""
        wizard = self.env["damm.reports.wizard"].create(
            {
                "report_type": "customers",
                "date_start": "2026-08-01",
                "date_end": "2026-08-31",
            }
        )
        line_data = wizard._format_report_items({self.partner.id: self.partner})
        report_name, report_data = wizard._assemble_report(line_data)

        self.assertEqual(report_name, "Det_TEST_20260801.txt")
        decoded = report_data.decode("utf-8")
        self.assertTrue(decoded)
        self.assertFalse(decoded.endswith("\r\n\r\n"))
        # QUOTE_NONE nunca añade comillas: ninguna debe sobrevivir al saneo.
        self.assertNotIn('"', decoded)
        # Los caracteres problemáticos se sustituyen de forma legible.
        self.assertIn("ASOC. 'TEST' (UNO)", decoded)
        self.assertIn("C/'X' segunda línea", decoded)
        # "[" es el separador de campo: si cada fila se parte en exactamente
        # el número de campos del formato, ningún valor contiene corchetes.
        n_fields = len(_report_formats["customers"])
        for row in decoded.strip("\r\n").split("\r\n"):
            self.assertEqual(len(row.split("[")), n_fields)
