# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# Copyright 2021 ACSONE SA/NV (http://www.acsone.eu)
# @author Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class ShopfloorApp(models.Model):
    """
    """
    _name = "shopfloor.app"
    _inherit = "collection.base"
    _description = "A Shopfloor application"

    name = fields.Char(required=True, translate=True)
    tech_name = fields.Char(required=True)
    active = fields.Boolean(default=True)
