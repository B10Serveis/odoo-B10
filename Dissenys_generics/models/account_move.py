from odoo import models, api, fields
from urllib.parse import urlencode

import base64
from io import BytesIO
try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_M
except Exception:
    qrcode = None

# Namespace de l’AEAT per a les XPath
NAMESPACE_SF_INFO = {
    "sf": "https://www2.agenciatributaria.gob.es/static_files/common/internet/dep/aplicaciones/es/aeat/tike/cont/ws/SuministroInformacion.xsd"
}

class AccountMove(models.Model):
    _inherit = "account.move"

    qr_code_image = fields.Binary(
        string="VeriFactu QR (PNG)",
        compute="_compute_qr_code_image",
        store=False,
    )

    l10n_es_edi_verifactu_qr_url = fields.Char(
        compute="_compute_l10n_es_edi_verifactu_qr_url",
        store=False,
        readonly=True,
    )
    
    def _compute_l10n_es_edi_verifactu_qr_url(self):
        EdiFormat = self.env["account.edi.format"]
        for move in self:
            url = False
            
            demo_vals = {
                'nif': move.company_id.vat or 'B00000000',
                'numserie': move.name or 'FAC-DEMO-0001',
                'fecha': (move.invoice_date or fields.Date.today()).strftime('%Y-%m-%d'),
                'importe': f"{move.amount_total:.2f}",
            }
            base_url = getattr(EdiFormat, '_l10n_es_verifactu_aeat_qr_url', lambda m: 'https://aeat.example/qr')(move)
            url = f"{base_url}?{urlencode(demo_vals, encoding='utf-8')}"

            move.l10n_es_edi_verifactu_qr_url = url

    @api.depends('l10n_es_edi_verifactu_qr_url')
    def _compute_qr_code_image(self):
        for rec in self:
            rec.qr_code_image = False  
            url = rec.l10n_es_edi_verifactu_qr_url
            if qrcode and url:
                buf = BytesIO()
                img = qrcode.make(url, error_correction=ERROR_CORRECT_M, box_size=10, border=2)
                img.save(buf, format="PNG")
                rec.qr_code_image = base64.b64encode(buf.getvalue()).decode()
