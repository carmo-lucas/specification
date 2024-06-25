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
        tracking=True,
    )
    # Version Control
    version  = fields.Integer("Version", default = 1, tracking = True)
    
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
            ("controlled", "Ambient (15 - 20 °C)"),
            ("room", "Ambient (< 30 °C)"),
        ],
        default="controlled",
        required=True
    )

    storage_packaging = fields.Text(string="Storage Packaging")

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

    def request_validation(self):
        self.status = "pending"

    def cancel_specification(self):
        self.status = "canceled"

