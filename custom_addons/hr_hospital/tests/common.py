from odoo.tests.common import TransactionCase


class HospitalTestCommon(TransactionCase):
    """
    Common test class for HR Hospital module.

    Provides shared test data and model references
    for other test cases (patients, doctors, visits, diseases).
    """

    def setUp(self):
        """ Initialize common test data.
        Creates: - test disease - test doctor - test patient
        Also prepares model references for reuse in tests. """
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