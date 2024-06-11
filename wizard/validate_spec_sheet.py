from odoo import fields, models

class ValidateSpecificationSheet(models.TransientModel):
    _name = "validate.spec.sheet"
    _description = "Validation of specification sheet"

    description = fields.Char("Description", required = True)
    password = fields.Char("password", required = True)
# TODO: function not working as expected
    def write_to_thread(self):
        message = f"Name:{self.name} validated this specification using the password with the description: {self.description}"
        self.message_post(body=message)
        return True
