from odoo import models, fields, _


class SpecificationMethod(models.Model):
    _name = "spec.method"
    _description = "Test method for give parameter"

    parameter_id = fields.Many2one("spec.parameter")

    name = fields.Text(string="Method Name")
    description = fields.Text(string="Description")
    reference = fields.Text(string="Bibliography reference")
