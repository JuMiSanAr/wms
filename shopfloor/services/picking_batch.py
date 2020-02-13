from odoo.osv import expression

from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component


class PickingBatch(Component):
    """Picking Batch services for the client application."""

    _inherit = "base.shopfloor.service"
    _name = "shopfloor.picking.batch"
    _usage = "picking_batch"
    _expose_model = "stock.picking.batch"
    _description = __doc__

    def _get_base_search_domain(self):
        base_domain = super()._get_base_search_domain()
        user = self.env.user
        return expression.AND(
            [
                base_domain,
                [
                    "|",
                    "&",
                    ("user_id", "=", False),
                    ("state", "=", "draft"),
                    "&",
                    ("user_id", "=", user.id),
                    ("state", "in", ("draft", "in_progress")),
                ],
            ]
        )

    def _search(self, name_fragment=None):
        domain = self._get_base_search_domain()
        if name_fragment:
            domain.append(("name", "ilike", name_fragment))
        records = self.env[self._expose_model].search(domain, order="id asc")
        records = records.filtered(
            # Include done/cancel because we want to be able to work on the
            # batch even if some pickings are done/canceled. They'll should be
            # ignored later.
            lambda batch: all(
                picking.state in ("assigned", "done", "cancel")
                for picking in batch.picking_ids
            )
        )
        # TODO why already convert to json in the internal method?
        return self._to_json(records)

    def search(self, name_fragment=None):
        """List available stock picking batches for current user

        Show only picking batches where all the pickings are available.
        """
        json_records = self._search(name_fragment=name_fragment)
        return self._response(data={"size": len(json_records), "records": json_records})

    def _validator_search(self):
        return {
            "name_fragment": {"type": "string", "nullable": True, "required": False}
        }

    def _validator_return_search(self):
        return self._response_schema(
            {
                "size": {"coerce": to_int, "required": True, "type": "integer"},
                "records": {
                    "type": "list",
                    "required": True,
                    "schema": {"type": "dict", "schema": self._record_return_schema},
                },
            }
        )

    @property
    def _record_return_schema(self):
        return {
            "id": {"coerce": to_int, "required": True, "type": "integer"},
            "name": {"type": "string", "nullable": False, "required": True},
            "picking_count": {"coerce": to_int, "required": True, "type": "integer"},
            "move_line_count": {"coerce": to_int, "required": True, "type": "integer"},
        }

    def _convert_one_record(self, record):
        assigned_pickings = record.picking_ids.filtered(
            lambda picking: picking.state == "assigned"
        )
        return {
            "id": record.id,
            "name": record.name,
            "picking_count": len(assigned_pickings),
            "move_line_count": len(assigned_pickings.mapped("move_line_ids")),
        }