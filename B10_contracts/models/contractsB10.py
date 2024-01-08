from odoo import models, fields, api
from datetime import datetime


class contractsB10(models.Model):
    _inherit = "contract.contract"
    # Afegir camp Estat Caducitat
    contract_expiration = fields.Date(
        string="Contract expiration",
        compute="compute_expiration",
        store=True,
    )

    @api.depends("date_end", "write_date")
    # depends defineix el trigger de compute, Write_date perque cada vegada que hi hagi una modificació a la comanda s'actualitzi
    def compute_expiration(self):
        for record in self:
            record["contract_expiration"] = record.date_end
