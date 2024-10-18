from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type Model"
    _order = "name"

    name = fields.Char(required=True)
    _sql_constraints = [
        ("check_unique_type", "UNIQUE(name)", "Type name must be unique")
    ]
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties", copy=False
    )
