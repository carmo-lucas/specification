from odoo import models, fields

class SpecificationParameter(models.Model):
    _name = "spec.parameter"
    _description = "Parameter/Variable of the specification property"

    name = fields.Char("Name", size=32, required=True)
    description = fields.Text()
    uom_id = fields.Many2one("uom.category")
    parameter_type = fields.Selection(
        [
            ("numeric", "Numeric"),
            ("qualitative", "Qualitative"),
        ]
    )
    method = fields.Text("Method Used")
    note = fields.Text(help = "This note will be added to the end of the CoA")