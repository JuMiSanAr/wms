// ***********************************************************
// This example support/index.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import "./commands";

// Alternatively you can use CommonJS syntax:
// require('./commands')

//// CUSTOM ////

// Clears the session storage before running the test suite.
sessionStorage.clear();

// TODO: when we make auth type depend on the shopfloor app backend
// we won't need this anymore.

it("Prepares test suite", () => {
    cy.prepare_test_authentication();
});
