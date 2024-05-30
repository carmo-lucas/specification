from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SpecificationSheet(models.Model):
    _name = "spec.sheet"
    _description = "Technical Specification of the Product"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # General Information
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending", "Pending"),
            ("validated", "Validated"),
            ("canceled", "Canceled"),
        ],
        default="draft",
    )
    product_id = fields.Many2one("product.product")
    technical_name = fields.Text("Technical Name")
    description = fields.Text(string="Description")
    specification_type = fields.Selection(
        string="Type",
        selection=[
            ("chemical", "Chemical"),
            ("physical", "Physical"),
            ("pharma", "Pharmaceutical"),
        ],
        required=True,
        default="chemical",
    )
    storage_condition = fields.Selection(
        string="Storage condition",
        selection=[
            ("cool", "Refrigerated (2 - 8 °C)"),
            ("room", "Ambient (< 30 °C)"),
            ("controlled", "Ambient (15 - 20 °C)"),
        ],
        default="room",
        required=True,
    )
    # Chemical Specifications
    cas_name = fields.Char("CAS", size=20, trim=False)
    molecular_weight = fields.Float("Mw")

    # Pharmaceutical Specifications
    classe_SNGPC = fields.Selection(
        string="Classe SNGPC",
        selection=[("1", "Controle Especial"), ("2", "Antimicrobiano")],
    )
    ## Biopharmaceutical Classification System
    bcs = fields.Selection(
        string="Biopharmaceutical Classification",
        selection=[
            ("1", "I"),
            ("2", "II"),
            ("3", "III"),
            ("4", "IV"),
        ],
    )

    property_ids = fields.One2many(
        "spec.property", "spec_sheet_id", string="Properties"
    )


class SpecificationProperty(models.Model):
    _name = "spec.property"
    _description = "Properties listed in Specification Sheet"
    spec_sheet_id = fields.Many2one("spec.sheet")
    parameter_id = fields.Many2one("spec.parameter")
    parameter_method = fields.Many2one("spec.method")
    parameter_target_value = fields.Float("Target", digits=(12, 4))
    parameter_tolerance_value = fields.Float("Tolerance", digits=(12, 4))
    parameter_range_value = fields.Char(
        string="Acceptance Value",
        compute="_compute_value_range",
        inverse="_set_value_range",
        store=True,
    )
    uom_id = fields.Many2one(related="parameter_id.uom_id")
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
            if rec.parameter_target_value < rec.parameter_tolerance_value:
                raise UserError("The tolerance value cannot be bigger than the target value")
            range_min = round(
                rec.parameter_target_value - rec.parameter_tolerance_value, 6
            )
            range_max = round(
                rec.parameter_target_value + rec.parameter_tolerance_value, 6
            )
            if rec.parameter_target_value:
                if rec.operator == "equal":
                    range_str = f"{range_min} - {range_max}"
                elif rec.operator == "lt":
                    range_str = f"< {range_max}"
                elif rec.operator == "le":
                    range_str = f"<= {range_max}"
                elif rec.operator == "gt":
                    range_str = f"> {range_min}"
                elif rec.operator == "ge":
                    range_str = f">= {range_min}"
                else:
                    range_str = ""
                rec.parameter_range_value = range_str
            else:
                rec.parameter_range_value = ""
