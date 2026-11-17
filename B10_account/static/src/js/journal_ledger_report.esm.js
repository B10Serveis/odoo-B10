/** @odoo-module **/

import { ReportAction } from "@web/webclient/actions/reports/report_action";
import { patch } from "@web/core/utils/patch";

const HTML_REPORT_NAME = "B10_account.journal_ledger_report";
const XLSX_REPORT_NAME = "b10_account.journal_ledger_xlsx";

patch(ReportAction.prototype, {
    setup() {
        super.setup(...arguments);
        if (this.props.report_name === HTML_REPORT_NAME) {
            this.isAccountFinancialReport = true;
        }
    },

    _get_xlsx_name(reportName) {
        if (reportName === HTML_REPORT_NAME) {
            return XLSX_REPORT_NAME;
        }
        return super._get_xlsx_name(...arguments);
    },
});
