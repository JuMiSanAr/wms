/**
 * Copyright 2021 Camptocamp SA (http://www.camptocamp.com)
 * @author Simone Orsi <simone.orsi@camptocamp.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

import {
    AuthHandlerMixin,
    auth_handler_registry,
} from "/shopfloor_mobile_base/static/wms/src/services/auth_handler_registry.js";

// Provide auth handle for Odoo calls
export class UserAuthHandler extends AuthHandlerMixin {
    // Not sure we need anything if we get a cookie in the same browser
    get_params($root) {
        return {
            /**
             * NOTE: we don't have to provide any param because the auth
             * comes from the cookie.
             * In the future if we want to support cross domain
             * we'll have to provide `credentials` same-origin|include
             * to the fetch method.
             * */

            headers: {},
        };
    }
}
auth_handler_registry.add(new UserAuthHandler("user"));

/**
 * Handle loging via user.
 *
 * Conventional name: `login-` + auth_type (from app config)
 */
Vue.component("login-user", {
    data: function () {
        return {
            error: "",
            username: "",
            password: "",
        };
    },
    // TODO: handle logout throu events and call `/session/auth/logout`
    mounted: function () {
        const self = this;
        // Components can trigger `state:change` on the root
        // and the current state gets stored into `global_state_key`
        this.$root.$on("logout:before", function () {});
    },
    methods: {
        login: function (evt) {
            const self = this;
            evt.preventDefault();
            // Call odoo application load => set the result in the local storage in json
            this.$parent.error = "";
            const odoo = this.$root.getOdoo({base_url: "/session/"});
            const data = {login: this.username, password: this.password};
            odoo.post("auth/login", data, true).then(function (result) {
                self.$root.trigger("login:after");
                self.$root
                    ._loadConfig()
                    .catch((error) => {
                        self._handle_invalid_login();
                    })
                    .then(() => {
                        // TODO: shall we do this in $root._loadRoutes?
                        if (self.$root.authenticated) {
                            self.$router.push({name: "home"});
                        } else {
                            self._handle_invalid_login();
                        }
                    });
            });
        },
        _handle_invalid_login() {
            this.$parent.error = this.$t("screen.login.error.login_invalid");
        },
    },
    template: `
    <v-form v-on:submit="login">
        <v-text-field
            name="username"
            v-model="username"
            :label="$t('screen.login.username')"
            :placeholder="$t('screen.login.username')"
            autofocus
            autocomplete="off"></v-text-field>
        <v-text-field
            name="password"
            v-model="password"
            type="password"
            :label="$t('screen.login.password')"
            :placeholder="$t('screen.login.password')"
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
