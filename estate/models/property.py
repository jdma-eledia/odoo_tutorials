from odoo import api, models, fields
import odoo
import odoo.exceptions
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Test Description"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Datetime.add(fields.Datetime.now(), months=3),
    )
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", copy=False
    )  # Update to res.partner
    seller_id = fields.Many2one(
        "res.users", string="Seller", default=lambda self: self.env.user
    )
    tags_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK (expected_price > 0)",
            "Expected price must be > 0",
        ),
        (
            "check_selling_price",
            "CHECK (selling_price >= 0)",
            "Selling price must be >= 0",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            # Skip check if selling_price is zero
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            # Calculate 90% of expected_price
            min_price = 0.9 * record.expected_price
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise odoo.exceptions.ValidationError(
                    f"Selling price cannot be lower than 90% of the expected price ({min_price})."
                )

    def action_property_sold(self):
        for record in self:
            if record.state == "canceled":
                raise odoo.exceptions.UserError("Canceled properties cannot be sold!")
            else:
                record.state = "sold"
        return True

    def action_property_canceled(self):
        for record in self:
            if record.state == "sold":
                raise odoo.exceptions.UserError("Sold properties cannot be canceled!")
            else:
                record.state = "canceled"
        return True
