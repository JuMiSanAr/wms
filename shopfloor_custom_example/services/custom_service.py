# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from werkzeug.exceptions import BadRequest

from odoo import _

from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component

from ..utils import to_float


class CustomService(Component):
    """
    Methods for the Custom Service Process
    """

    _inherit = "base.shopfloor.process"
    _name = "shopfloor.checkout"
    _usage = "custom_service"
    _description = __doc__

    def scan_partner(self, ref):
        """Scan a partner ref and return its data.
        """
        search = self._actions_for("search")
        picking = search.picking_from_scan(barcode)