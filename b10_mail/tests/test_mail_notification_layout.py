from base64 import b64encode
from pathlib import Path

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestMailNotificationLayout(TransactionCase):
    def test_inherited_mail_layouts_combine(self):
        for xmlid in (
            "mail.mail_notification_invite",
            "mail.mail_notification_multi_invite",
            "mail.mail_notification_layout_with_responsible_signature",
        ):
            self.assertTrue(self.env.ref(xmlid).get_combined_arch())

    def test_notification_renders_company_logo_without_footer(self):
        company = self.env.company
        icon_path = Path(__file__).resolve().parents[1] / "static/description/icon.png"
        with icon_path.open("rb") as icon:
            company.logo = b64encode(icon.read())
        self.assertFalse(company.uses_default_logo)

        html = self.env["mail.render.mixin"].with_context(
            email_notification_force_header=True,
            email_notification_force_footer=True,
        )._render_encapsulate(
            "mail.mail_notification_layout",
            "<p>Message body</p>",
            add_context={
                "company": company,
                "has_button_access": True,
                "button_access": {"url": "https://example.invalid", "title": "View"},
                "show_unfollow": True,
                "email_add_signature": True,
                "signature": "<p>Signature text</p>",
            },
        )

        self.assertIn(f"/logo.png?company={company.id}", html)
        self.assertIn("Message body", html)
        self.assertIn("Signature text", html)
        self.assertNotIn("o_mail_notification", html)
        self.assertNotIn("Powered by", html)
        self.assertNotIn("mail_unfollow", html)
