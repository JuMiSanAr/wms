/**
 * @author Simone Orsi <simone.orsi@camptocamp.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

import {
    AuthHandlerMixin,
    auth_handler_registry,
} from "/shopfloor_mobile_base/static/wms/src/services/auth_handler_registry.js";
import {config_registry} from "/shopfloor_mobile_base/static/wms/src/services/config_registry.js";

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

    on_login($root, evt, data) {
        evt.preventDefault();
        // Call odoo application load => set the result in the local storage in json
        // $root.apikey = data.apikey;
        $root.apikey = data.apikey;
        const def = $.Deferred();
        return $root
            ._loadConfig()
            .then(function () {
                if (!$root.authenticated) {
                    return def.reject("screen.login.error.api_key_invalid");
                }
                return def.resolve();
            })
            .catch(function (error) {
                return def.reject("screen.login.error.api_key_invalid");
            });
    }

    on_logout($root) {
        const def = $.Deferred();
        return def.resolve();
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
            apikey: "",
        };
    },
    methods: {
        login: function (evt) {
            const data = {apikey: this.apikey};
            this.$root.login(evt, data);
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

// TODO: Add translation
// login: {
//     api_key_placeholder: "YOUR_API_KEY_HERE",
//     api_key_label: "API key",
// },
