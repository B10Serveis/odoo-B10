# Copyright 2020 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br> - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class CrmLead(models.Model):
    _inherit = "crm.lead"

    secondary_user_id = fields.Many2one(
        'res.users', string="Secondary Salesperson", tracking=True
    )

    _sql_constraints = [
        (
            "check_secondary_salesperson",
            "CHECK((secondary_user_id IS NULL) OR (secondary_user_id != user_id))",
            "El secondary salesperson ha de ser diferent del primary salesperson.",
        ),
    ]
