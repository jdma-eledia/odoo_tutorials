from datetime import timedelta
from odoo import api, models, fields


class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "this is the offer model"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline")

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )
