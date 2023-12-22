from odoo import models, fields, api
from datetime import datetime


class contractsB10(models.Model):
    _inherit = "contract.contract"
    # Afegir camp Estat Caducitat
    contract_expiration = fields.Text(
        [
            ("active", "Active"),
            ("expired", "Expired"),
        ],
        string="Contract expiration",
        default="active",
        compute="compute_caducitat",
        store=True,
    )

    @api.depends("date_end", "write_date")
    # depends defineix el trigger de compute, Write_date perque cada vegada que hi hagi una modificació a la comanda s'actualitzi
    def compute_expiration(self):
        for record in self:
            if record.date_end and record.date_end > fields.datetime.now():
                record["contract_expiration"] = "expired"
                break
            else:
                record["contract_expiration"] = "active"
                break
