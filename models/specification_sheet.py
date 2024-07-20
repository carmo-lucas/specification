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
    version = fields.Integer("Version", default=1, tracking=True)
    user_approved = fields.Many2one("res.users")
    date_approved = fields.Datetime("Date of Approval")
    
    product_id = fields.Many2one("product.product")
    description = fields.Text(string="Description")
    specification_type = fields.Selection(
        string="Type",
        selection=[
            ("chemical", "Chemical"),
            ("physical", "Physical"),
            ("pharma", "Pharmaceutical"),
            ("vegetable", "Vegetable"),
        ],
        required=True,
        default="chemical",
    )
    storage_condition = fields.Many2one("spec.storage_condition", required=True)

    storage_packaging = fields.Text(string="Storage Packaging")

    # Chemical Specifications
    dcb_name = fields.Char("DCB", size=255, trim=False)
    dci_name = fields.Char("DCI", size=255, trim=False)
    cas_name = fields.Char("CAS", size=255, trim=False)
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
