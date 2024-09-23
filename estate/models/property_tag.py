from odoo import models, fields


class Property(models.Model):
    _name = "estate.property.tag"
    _description = "These are Tags like cozy"

    name = fields.Char(required=True)
