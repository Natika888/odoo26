
from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    color = fields.Integer(string="Color")
    # color = fields.Integer(default=lambda self: random)
    # color = fields.Integer(compute="_compute_color")
