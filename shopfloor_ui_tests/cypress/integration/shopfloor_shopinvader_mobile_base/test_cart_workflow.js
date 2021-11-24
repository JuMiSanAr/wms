describe("Tests the catalog, cart and sale orders in the app", () => {
    before(() => {
        cy.visit(Cypress.config("baseUrl"));

        // TODO: make it work for apikey as well.
        cy.get_credentials("demo_user", "user").then((credentials) => {
            cy.login([
                {name: "username", value: credentials.username},
                {name: "password", value: credentials.password},
            ]);
            cy.get("[data-ref=profile-not-ready]").find("button").click();
            cy.contains("Profile -", {matchCase: false}).click();
            cy.get("input[value=1]").parent().click();
        });
    });

    beforeEach(() => {
        Cypress.Cookies.preserveOnce("session_id");
    });

    after(() => {
        cy.logout();
    });

    describe("Catalog tests", () => {
        it("Opens the catalog", () => {
            intercept_products_request();
            cy.get("div[class='main-content']").contains("Catalog").click();
            cy.wait_for({expect_success: true, request_name: "products_data"}).then(
                (res) => {
                    Cypress.env("test_products", res.response.body.data);
                }
            );
        });

        it("Checks that the expected products appear in the list", () => {
            const products = Cypress.env("test_products");
            products.forEach((product) => {
                cy.get(`div[data-id='${product.id}']`);
            });
        });

        it("Adds one unit of the first product to cart", () => {
            const first_product_id = Cypress.env("test_products")[0].id;
            cy.get(`div[data-id='${first_product_id}']`)
                .find("[data-ref='add-to-cart']")
                .click();
        });

        it("Clicks on the first product and makes sure only that one appears in the screen", () => {
            const first_product_id = Cypress.env("test_products")[0].id;
            cy.get(`div[data-id='${first_product_id}']`)
                .find("[data-ref='card-image']")
                .click();
            cy.get("[data-ref='product-detail']").should(
                "have.attr",
                "data-id",
                first_product_id
            );
        });

        it("Adds another unit to cart", () => {
            cy.get("[data-ref='add-to-cart']").click();
        });
    });
    describe("Cart tests", () => {
        // TODO: test that different products appear in the cart
        // TODO: test that the quantities can be changed directly in the cart
        // TODO: test checkout
        it("Goes to cart", () => {
            cy.sidebar_menu_to("cart");
        });
        it("Checks that two units of the product were added to the cart", () => {
            const first_product_id = Cypress.env("test_products")[0].id;
            cy.get("[data-ref='cart-item']")
                .should("have.attr", "data-id", first_product_id)
                .find("[data-ref='quantity']")
                .invoke("text")
                .then((text) => {
                    if (!text.includes("2")) {
                        throw new Error(
                            "The expected product quantity (2) doesn't correspond to the quantity in the cart"
                        );
                    }
                });
        });
    });

    describe("Orders tests", () => {
        it("Goes to orders", () => {
            intercept_orders_request();
            cy.sidebar_menu_to("orders");
            cy.wait_for({expect_success: true, request_name: "orders_data"}).then(
                (res) => {
                    Cypress.env("test_orders", res.response.body.data);
                }
            );
        });

        it("Checks that the expected orders appear in the list", () => {
            const orders = Cypress.env("test_orders");
            orders.forEach((order) => {
                cy.get(`div[data-id='${order.id}']`);
            });
        });

        it("Clicks on the first order and makes sure only that one appears in the screen", () => {
            const first_order_id = Cypress.env("test_orders")[0].id;
            cy.get(`div[data-id='${first_order_id}']`).click();
            cy.get("[data-ref='order-detail']").should(
                "have.attr",
                "data-id",
                first_order_id
            );
        });
    });
});

// Test-specific functions

const intercept_products_request = () => {
    cy.intercept({
        method: "GET",
        url: "**/invader/products/search?",
    }).as("products_data");
};

const intercept_orders_request = () => {
    cy.intercept({
        method: "GET",
        url: "**/invader/sales/search?",
    }).as("orders_data");
};
