# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# Copyright 2021 ACSONE SA/NV (http://www.acsone.eu)
# @author Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class ShopfloorApp(models.Model):
    """Backend for a Shopfloor app."""

    _name = "shopfloor.app"
    _inherit = "collection.base"
    _description = "A Shopfloor application"

    # TODO: attach and load menu items and other records
    # from the specific shopfloor.app (aka current collection)
    name = fields.Char(required=True, translate=True)
    tech_name = fields.Char(required=True)
    active = fields.Boolean(default=True)
