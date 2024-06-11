from odoo import fields, models, api


class ValidateSpecificationSheet(models.TransientModel):
    _name = "validate.spec.sheet"
    _description = "Validation of specification sheet"

    specification_sheet_id = fields.Many2one("spec.sheet")
    comment = fields.Text("Comment", required=True)
    password = fields.Char("Password", required=True)

    # TODO: function not working as expected
    @api.model
    def write_to_thread(self, fields):
        active_id = self.env.context.get("active_id")
        if active_id:
            self.env["spec.sheet"].browse(active_id).message_post(
                body="message working"
            )
            return {"type": "ir.actions.act_window_close"}

    @api.model
    def default_get(self, fields):
        res = super(ValidateSpecificationSheet, self).default_get(fields)
        res["specification_sheet_id"] = self.env.context.get("active_id")
        return res
