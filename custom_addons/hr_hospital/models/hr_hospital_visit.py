import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HospitalVisit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Visit'

    patient_id = fields.Many2one('hr_hospital.patient', string='Patient')
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor')
    disease_id = fields.Many2one('hr_hospital.disease', string='Disease')
    visit_date = fields.Date(string='Visit Date')
