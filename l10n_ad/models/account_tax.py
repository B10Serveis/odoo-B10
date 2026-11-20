# Copyright 2024, 2025 Batista10
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    l10n_ad_type = fields.Selection(
        selection=[
            ("subjecte", "Subject"),
            ("retencio", "Withholding"),
        ],
        string="Tax Type (Andorra)", default="subjecte",
    )
    l10n_ad_bien_inversion = fields.Boolean(string="Investment Goods (Andorra)")
