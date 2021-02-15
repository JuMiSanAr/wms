/**
 * Copyright 2021 ACSONE SA/NV (http://www.acsone.eu)
 * @author Simone Orsi <simahawk@gmail.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

import {ScenarioBaseMixin} from "/shopfloor_mobile_base/static/wms/src/scenario/mixins.js";
import {process_registry} from "/shopfloor_mobile_base/static/wms/src/services/process_registry.js";

const Partner = {
    mixins: [ScenarioBaseMixin],
    template: `
        <Screen :screen_info="screen_info">
            <template v-slot:header>
                <state-display-info :info="state.display_info" v-if="state.display_info"/>
            </template>
            <searchbar
                v-if="state.on_scan"
                v-on:found="on_scan"
                :input_placeholder="search_input_placeholder"
                />
        </Screen>
        `,
    methods: {
        screen_title: function() {
            if (_.isEmpty(this.current_doc()) || this.state_is("confirm_start"))
                return this.menu_item().name;
            let title = this.current_doc().record.name;
            return title;
        },
        current_doc: function() {
            const data = this.state_get_data("view_partner");
            if (_.isEmpty(data)) {
                return null;
            }
            return {
                record: data.picking,
                identifier: data.picking.name,
            };
        },
    },
    data: function() {
        return {
            usage: "partner",
            initial_state_key: "scan_partner",
            states: {
                scan_partner: {
                    display_info: {
                        title: "Scan a partner",
                        scan_placeholder: "Scan ref",
                    },
                    on_scan: scanned => {
                        this.wait_call(
                            this.odoo.call("scan_partner", {barcode: scanned.text})
                        );
                    },
                    on_manual_selection: evt => {
                        this.wait_call(this.odoo.call("list_stock_picking"));
                    },
                },
                view_partner: {
                    display_info: {
                        title: "Partner detail",
                    },
                    on_scan: scanned => {
                        this.wait_call(
                            this.odoo.call("scan_document", {barcode: scanned.text})
                        );
                    },
                    on_manual_selection: evt => {
                        this.wait_call(this.odoo.call("list_stock_picking"));
                    },
                },
            },
        };
    },
};

process_registry.add("partner", Partner);

export default Partner;
