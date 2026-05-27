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

    intern_ids = fields.One2many(
        comodel_name='hr_hospital.doctor',
        inverse_name='mentor_id',
        string="Interns"
    )

    intern_names = fields.Char(
        string="Intern Names",
        compute="_compute_intern_names"
    )

    @api.depends('category_id')
    def _compute_is_intern(self):
        intern_category = self.env.ref(
            'hr_hospital.doctor_category_intern',
            raise_if_not_found=False
        )

        for rec in self:
            rec.is_intern = bool(
                intern_category and rec.category_id == intern_category
            )

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor(self):
        for record in self:
            if record.is_intern and not record.mentor_id:
                raise ValidationError("Інтерн повинен мати ментора")

            if record.mentor_id and record.mentor_id.is_intern:
                raise ValidationError("Ментор не може бути інтерном")

    def action_create_visit(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_doctor_id': self.id,
            }
        }

    def _compute_intern_names(self):
        for rec in self:
            rec.intern_names = ', '.join(rec.intern_ids.mapped('name'))
