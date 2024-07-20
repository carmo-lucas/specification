from odoo import models, fields


class SpecificationStorageCondition(models.Model):
    _name = "spec.storage_condition"
    _description = "Storage Conditions"

    name = fields.Text("Name")
    description = fields.Text("Description")