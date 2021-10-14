# Copyright 2021 Camptocamp SA (http://www.camptocamp.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.addons.shopfloor_base.controllers.main import ShopfloorController


class APIKeyShopfloorController(ShopfloorController):
    _default_auth = "api_key"
