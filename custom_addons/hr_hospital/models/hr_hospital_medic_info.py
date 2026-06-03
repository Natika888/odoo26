from datetime import date

from odoo import api, fields, models


class HospitalMedicInfo(models.AbstractModel):
    """
    Abstract model for storing common medical information.

    This model is inherited by other models (e.g., Patient, Doctor)
    to provide shared fields such as blood group, gender, birthdate,
    and automatically computed age.
    """
    _name = 'hr_hospital.medic.info'
    _description = 'Medical Info'

    blood_group = fields.Selection(
        selection=[
            ('o_pos', 'O(I) Rh+'),
            ('o_neg', 'O(I) Rh-'),
            ('a_pos', 'A(II) Rh+'),
            ('a_neg', 'A(II) Rh-'),
            ('b_pos', 'B(III) Rh+'),
            ('b_neg', 'B(III) Rh-'),
            ('ab_pos', 'AB(IV) Rh+'),
            ('ab_neg', 'AB(IV) Rh-'),
        ],
        string="Blood Group"
    )

    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        string="Gender"
    )

    birth_date = fields.Date(
        string="Birth Date"
    )

    age = fields.Integer(
        string="Age",
        compute="_compute_age",
    )

    @api.depends('birth_date')
    def _compute_age(self):
        """ Compute age based on birthdate.
        Calculates full years difference between today and birthdate.
        If birthdate is not set, age is 0. """
        today = date.today()
        for rec in self:
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year - (
                    (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0
