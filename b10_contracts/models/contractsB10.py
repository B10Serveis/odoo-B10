from odoo import api, fields, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    contract_expiration = fields.Date(
        string="Contract expiration",
        related="date_end",
        store=True,
    )
    last_date_invoiced = fields.Date(readonly=False)

    def write(self, vals):
        result = super().write(vals)
        if "last_date_invoiced" in vals or vals.get("line_recurrence") is False:
            for contract in self.filtered(lambda record: not record.line_recurrence):
                contract.contract_line_fixed_ids.write(
                    {"last_date_invoiced": contract.last_date_invoiced or False}
                )
        return result


class ContractLine(models.Model):
    _inherit = "contract.line"

    last_date_invoiced = fields.Date(string="Last date invoiced", readonly=False)

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [vals.copy() for vals in vals_list]
        for vals in vals_list:
            if "last_date_invoiced" not in vals and vals.get("contract_id"):
                contract = self.env["contract.contract"].browse(vals["contract_id"])
                if not contract.line_recurrence:
                    vals["last_date_invoiced"] = contract.last_date_invoiced or False
        return super().create(vals_list)
