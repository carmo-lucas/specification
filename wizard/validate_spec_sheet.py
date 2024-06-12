from odoo import fields, models, api
from markupsafe import Markup


class ValidateSpecificationSheet(models.TransientModel):
    _name = "validate.spec.sheet"
    _description = "Validation of specification sheet"

    specification_sheet_id = fields.Many2one("spec.sheet")
    comment = fields.Text("Comment", required=True)
    password = fields.Char("Password", required=True)



    @api.model
    def default_get(self, fields):
        res = super(ValidateSpecificationSheet, self).default_get(fields)
        res["specification_sheet_id"] = self.env.context.get("active_id")
        return res

    # TODO: comment returning as False

    def write_to_thread(self):
        active_id = self.env.context.get("active_id")
        if active_id:
            self.env["spec.sheet"].browse(active_id).message_post(
                body=Markup(f"<b>{self.env.user.name}</b> has validated this specification with password.<br><b>Comment:</b> <i>'{self.comment}</i>'")
            )
            return {"type": "ir.actions.act_window_close"}