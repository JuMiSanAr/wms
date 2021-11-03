/**
 * Copyright 2021 Camptocamp SA (http://www.camptocamp.com)
 * @author Simone Orsi <simone.orsi@camptocamp.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

import {process_registry} from "/shopfloor_mobile_base/static/wms/src/services/process_registry.js";

const Cart = {
    template: `
        <Screen :screen_info="screen_info">
            <div v-if="has_cart">
                <h3>cart amount: {{ cart.amount.total }}</h3>
                <item-detail-card
                    v-for="line in _.result(cart, 'lines.items', [])"
                    :record="line"
                    :options="{fields: [{path: 'product.name'}, {path: 'amount.price'}, {path: 'qty', label: 'qty'},]}"
                    />
            </div>

        </Screen>
    `,
    data: function () {
        return {
            has_cart: false,
            cart: {},
            user_message: {},
        };
    },
    mounted() {
        if (!_.isEmpty(this.$storage.get("cart"))) {
            this.$set(this, "cart", this.$storage.get("cart"));
            this.has_cart = true;
        }
        const odoo_params = {
            base_url: this.$root.app_info.shop_api_route,
            usage: "cart",
            headers: {},
        };
        if (!_.isEmpty(this.cart)) {
            odoo_params.headers["SESS-CART-ID"] = this.cart.id;
        }
        this.odoo = this.$root.getOdoo(odoo_params);
        this._fetch();
    },
    methods: {
        _fetch: function () {
            const params = {};
            const self = this;
            this.odoo.get("search", params).then((result) => {
                self.$set(this, "cart", result.data || {});
                self.user_message = result.message || null;
            });
        },
    },
    computed: {
        screen_info: function () {
            return {
                title: this.screen_title,
                klass: "shop cart",
                user_message: this.user_message,
            };
        },
        screen_title: function () {
            return this.$t("screen.cart.title");
        },
    },
};

process_registry.add(
    "cart",
    Cart,
    {
        path: "/cart",
    },
    {
        menu: {
            _type: "all",
            name: "Cart",
            id: "cart",
            to: {
                name: "cart",
            },
        },
    }
);

export default Cart;
