/**
 * Copyright 2020 Akretion (http://www.akretion.com)
 * @author Raphaël Reverdy <raphael.reverdy@akretion.com>
 * Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
 * @author Thierry Ducrest <thierry.ducrest@camptocamp.com>
 * @author Simone Orsi <simone.orsi@camptocamp.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

import {config_registry} from "/shopfloor_mobile_base/static/wms/src/services/config_registry.js";
import {
    AuthHandlerMixin,
    auth_handler_registry,
} from "/shopfloor_mobile_base/static/wms/src/services/auth_handler_registry.js";

//  Register apikey storage
config_registry.add("apikey", {default: "", reset_on_clear: true});

// Provide auth handle for Odoo calls
export class ApiKeyAuthHandler extends AuthHandlerMixin {
    get_params($root) {
        return {
            headers: {
                "API-KEY": $root.apikey,
            },
        };
    }
}
auth_handler_registry.add(new ApiKeyAuthHandler("api_key"));

/**
 * Handle loging via API key.
 *
 * Conventional name: `login-` + auth_type (from app config)
 */
Vue.component("login-api_key", {
    data: function () {
        return {
            error: "",
            apikey: "",
        };
    },
    methods: {
        login: function (evt) {
            evt.preventDefault();
            // Call odoo application load => set the result in the local storage in json
            this.$parent.error = "";
            this.$root.apikey = this.apikey;
            this.$root
                ._loadConfig()
                .catch((error) => {
                    this._handle_invalid_key();
                })
                .then(() => {
                    // TODO: shall we do this in $root._loadRoutes?
                    if (this.$root.authenticated) {
                        this.$router.push({name: "home"});
                    } else {
                        this._handle_invalid_key();
                    }
                });
        },
        _handle_invalid_key() {
            this.error = this.$t("screen.login.error.api_key_invalid");
            this.$root.apikey = "";
        },
    },
    template: `
    <v-form v-on:submit="login">
        <v-text-field
            name="apikey"
            v-model="apikey"
            :label="$t('screen.login.api_key_label')"
            :placeholder="$t('screen.login.api_key_placeholder')"
            autofocus
            autocomplete="off"></v-text-field>
        <div class="button-list button-vertical-list full">
            <v-row align="center">
                <v-col class="text-center" cols="12">
                    <v-btn color="success" type="submit">{{ $t('screen.login.action.login') }}</v-btn>
                </v-col>
            </v-row>
        </div>
    </v-form>
    `,
});
