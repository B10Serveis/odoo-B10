# Copyright 2024, 2025 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, exceptions, models, fields


class DammReportsWizard(models.TransientModel):
    _name = "damm_integration.reports.wizard"
    _description = "Wizard to help create reports for Damm"

    # To show a warning about incomplete configuration in the view.
    damm_config_ok = fields.Boolean(
        default=(lambda self:
                 bool(self.env.user.company_id.damm_dealer_code
                      and self.env.user.company_id.damm_partner_id)))

    date_start = fields.Date(
        string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(
        string="End Date", required=True, default=fields.Date.today)

    report_type = fields.Selection(
        [
            ("customers", "Customers Data"),
            ("conditions", "Commercial Conditions"),
            ("sales", "Sales"),
        ],
        string="Report Type",
        required=True,
        default="sales",
    )

    @api.constrains("date_start", "date_end")
    def _check_dates_range(self):
        for report in self:
            if report.date_start > report.date_end:
                raise models.ValidationError(
                    "Report end date must be greater than its start date")

    @api.model
    def create(self, values):
        company = self.env.user.company_id
        dealer_code = company.damm_dealer_code
        if not dealer_code:
            raise exceptions.UserError("Please configure your company's Damm dealer code")
        damm_partner = company.damm_partner_id
        if not damm_partner:
            raise exceptions.UserError("Please configure which partner is the Damm company")
        return super(DammReportsWizard, self).create(values)

    def generate_report(self):
        self.ensure_one()

        company = self.env.user.company_id
        damm_partner_id = company.damm_partner_id.id
        sale_orders = self.env["sale.order"].search(
            [
                ("state", "=", "sale"),
                ("date_order", ">=", self.date_start),
                ("date_order", "<=", self.date_end),
            ]
        )

        customer_ids = set()
        sale_line_ids = set()
        is_product_by_damm = {}  # cache
        for sale_order in sale_orders:
            customer_id = sale_order.partner_id.id
            for sale_order_line in sale_order.order_line:
                product = sale_order_line.product_id
                by_damm = is_product_by_damm.get(product.id)
                if by_damm is None:  # cache whether product by Damm
                    is_product_by_damm[product.id] = by_damm = (
                        damm_partner_id in product.mapped("seller_ids.name.id")
                    )
                if by_damm:
                    customer_ids.add(customer_id)
                    sale_line_ids.add(sale_order_line.id)

        raise NotImplementedError("TODO")
