from odoo import fields, models, api, _
from datetime import datetime, timedelta

QUALIFICATION_STATUS = [
    ("draft", "Draft"),
    ("ongoing", "In Process"),
    ("qualified", "Qualified"),
    ("fail", "Failed")
]


class QualificationProcess(models.Model):
    _name = "qualification.process"
    _description = " Qualification Process with Qualification Steps"

    target_model = fields.Reference(
        selection="_select_target", string="Target", required=True
    )

    status = fields.Selection(selection=QUALIFICATION_STATUS, default="draft")
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    auditor_ids = fields.Many2many(string="Auditors", comodel_name="res.users")
    result = fields.Boolean(string="Qualification Result")
    days_to_expire = fields.Integer(string="", default=365)
    remaining_days = fields.Integer(compute="_compute_remaining_days")

    def _select_target(self):
        return [
            ("res.partner", "Partner"),
            ("maintenance.equipment", "Equipment"),
            ("product.template", "Product"),
        ]
    @api.onchange("days_to_expire")
    def _compute_remaining_days(self):
        for record in self:
            if record.date_end:
                # Calculate the current date
                current_date = datetime.now().date()
                # Calculate the remaining days
                remaining_days = (
                    record.date_end - current_date
                ).days - record.days_to_expire
                # Assign the value to the field
                record.remaining_days = remaining_days if remaining_days > 0 else 0
            else:
                record.remaining_days = 0
