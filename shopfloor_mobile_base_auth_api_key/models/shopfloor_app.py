# Copyright 2021 Camptcamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ShopfloorApp(models.Models):

    _inherit = "shopfloor.app"

    # TODO: limit auth to specific api keys

    # def _selection_auth_type(self):
    #     return super()._selection_auth_type() + [("api_key", "API key")]

    # # Borrowed from `enddpoint_auth_api_key`: shall we define a mixin?
    # auth_api_key_group_ids = fields.Many2many(
    #     comodel_name="auth.api.key.group",
    #     string="Allowed API key groups",
    # )

    # def _validate_request(self, request):
    #     super()._validate_request(request)
    #     if self.auth_type == "api_key":
    #         self._validate_api_key(request)

    # def _validate_api_key(self, request):
    #     key_id = request.auth_api_key_id
    #     if key_id not in self._allowed_api_key_ids():
    #         self._logger.error("API key %s not allowed on %s", key_id, self.route)
    #         raise werkzeug.exceptions.Forbidden()

    # def _allowed_api_key_ids(self):
    #     return self.auth_api_key_group_ids.auth_api_key_ids.ids
