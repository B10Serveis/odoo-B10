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


class contractLineB10(models.Model):
    _inherit = "contract.line"
    # Modifica el camp last_date_invoiced per que es calculi a partir del del contracte en cas que no estigui marcat el camp bool line_recurrence
    last_date_invoiced = fields.Date(
        string="Last date invoiced",
        compute="compute_last_date_invoiced",
        store=True,
    )

    @api.depends(
        "is_recurring_note",
        "write_date",
        "contract_id.last_date_invoiced",
        "contract_id.write_date",
    )
    def compute_last_date_invoiced(self):
        for record in self:
            if not record.contract_id.line_recurrence:
                record["last_date_invoiced"] = record.contract_id.last_date_invoiced
