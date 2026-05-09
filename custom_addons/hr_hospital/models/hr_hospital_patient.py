import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor')