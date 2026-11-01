from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPaymentModeOnchange(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Onchange supplier"})
        cls.supplier_bank = cls.env["res.partner.bank"].create({
            "partner_id": cls.partner.id,
            "acc_number": "B10-ONCHANGE-SUPPLIER",
        })
        cls.company_bank = cls.env["res.partner.bank"].create({
            "partner_id": cls.env.company.partner_id.id,
            "acc_number": "B10-ONCHANGE-COMPANY",
        })
        journal = cls.env["account.journal"].new({
            "type": "bank",
            "bank_account_id": cls.company_bank.id,
        })
        cls.mode = cls.env["account.payment.mode"].new({
            "payment_method_id": cls.env.ref(
                "Dissenys_generics.account_payment_method_bank_transfer"
            ).id,
            "bank_account_link": "fixed",
        })
        cls.mode.fixed_journal_id = journal

    def _new_move(self, move_type, mode, bank=False):
        move = self.env["account.move"].new({
            "move_type": move_type,
            "partner_id": self.partner.id,
            "company_id": self.env.company.id,
            "partner_bank_id": bank.id if bank else False,
        })
        move.payment_mode_id = mode
        # Isolate this onchange from the computed default bank.
        move.partner_bank_id = bank
        return move

    def test_outbound_documents_preserve_supplier_bank(self):
        for move_type in ("in_invoice", "out_refund", "in_receipt", "entry"):
            with self.subTest(move_type=move_type):
                move = self._new_move(move_type, self.mode, self.supplier_bank)
                move._onchange_payment_mode_id_b10()
                self.assertEqual(move.partner_bank_id, self.supplier_bank)

    def test_inbound_transfer_selects_company_bank(self):
        for move_type in ("out_invoice", "in_refund", "out_receipt"):
            with self.subTest(move_type=move_type):
                move = self._new_move(move_type, self.mode)
                move._onchange_payment_mode_id_b10()
                self.assertEqual(move.partner_bank_id, self.company_bank)

    def test_other_method_preserves_bank(self):
        self.mode.payment_method_id = self.env.ref(
            "account.account_payment_method_manual_in"
        )
        move = self._new_move("out_invoice", self.mode, self.supplier_bank)
        move._onchange_payment_mode_id_b10()
        self.assertEqual(move.partner_bank_id, self.supplier_bank)

    def test_no_mode_preserves_bank(self):
        move = self._new_move("out_invoice", False, self.supplier_bank)
        move._onchange_payment_mode_id_b10()
        self.assertEqual(move.partner_bank_id, self.supplier_bank)

    def test_inbound_transfer_keeps_incompatible_bank_warning(self):
        move = self._new_move("out_invoice", self.mode, self.supplier_bank)
        with self.assertRaises(ValidationError):
            move._onchange_payment_mode_id_b10()
