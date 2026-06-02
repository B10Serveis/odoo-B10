from odoo import fields, models


class B10CommissionLineReport(models.Model):
    _name = "b10.commission.line.report"
    _description = "Commission line report"
    _auto = False
    _order = "date desc, move_id"

    line_id = fields.Many2one("account.move.line", string="Line", readonly=True)
    move_id = fields.Many2one("account.move", string="Factura", readonly=True)
    date = fields.Date(string="Data", readonly=True)
    journal_id = fields.Many2one("account.journal", string="Diari", readonly=True)
    currency_id = fields.Many2one("res.currency", string="Currency", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Client", readonly=True)
    product_id = fields.Many2one("product.product", string="Producte", readonly=True)
    product_categ_id = fields.Many2one(
        "product.category", string="Categoria", readonly=True
    )
    label = fields.Char(string="Etiqueta", readonly=True)
    quantity = fields.Float(string="Quant.", readonly=True)
    price_unit = fields.Float(string="Preu Un.", readonly=True)
    price_subtotal = fields.Float(string="Subtotal (sense iva)", readonly=True)
    price_total = fields.Float(string="Total (amb iva)", readonly=True)
    agent_id = fields.Many2one("res.partner", string="Agent", readonly=True)

    def _exists_table(self, table_name):
        self.env.cr.execute("SELECT to_regclass(%s)", (table_name,))
        return bool(self.env.cr.fetchone()[0])

    def _column_exists(self, table_name, column_name):
        self.env.cr.execute(
            "SELECT 1 FROM information_schema.columns WHERE table_name=%s AND column_name=%s",
            (table_name, column_name),
        )
        return bool(self.env.cr.fetchone())

    def init(self):
        self.env.cr.execute("DROP VIEW IF EXISTS b10_commission_line_report")
        query = self._get_sql_query()
        self.env.cr.execute(
            "CREATE OR REPLACE VIEW b10_commission_line_report AS (%s)" % query
        )

    def _get_sql_query(self):
        return (
            "SELECT (l.id::bigint << 32) + a.id AS id, "
            "l.id AS line_id, l.move_id, l.date, l.journal_id, l.currency_id, l.partner_id, "
            "l.product_id, pt.categ_id AS product_categ_id, l.name AS label, l.quantity, l.price_unit, "
            "l.price_subtotal, l.price_total, a.agent_id AS agent_id "
            "FROM account_move_line l "
            "JOIN account_invoice_line_agent a ON a.object_id = l.id "
            "LEFT JOIN product_product pp ON pp.id = l.product_id "
            "LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id "
            "WHERE a.agent_id IS NOT NULL"
        )

    def _commission_rel_query(self, rel_table, rel_line_col, rel_agent_col):
        return (
            "SELECT (l.id::bigint << 32) + a.id AS id, "
            "l.id AS line_id, l.move_id, l.date, l.journal_id, l.partner_id, "
            "l.account_id, l.name AS label, l.debit, l.credit, l.balance, a.id AS agent_id "
            "FROM account_move_line l "
            "JOIN %s rel ON rel.%s = l.id "
            "JOIN res_partner a ON a.id = rel.%s"
        ) % (rel_table, rel_line_col, rel_agent_col)

    def _commission_field_query(self, field_name):
        return (
            "SELECT (l.id::bigint << 32) + coalesce(l.%s, 0) AS id, "
            "l.id AS line_id, l.move_id, l.date, l.journal_id, l.partner_id, "
            "l.account_id, l.name AS label, l.debit, l.credit, l.balance, l.%s AS agent_id "
            "FROM account_move_line l "
            "WHERE l.%s IS NOT NULL"
        ) % (field_name, field_name, field_name)

    def _fallback_query(self):
        return (
            "SELECT (l.id::bigint << 32) + coalesce(l.partner_id, 0) AS id, "
            "l.id AS line_id, l.move_id, l.date, l.journal_id, l.partner_id, "
            "l.account_id, l.name AS label, l.debit, l.credit, l.balance, l.partner_id AS agent_id "
            "FROM account_move_line l "
            "WHERE l.partner_id IS NOT NULL"
        )
