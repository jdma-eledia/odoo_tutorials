from odoo import models, fields


class Property(models.Model):
    _name = "estate.property.tag"
    _description = "These are Tags like cozy"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [("check_unique_tag", "UNIQUE(name)", "Tag name must be unique")]
