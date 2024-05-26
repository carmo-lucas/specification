from odoo import models, fields, api, _


class SpecificationSheet(models.Model):
    _name = "spec.sheet"
    _description = "Technical Specification of the Product"
    _inherit = ['mail.thread','mail.activity.mixin']

    product_id = fields.Many2one("product.product")
    technical_name = fields.Text("Product Technical Name")
    cas_name = fields.Char("CAS", size=20, trim=False)
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("validated", "Validated"),
            ("canceled", "Canceled"),
        ],
        default="draft",
    )
    classe_SNGPC = fields.Selection(
        string="Classe SNGPC",
        selection=[("1", "Controle Especial"), ("2", "Antimicrobiano")],
    )
    # Biopharmaceutical Classification System
    bcs = fields.Selection(
        string="Biopharmaceutical Classification",
        selection=[
            ("1", "I"),
            ("2", "II"),
            ("3", "III"),
            ("4", "IV"),
        ],
    )
    observations = fields.Text(string="Observations")

    # schedule_ids = fields.Many2many(
    #     "rx.drug.schedule",
    #     string="Drug Schedule",
    #     help="Drug Regulatory Classification According to Health Surveilance Agencies",
    # )

    property_ids = fields.One2many(
        "spec.property", "spec_sheet_id", string="Properties"
    )


class SpecificationProperty(models.Model):
    _name = "spec.property"
    _description = "Properties listed in Specification Sheet"
    spec_sheet_id = fields.Many2one("spec.sheet")
    parameter_id = fields.Many2one("spec.parameter")
    parameter_target_value = fields.Float("Target", digits=(12,4))
    parameter_tolerance_value = fields.Float("Tolerance", digits=(12,4))
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
        self.ensure_one()
        for rec in self:
            if rec.operator == "characteristic":
                continue

    @api.depends("parameter_target_value", "parameter_tolerance_value", "operator")
    def _compute_value_range(self):
        self.ensure_one()
        for rec in self:
            range_min = self.parameter_target_value - self.parameter_tolerance_value
            range_max = self.parameter_target_value + self.parameter_tolerance_value
            if rec.parameter_target_value:
                if rec.operator == "equal":
                    range = (str(range_min), str(range_max))
                    rec.parameter_range_value = " - ".join(range)
                if rec.operator == "lt":
                    range = str(range_max)
                    rec.parameter_range_value = "< " + range
                if rec.operator == "le":
                    range = str(range_max)
                    rec.parameter_range_value = "<= " + range
                if rec.operator == "gt":
                    range = str(range_min)
                    rec.parameter_range_value = "> " + range
                if rec.operator == "ge":
                    range = str(range_min)
                    rec.parameter_range_value = ">= " + range
            else:
                rec.parameter_range_value = ""
        return rec.parameter_range_value


class SpecificationPropertiesTemplate(models.Model):
    _name = "spec.properties.template"
    _description = "Templates for specification parameters"
    property_ids = fields.One2many(
        "spec.property", "spec_sheet_id", string="Properties"
    )


class SpecificationParameter(models.Model):
    _name = "spec.parameter"
    _description = "Parameter/Variable of the specification property"

    name = fields.Char("Name", size=32, required=True)
    description = fields.Text()
    uom_id = fields.Many2one("uom.uom")
    parameter_type = fields.Selection(
        [
            ("numeric", "Numeric"),
            ("qualitative", "Qualitative"),
        ]
    )
    method = fields.Text(string = "Method")
