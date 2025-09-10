# Copyright 2024, 2025 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import csv
import io
import itertools

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

def _g_if_gift(gift_val, nongift_val=""):
    return lambda r, sl: (
        gift_val if sl.discount == 100 or _v_price(sl) == 0
        else nongift_val)

def _f_str_or_empty(rep, v):
    return str(v) if v is not False else ""

def _f_date(rep, v):
    return v.strftime("%Y%m%d") if v else ""

def _f_float(rep, v):
    return ("%g" % v).replace(".", ",") if v is not False else ""

# Other helpers.

def _v_price(sale_line):  # TODO: cache
    return round(1000 * (  # may be tuned to include some taxes
        sale_line.price_unit * sale_line.quantity))

def _v_discount(sale_line):  # TODO: cache
    return round(1000 * (  # no taxes
        sale_line.price_unit * sale_line.quantity * sale_line.discount / 100))

# Report format for the individual fields of each report type.
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

    "sales": [
        ("Distribuidor", 10, _g_damm_code, _f_str_or_empty),
        ("Nº Cliente", 20, _g_field("partner_id.id"), _f_str_or_empty),
        ("Nº Producto", 20, _g_field("product_id.id"), _f_str_or_empty),
        ("Nº Producto Damm", 20, _g_field("product_id.default_code"), _f_str_or_empty),
        ("Tipo documento venta", 2, _g_const("EN"), None),
        ("Servicio a terceros", 1, _g_const("N"), None),
        ("Nº Pedido Detallista", 20, _g_field("move_id.invoice_origin"), _f_str_or_empty),
        ("Nº Documento", 20, _g_field("move_name"), _f_str_or_empty),
        ("Nº Línea doc", 10, _g_field("sequence"), None),
        ("Fecha documento", 8, _g_field("date"), _f_date),
        ("Cantidad", 15, lambda r, sl: round(sl.quantity * 100_000), None),
        ("Importe albarán", 12,
         lambda r, sl: _v_discount(sl) if sl.discount == 100 else _v_price(sl), None),
        ("Importe Dto", 12, lambda r, sl: _v_discount(sl), None),
        ("Nº descuento", 20,
         lambda r, sl: "" if sl.discount in [0, 100] else "DTO VALOR", None),
        ("Nº descuento en producto", 20, _g_empty, None),
        ("Tipo obsequio ", 20, _g_if_gift("OBSEQUIO"), None),
        ("Motivo Obsequio", 10, _g_if_gift("ZH08"), None),
        ("Fecha aplicación cond. precio", 8, _g_field("date"), _f_date),
        ("Sin cargo", 2, _g_if_gift("OB", "NO"), None),
        ("Prev. Habitual", 10, _g_field("partner_id.user_id.id"), _f_str_or_empty),
        ("Prev. Documento", 10, _g_field("move_id.user_id.id"), _f_str_or_empty),
        ("SubDistribuidor", 10, _g_empty, None),
    ],

    "conditions": [
        ("Distribuidor", 50, _g_damm_code, _f_str_or_empty),
        ("cod_Establ", None, _g_empty, None),
        ("cod_detallista", 50,
         lambda r, ci: ci.env.context.get("_partner_id"), None),
        ("TipoCondición", 25,
         lambda r, ci: "Descuento Valor" if ci.compute_price == "percentage" else "", None),
        ("Modalidad", 50, _g_const("%"), None),
        ("FechaDesde", None, _g_field("date_start"), _f_date),
        ("NM", 50, _g_const("M"), None),
        ("GrupoObjetivo", 50, _g_empty, None),
        ("Nº Producto", 20, _g_field("product_tmpl_id.id"), _f_str_or_empty),
        ("Material", 25, _g_field("product_tmpl_id.default_code"), _f_str_or_empty),
        ("Objetivo_N", None, _g_const(0.0), _f_float),
        ("Periodo", 50, _g_const("Factura"), None),
        ("Entrega_Mínima", None, _g_field("min_quantity"),  _f_float),
        ("FechaHasta", None, _g_field("date_end"), _f_date),
        ("Centralizada", None, _g_const("N"), None),
        ("Descuento_M", None, _g_field("percent_price"), _f_float),
        ("Objetivo_Tipo", 50, _g_const("Cajas"), None),
        ("Comentarios", 255, _g_empty, None),
        ("Aplicable", 10, _g_const("Depend"), None),
        ("Libre", None, _g_empty, None),
        ("MotivoAlta", 50, _g_empty, None),
        ("Marca_HK", None, _g_empty, None),
        ("Marca_MH", None, _g_empty, None),
        ("Marca_CC", None, _g_empty, None),
        ("Marca_AM", None, _g_empty, None),
        ("Marca_MO", None, _g_empty, None),
        ("Marca_SM", None, _g_empty, None),
        ("Marca_Otras", 50, _g_empty, None),
        ("Observaciones", 255, _g_empty, None),
    ],
}

# Report types which use a format with fixed field widths.
_report_formats_fixed = {"sales"}

# Report name formatter functions, by report type.
_report_names = {
    "customers": lambda rep: ("Det_%s_%s.txt"
                              % (rep.env.user.company_id.damm_dealer_code,
                                 rep.date_start.strftime("%Y%m%d"))),
    "sales": lambda rep: ("%s_VENTAS_Factura_%s.txt"
                          % (rep.env.user.company_id.damm_dealer_code,
                             rep.date_start.strftime("%Y%m"))),
    "conditions": lambda rep: ("CondCiales_%s_%s.txt"
                               % (rep.env.user.company_id.damm_dealer_code,
                                  rep.date_start.strftime("%Y%m%d"))),
}


class DammReportsWizard(models.TransientModel):
    _name = "damm.reports.wizard"
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

    def _search_report_items(self) -> dict[int, object]:
        company = self.env.user.company_id
        damm_partner_id = company.damm_partner_id.id

        customers = {}
        sale_lines = {}
        is_product_by_damm = {}  # cache
        sales = self.env["account.move"].search([
            ("state", "=", "posted"),
            ("invoice_date", ">=", self.date_start),
            ("invoice_date", "<=", self.date_end),
        ])
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

        if self.report_type == "customers":
            return customers
        if self.report_type == "sales":
            return sale_lines
        del sales, sale_lines

        conditions = {}
        # Conditions for non-buyers are irrelevant,
        # filter by customers that did buy (and group them by pricelist).
        plist_ids = dict((plist_id, list(custs))
                         for plist_id, custs in itertools.groupby(
                             customers.values(),
                             lambda c: c.property_product_pricelist.id)
                         if plist_id)
        plist_items = self.env["product.pricelist.item"].search([
            ("pricelist_id", "in", list(plist_ids)),
        ])
        for plist_item in plist_items:
            product = plist_item.product_tmpl_id
            if damm_partner_id in product.mapped("seller_ids.name.id"):  # TODO: cache
                # The condition must appear for each customer that it applies to,
                # so decorate it with the customer id to tell them apart.
                for plcust in plist_ids[plist_item.pricelist_id.id]:
                    conditions[plist_item.id, plcust.id] = (
                        plist_item.with_context(_partner_id=plcust.id))

        assert(self.report_type == "conditions")
        return conditions

    def _format_report_items(self, items: dict[int, object]) -> (
            list[dict[str, str]]
    ):
        formats = _report_formats[self.report_type]
        formatted_items = []
        fixed_width = self.report_type in _report_formats_fixed
        for item in items.values():
            formatted_item = {}
            for (title, maxlen, getter, formatter) in formats:
                value = getter(self, item)

                ffmt = "%s"  # report's generic field format
                if fixed_width:
                    ffmt = "%%%ds" % (maxlen if isinstance(value, (int, float))
                                      else -maxlen)
                if formatter:
                    value = formatter(self, value)
                value = (ffmt % value)[:maxlen]

                formatted_item[title] = value
            formatted_items.append(formatted_item)
        return formatted_items

    def _assemble_report(self, lines: list[dict[str, str]]) -> (
            tuple[str, bytes]
    ):
        report_name = _report_names[self.report_type](self)
        field_names = [fmt[0] for fmt in _report_formats[self.report_type]]
        lterm = "\r\n"

        if self.report_type in _report_formats_fixed:
            # One entry per line, fields in order, back-to-back.
            report_data = lterm.join(
                "".join(line[f] for f in field_names)
                for line in lines
            )
            if report_data:
                report_data += lterm
        else:
            csv_file = io.StringIO()
            csv_writer = csv.DictWriter(csv_file, fieldnames=field_names,
                                        delimiter="[", lineterminator=lterm,
                                        quoting=csv.QUOTE_NONE)
            # csv_writer.writeheader()
            for line in lines:
                csv_writer.writerow(line)
            report_data = csv_file.getvalue()

        return (report_name, report_data.encode("utf-8"))  # TODO check encoding

    def generate_report(self):
        self.ensure_one()
        report_items = self._search_report_items()

        if not report_items:
            # Avoid weird behaviour with empty data
            # (e.g. missing attachment, 404 Not Found with `/web/content`).
            raise exceptions.UserError("No items match the given selection, empty report")

        line_data = self._format_report_items(report_items)
        report_name, report_data = self._assemble_report(line_data)
        raise NotImplementedError("TODO")
