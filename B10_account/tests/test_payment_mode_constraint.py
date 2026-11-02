from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestPaymentModeConstraint(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        transfer = cls.env.ref(
            "Dissenys_generics.account_payment_method_bank_transfer"
        )
        cls.bank_journal = cls.env["account.journal"].create({
            "name": "Transfer bank",
            "code": "B10T",
            "type": "bank",
            "company_id": cls.env.company.id,
            "bank_acc_number": "B10-CONSTRAINT-BANK",
        })
        cls.mode = cls.env["account.payment.mode"].create({
            "name": "Transfer with allowed bank",
            "company_id": cls.env.company.id,
            "payment_method_id": transfer.id,
            "bank_account_link": "variable",
            "variable_journal_ids": [(6, 0, cls.bank_journal.ids)],
        })
        cls.compatible_mode = cls.mode.copy({"name": "Same allowed bank"})
        cls.incompatible_mode = cls.mode.copy({
            "name": "No allowed banks",
            "variable_journal_ids": [(5, 0, 0)],
        })

    def _create_invoice(self):
        return self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner_a.id,
            "journal_id": self.company_data["default_journal_sale"].id,
            "payment_mode_id": self.mode.id,
            "partner_bank_id": self.bank_journal.bank_account_id.id,
        })

    def test_write_only_incompatible_payment_mode_is_rejected(self):
        move = self._create_invoice()
        with self.assertRaisesRegex(
            ValidationError, "A recipient bank must be set"
        ), self.cr.savepoint():
            move.write({"payment_mode_id": self.incompatible_mode.id})

    def test_write_only_compatible_payment_mode_preserves_bank(self):
        move = self._create_invoice()
        move.write({"payment_mode_id": self.compatible_mode.id})
        self.assertEqual(move.payment_mode_id, self.compatible_mode)
        self.assertEqual(move.partner_bank_id, self.bank_journal.bank_account_id)

    def test_clear_payment_mode_is_allowed(self):
        move = self._create_invoice()
        move.write({"payment_mode_id": False})
        self.assertFalse(move.payment_mode_id)
