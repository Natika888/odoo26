import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Name', required=True)
    specialization = fields.Char(string='Specialization')