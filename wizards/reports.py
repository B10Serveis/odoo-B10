# Copyright 2024, 2025 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, exceptions, models, fields


# Report item field getters and value formatters.
def _g_damm_code(rep, item):
    return rep.env.user.company_id.damm_dealer_code

def _g_field(f):
    def _g_field_getter(rep, item):
        value = item
        for field in f.split("."):
            value = getattr(value, field)
        return value
    return _g_field_getter

def _g_const(v):
    return lambda rep, item: v

_g_empty = _g_const("")

def _f_str_or_empty(rep, v):
    return str(v) if v is not False else ""

# Report format for each report type.
# Each value is a list of tuples
# `(title, maxlen, getter(report, item), formatter(report, value))`.
_report_formats = {
    "customers": [
        ("Distribuidor", 10, _g_damm_code, _f_str_or_empty),
        ("cod_Detallista", 50, _g_field("id"), _f_str_or_empty),
        ("Nombre", 150, _g_field("comercial"), _f_str_or_empty),
        ("Prefijo", 50, _g_empty, None),
        ("NombreAj", 100, _g_field("comercial"), _f_str_or_empty),
        ("Domicilio", 155, _g_field("street"), _f_str_or_empty),
        ("TipoCalle", 50, _g_empty, None),
        ("Dom_Nombre", 50, _g_empty, None),
        ("Dom_Número", 50, _g_empty, None),
        ("Dom_Resto", 50, _g_empty, None),
        ("PoblacionDist", 50, _g_field("city"), _f_str_or_empty),
        ("cod_Postal", 5, _g_field("zip"), _f_str_or_empty),
        ("Telefono", 40, _g_field("phone"), _f_str_or_empty),
        ("MóvilTelefono", 40, _g_field("mobile"), _f_str_or_empty),
        ("email", 50, _g_field("email"), _f_str_or_empty),
        ("PersonaContacto", 40, _g_empty, None),
        ("Cadena", 50, _g_empty, None),
        ("SubDistribuidor", 50, _g_const("N"), None),
        ("Preventista", 20, _g_empty, None),
        ("Ruta", 50, _g_empty, None),
        ("Titular", 150, _g_field("name"), _f_str_or_empty),
        ("TitularNombre", 150, _g_empty, None),
        ("TitularApellido1", 50, _g_empty, None),
        ("TitularApellido2", 50, _g_empty, None),
        ("NIF_Distribuidor", 20, _g_field("vat"),
         lambda r, v: (v or "").replace("ES", "", 1)),
        ("DomicilioTit", 155, _g_field("street"), _f_str_or_empty),
        ("TipoCalleTit", 5, _g_empty, None),
        ("DomicilioNomTit", 50, _g_empty, None),
        ("DomicilioNumTit", 50, _g_empty, None),
        ("DomicilioRestoTit", 50, _g_empty, None),
        ("Cod_Postal_Tit", 5, _g_field("zip"), _f_str_or_empty),
        ("PoblaciónTit", 50, _g_field("city"), _f_str_or_empty),
    ],
}


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

    def _search_customers_and_sales(self):  # ->  (customers, sale_lines)
        company = self.env.user.company_id
        damm_partner_id = company.damm_partner_id.id
        sales = self.env["account.move"].search(
            [
                ("state", "=", "posted"),
                ("invoice_date", ">=", self.date_start),
                ("invoice_date", "<=", self.date_end),
            ]
        )

        customers = {}
        sale_lines = {}
        is_product_by_damm = {}  # cache
        for sale in sales:
            customer = sale.partner_id
            for sale_line in sale.invoice_line_ids:
                product = sale_line.product_id
                by_damm = is_product_by_damm.get(product.id)
                if by_damm is None:  # cache whether product by Damm
                    is_product_by_damm[product.id] = by_damm = (
                        damm_partner_id in product.mapped("seller_ids.name.id")
                    )
                if by_damm:
                    customers[customer.id] = customer
                    sale_lines[sale_line.id] = sale_line

        return (customers, sale_lines)

    def _format_report_items(self, items):
        formats = _report_formats[self.report_type]
        formatted_items = []
        for item in items.values():
            formatted_item = {}
            for (title, maxlen, getter, formatter) in formats:
                value = getter(self, item)
                value = formatter(self, value) if formatter else str(value)
                value = value[:maxlen]
                formatted_item[title] = value
            formatted_items.append(formatted_item)
        return formatted_items

    def generate_report(self):
        self.ensure_one()
        (customers, sale_lines) = self._search_customers_and_sales()

        if self.report_type == "customers":
            line_data = self._format_report_items(customers)
        else:
             raise NotImplementedError("TODO report type")

        raise NotImplementedError("TODO")
