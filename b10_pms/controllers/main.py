# Copyright 2026 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request


class PmsPropertyLogoController(http.Controller):
    @http.route(
        "/b10_pms/property/<int:property_id>/logo",
        type="http",
        auth="public",
    )
    def property_logo(self, property_id):
        """Serve the property logo to recipients that cannot read PMS records."""
        pms_property = (
            request.env["pms.property"].sudo().browse(property_id).exists()
        )
        if not pms_property:
            return request.not_found()

        stream = request.env["ir.binary"]._get_image_stream_from(
            pms_property, "logo"
        )
        stream.public = True
        return stream.get_response(
            as_attachment=False,
            content_security_policy=None,
        )
