# Copyright 2021 Camptocamp SA (http://www.camptocamp.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from odoo.addons.component.core import AbstractComponent


class BaseShopfloorService(AbstractComponent):
    _inherit = "base.shopfloor.service"

    # def dispatch(self, method_name, *args, params=None):
    #     self._validate_request(request)
    #     return super().dispatch(method_name, *args, params=params)

    # def _validate_request(self, request):
    #     if self.collection.auth_type == "api_key":
    #         # request api key is already validated when we reach this point
    #         # Now let's validate it at app level.
    #         if not self.request.auth_api_key_id in self.collection._allowed_api_key_ids():
    #             raise Forbidden()
