from odoo import fields, models, api
from odoo.exceptions import UserError

class SpecificationProperty(models.Model):
    _name = "spec.property"
    _description = "Properties listed in Specification Sheet"
    spec_sheet_id = fields.Many2one("spec.sheet")
    parameter_id = fields.Many2one("spec.parameter")
    parameter_method = fields.Many2one("spec.method")
    parameter_target_value = fields.Float("Target", digits=(12, 4))
    parameter_tolerance_value = fields.Float("Tolerance", digits=(12, 4))
    parameter_range_value = fields.Char(
        string="Reference Value",
        compute="_compute_value_range",
        inverse="_set_value_range",
        store=True,
    )
    uom_id = fields.Many2one("uom.uom")
    operator = fields.Selection(
        [
            ("characteristic", "Characteristic"),
            ("lt", "<"),
            ("gt", ">"),
            ("le", "<="),
            ("ge", ">="),
            ("equal", " = "),
        ],
        default="equal",
        string="Mode",
    )

    @api.depends("operator")
    def _set_value_range(self):
        for rec in self:
            if rec.operator == "characteristic":
                continue

    @api.depends("parameter_target_value", "parameter_tolerance_value", "operator")
    def _compute_value_range(self):
        for rec in self:
            # if rec.parameter_target_value < rec.parameter_tolerance_value:
            #     raise UserError("The tolerance value cannot be bigger than the target value")
            range_min = round(
                rec.parameter_target_value - rec.parameter_tolerance_value, 6
            )
            range_max = round(
                rec.parameter_target_value + rec.parameter_tolerance_value, 6
            )
            if rec.parameter_target_value:
                operator_map = {
                    "equal": f"{range_min} - {range_max}",
                    "lt": f"< {range_max}",
                    "le": f"<= {range_max}",
                    "gt": f"> {range_min}",
                    "ge": f">= {range_min}",
                }
                range_str = operator_map.get(rec.operator, "")
                rec.parameter_range_value = range_str
            else:
                rec.parameter_range_value = ""
