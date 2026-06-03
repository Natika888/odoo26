from .common import HospitalTestCommon
from odoo.tests import tagged

@tagged('post_install', 'at_install')
class TestPatient(HospitalTestCommon):

    def test_create_sets_user(self):
        patient = self.Patient.create({
            'name': 'New Patient',
        })

        self.assertEqual(patient.user_id, self.env.user)

    def test_action_create_visit(self):
        action = self.patient.action_create_visit()

        self.assertEqual(action['res_model'], 'hr_hospital.visit')
        self.assertEqual(action['context']['default_patient_id'], self.patient.id)