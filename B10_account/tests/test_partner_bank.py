from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPartnerBank(TransactionCase):
    def test_variable_transfer_without_journals(self):
        """An unconfigured variable mode must leave the bank empty."""
        payment_mode = self.env["account.payment.mode"].create({
            "name": "Transfer without bank journals",
            "company_id": self.env.company.id,
            "bank_account_link": "variable",
            "payment_method_id": self.env.ref(
                "Dissenys_generics.account_payment_method_bank_transfer"
            ).id,
        })
        move = self.env["account.move"].new({
            "move_type": "out_invoice",
            "company_id": self.env.company.id,
            "payment_mode_id": payment_mode.id,
            "partner_bank_id": False,
        })

        move._compute_partner_bank_id()

        self.assertFalse(move.partner_bank_id)
