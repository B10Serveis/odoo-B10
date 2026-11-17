/** @odoo-module **/

import { ReportAction } from "@web/webclient/actions/reports/report_action";
import { patch } from "web.utils";

patch(ReportAction.prototype, "B10_account.ReportAction", {
    setup() {
        this._super.apply(this, arguments);
        if (this.props.report_name === "B10_account.journal_ledger_report") {
            this.isAccountFinancialReport = true;
        }
    },

    _get_xlsx_name(reportName) {
        if (reportName === "B10_account.journal_ledger_report") {
            return "b10_account.journal_ledger_xlsx";
        }
        return this._super.apply(this, arguments);
    },
});
