{
    "name": "Batista10 - Account",
    "summary": """Personalitzacions de Facturació""",
    "author": "Batista10",
    "website": "https://www.batista10.cat",
    "category": "Personalization",
    "version": "18.0.1.7.6",
    "depends": [
        "account",
        "b10_mail",
        "l10n_es_partner",
        "l10n_es_partner_mercantil",
        "account_payment_sale",
        "b10_settings_hub",
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
    ],
}
