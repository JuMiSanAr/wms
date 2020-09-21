Frontend for Shopfloor app.

This frontend is built on top of `VueJS <vuejs.org>`_
and relies on `base_rest <https://github.com/OCA/rest-framework/tree/13.0/base_rest>`_
to "talk" with Odoo.

The whole business logic comes from `shopfloor` module.
This module takes care of providing a nice and reactive UI to work with.

The work is organized in scenario.
A scenario represents a process in the warehouse (eg: receive, deliver).
The app allows to start each process through the main menu.
