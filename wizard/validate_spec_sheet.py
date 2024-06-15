from odoo import fields, models, api, _
from markupsafe import Markup
from odoo.exceptions import UserError, AccessDenied


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

    def write_to_thread(self):
        # Get the active specification sheet ID from the context
        active_id = self.env.context.get("active_id")

        # Verify the provided password
        try:
            self.env['res.users']._check_credentials(self.password, {'interactive': True})
        except AccessDenied:
            raise UserError(_("Invalid password"))

        # Post the message if password is correct
        if active_id:
            rec = self.env["spec.sheet"].browse(active_id)
            rec.message_post(
                body=Markup(
                    f"{self.env.user.name} has validated this specification with password.<br><b>Comment:</b> <i>'{self.comment}'</i>"
                )
            )
            rec.status = "validated"
            return {"type": "ir.actions.act_window_close"}
