# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import json

from odoo import SUPERUSER_ID, api


def _compute_logs_new_values(env):
    log_entries = env["shopfloor.log"].search([])
    for entry in log_entries:
        new_vals = {}
        for fname in ("params", "headers", "result"):
            if not entry[fname]:
                continue
            # make it json-like
            val = json.loads(
                entry[fname]
                .replace("'", '"')
                .replace("False", '"false"')
                .replace("None", '"null"')
            )
            new_vals[fname] = json.dumps(val, indent=4, sort_keys=True)
        if entry.error and not entry.exception_name:
            new_vals.update(_get_exception_details(entry))
        entry.write(new_vals)


def _get_exception_details(entry):
    for line in reversed(entry.error.splitlines()):
        if "Error:" in line:
            name, msg = line.split(":", 1)
            return {
                "exception_name": name.strip(),
                "exception_message": msg.strip("() "),
            }


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _compute_logs_new_values(env)
