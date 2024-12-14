# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models

class AccountTax(models.Model):
    _inherit = "account.tax"

    l10n_ad_exempt_reason = fields.Selection(
        selection=[
            ("E1", "No exempt"),
        ],
        string="Exempt Reason (Andorra)",
    )
    l10n_ad_type = fields.Selection(
        selection=[
            ("sujeto", "Sujeto"),
            ("retencion", "Retencion"),
        ],
        string="Tax Type (Andorra)", default="sujeto",
    )
    l10n_ad_bien_inversion = fields.Boolean("Bien de Inversion", default=False)
