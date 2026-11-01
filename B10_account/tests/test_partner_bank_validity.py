from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPartnerBankValidity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env["res.partner"].create({"name": "Supplier A"})
        cls.other_supplier = cls.env["res.partner"].create({"name": "Supplier B"})
        cls.bank = cls.env["res.partner.bank"].create({
            "partner_id": cls.supplier.id,
            "acc_number": "B10-TEST-A",
        })
        cls.other_bank = cls.env["res.partner.bank"].create({
            "partner_id": cls.other_supplier.id,
            "acc_number": "B10-TEST-B",
        })
        cls.mode = cls.env["account.payment.mode"].create({
            "name": "Supplier payment",
            "company_id": cls.env.company.id,
            "bank_account_link": "variable",
            "payment_method_id": cls.env.ref(
                "account.account_payment_method_manual_out"
            ).id,
        })

    def _new_move(self):
        return self.env["account.move"].new({
            "move_type": "in_invoice",
            "company_id": self.env.company.id,
            "partner_id": self.supplier.id,
            "payment_mode_id": self.mode.id,
            "partner_bank_id": self.bank.id,
        })

    def test_change_supplier_replaces_bank(self):
        move = self._new_move()
        move.partner_id = self.other_supplier
        self.assertEqual(move.partner_bank_id, self.other_bank)

    def test_change_supplier_without_bank_clears_bank(self):
        move = self._new_move()
        move.partner_id = self.env["res.partner"].create({"name": "No bank"})
        self.assertFalse(move.partner_bank_id)

    def test_valid_manual_bank_is_preserved(self):
        manual_bank = self.bank.copy({"acc_number": "B10-TEST-MANUAL"})
        move = self._new_move()
        move.partner_bank_id = manual_bank
        move._compute_partner_bank_id()
        self.assertEqual(move.partner_bank_id, manual_bank)

    def test_bank_from_another_company_is_replaced(self):
        company = self.env["res.company"].create({"name": "Other bank company"})
        foreign_bank = self.bank.copy({
            "acc_number": "B10-TEST-FOREIGN",
            "company_id": company.id,
        })
        move = self._new_move()
        move.partner_bank_id = foreign_bank
        move._compute_partner_bank_id()
        self.assertEqual(move.partner_bank_id, self.bank)

    def test_transfer_without_allowed_journals_clears_bank(self):
        move = self._new_move()
        mode = self.mode.copy({
            "payment_method_id": self.env.ref(
                "Dissenys_generics.account_payment_method_bank_transfer"
            ).id,
        })
        move.payment_mode_id = mode
        self.assertFalse(move.partner_bank_id)
