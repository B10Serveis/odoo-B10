from lxml import etree, html

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHelpdeskTicket(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ticket = cls.env["helpdesk.ticket"].create(
            {
                "name": "B10 report test ticket",
                "description": "<p>B10 test description</p>",
            }
        )

    def test_ticket_form_fields(self):
        view = self.env["helpdesk.ticket"].get_view(
            view_id=self.env.ref("helpdesk_mgmt.ticket_view_form").id,
            view_type="form",
        )
        arch = etree.fromstring(view["arch"].encode())
        self.assertEqual(len(arch.xpath("//page[@name='internal_note']/field[@name='internal_note']")), 1)
        self.assertEqual(len(arch.xpath("//page[@name='close_note']/field[@name='close_note']")), 1)
        self.assertEqual(
            arch.xpath("//field[@name='worked_hours']/@required"),
            ["stage_closed == 1"],
        )

    def test_report_renders_ticket_and_omits_empty_closing_note(self):
        report = self.env.ref("b10_helpdesk.action_helpdesk_ticket_report_B10")
        rendered, _ = report._render_qweb_html(report.report_name, self.ticket.ids)
        document = html.fromstring(rendered)

        self.assertIn("B10 report test ticket", document.text_content())
        self.assertIn("B10 test description", document.text_content())
        self.assertEqual(document.xpath("//div[@id='b10_ticket_close_notes']"), [])
        article = document.xpath("//div[contains(@class, 'article')]")
        self.assertEqual(article[0].get("data-oe-id"), str(self.ticket.id))

        self.ticket.close_note = "<p>B10 closing note</p>"
        rendered, _ = report._render_qweb_html(report.report_name, self.ticket.ids)
        document = html.fromstring(rendered)
        self.assertIn("B10 closing note", document.text_content())
        self.assertEqual(len(document.xpath("//div[@id='b10_ticket_close_notes']")), 1)
