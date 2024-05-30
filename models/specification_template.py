from odoo import models, fields

class SpecificationPropertiesTemplate(models.Model):
    _name = "spec.properties.template"
    _description = "Templates for specification parameters"
    property_ids = fields.One2many(
        "spec.property", "spec_sheet_id", string="Properties"
    )
