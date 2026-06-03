from odoo import fields, models


class HospitalDoctorCategory(models.Model):
    """
    Model representing doctor categories.

    Categories are used to classify doctors (e.g., Surgeon, Therapist, Intern)
    and help organize them within the system.
    """
    _name = 'hr_hospital.doctor.category'
    _description = 'Doctor Category'
    _order = 'sequence, name'

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=10)

    doctor_ids = fields.One2many(
        comodel_name='hr_hospital.doctor',
        inverse_name='category_id',
        string="Doctors"
    )

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Category name must be unique!')
    ]
