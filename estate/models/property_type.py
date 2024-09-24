from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type Model"

    name = fields.Char(required=True)
    _sql_constraints = [
        ("check_unique_type", "UNIQUE(name)", "Type name must be unique")
    ]
