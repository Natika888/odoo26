from odoo.tests.common import TransactionCase


class HospitalTestCommon(TransactionCase):

    def setUp(self):
        super().setUp()

        self.Patient = self.env['hr_hospital.patient']
        self.Visit = self.env['hr_hospital.visit']
        self.Disease = self.env['hr_hospital.disease']
        self.Doctor = self.env['hr_hospital.doctor']

        self.disease = self.Disease.create({
            'name': 'Flu',
        })

        self.doctor = self.Doctor.create({
            'name': 'Test Doctor',
            'is_intern': False,
        })

        self.patient = self.Patient.create({
            'name': 'Test Patient',
        })