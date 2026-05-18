import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'
    _inherit = ['hr_hospital.medic.info']

    name = fields.Char(string='Name', required=True)
    specialization = fields.Char(string='Specialization')

    category_id = fields.Many2one(
        comodel_name='hr_hospital.doctor.category',
        string="Category"
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User"
    )

    is_intern = fields.Boolean(
        string="Is Intern",
        compute="_compute_is_intern",
        store=True
    )

    mentor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string="Mentor",
        domain=[('is_intern', '=', False)]
    )

    @api.depends('category_id')
    def _compute_is_intern(self):
        for rec in self:
            rec.is_intern = rec.category_id and rec.category_id.name == 'Лікар-інтерн'

    @api.constrains('is_intern', 'mentor_id')
    def _check_mentor(self):
        for rec in self:
            if rec.is_intern and not rec.mentor_id:
                raise ValidationError("Intern must have a mentor")
