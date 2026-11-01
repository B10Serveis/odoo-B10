from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestInheritedPartnerBank(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Bank compute supplier"})
        cls.bank = cls.env["res.partner.bank"].create({
            "partner_id": cls.partner.id,
            "acc_number": "B10-INHERITED-BANK",
        })

    def _new_invoice(self, payment_mode=False):
        return self.env["account.move"].new({
            "move_type": "in_invoice",
            "partner_id": self.partner.id,
            "company_id": self.env.company.id,
            "payment_mode_id": payment_mode.id if payment_mode else False,
            "partner_bank_id": False,
        })

    def test_no_mode_respects_company_setting(self):
        for keep_bank in (True, False):
            with self.subTest(keep_bank=keep_bank):
                self.env.company.keep_partner_bank_without_payment_mode = keep_bank
                move = self._new_invoice()
                move._compute_partner_bank_id()
                self.assertEqual(bool(move.partner_bank_id), keep_bank)
                if keep_bank:
                    self.assertEqual(move.partner_bank_id, self.bank)

    def test_outbound_mode_without_required_bank_clears_bank(self):
        method = self.env.ref("account.account_payment_method_manual_out")
        method.bank_account_required = False
        mode = self.env["account.payment.mode"].create({
            "name": "Payment without bank",
            "company_id": self.env.company.id,
            "payment_method_id": method.id,
            "bank_account_link": "variable",
        })
        move = self._new_invoice(mode)
        move.partner_bank_id = self.bank
        move._compute_partner_bank_id()
        self.assertFalse(move.partner_bank_id)

    def test_variable_transfer_selects_journal_bank(self):
        journal = self.env["account.journal"].create({
            "name": "Transfer bank",
            "code": "B10I",
            "type": "bank",
            "company_id": self.env.company.id,
            "bank_acc_number": "B10-INHERITED-TRANSFER",
        })
        mode = self.env["account.payment.mode"].create({
            "name": "Variable transfer",
            "company_id": self.env.company.id,
            "payment_method_id": self.env.ref(
                "Dissenys_generics.account_payment_method_bank_transfer"
            ).id,
            "bank_account_link": "variable",
            "variable_journal_ids": [(6, 0, journal.ids)],
        })
        move = self._new_invoice(mode)
        move.move_type = "out_invoice"
        move._compute_partner_bank_id()
        self.assertEqual(move.partner_bank_id, journal.bank_account_id)

        mode.variable_journal_ids = False
        move._compute_partner_bank_id()
        self.assertFalse(move.partner_bank_id)
