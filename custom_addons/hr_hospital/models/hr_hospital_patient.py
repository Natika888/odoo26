import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient'
    _inherit = ['hr_hospital.medic.info']

    name = fields.Char(string='Name', required=True)
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor')

    personal_doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string="Personal Doctor"
    )

    doctor_history_ids = fields.One2many(
        comodel_name='hr_hospital.doctor.history',
        inverse_name='patient_id',
        string="Doctor History"
    )

    insurance_policy = fields.Char(
        string="Insurance Policy",
        size=20
    )
