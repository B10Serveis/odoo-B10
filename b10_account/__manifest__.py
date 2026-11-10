{
    "name": "Batista10 - Account",
    "summary": """Personalitzacions de Facturació""",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "category": "Personalization",
    "version": "18.0.1.11.0",
    "depends": [
        "account",
        "mis_builder",  # Motor dels informes MIS
        "l10n_es_mis_report",  # Plantilles i estils PGCE
        "b10_base",
        "b10_mail",
        "l10n_es_partner",
        "l10n_es_partner_mercantil",
        "account_payment_sale",
        "l10n_es_verifactu_oca",
        "report_qweb_element_page_visibility",  # Perque el QR surti només a la primera pàgina
        "account_payment_partner",  # account.move:payment_mode_id
        "sale_stock",  # sale.order.line:move_ids
    ],
    "license": "AGPL-3",
    "application": True,
    "data": [
        "views/config_settings_view.xml",
        "views/account_move_inherit.xml",
        "report/factura_batista.xml",
        "report/report_factura_batista.xml",
        "views/email_factura_impagada.xml",
        "views/email_factura.xml",
        "views/invoice_report_pivot.xml",
        "data/account.payment.method.csv",
        "views/partner_form_inherit.xml",
        "data/mis_report_styles.xml",
        "data/mis_report_balance_abreviated_3digits.xml",
        "data/mis_report_pyg_abreviated_3digits.xml",
    ],
}
