from odoo import models, fields


class Property(models.Model):
    _name = "estate.property.tag"
    _description = "These are Tags like cozy"

    name = fields.Char(required=True)

    _sql_constraints = [("check_unique_tag", "UNIQUE(name)", "Tag name must be unique")]
