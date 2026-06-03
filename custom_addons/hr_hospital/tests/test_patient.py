from .common import HospitalTestCommon
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestPatient(HospitalTestCommon):
    """
    Test cases for HospitalPatient model.

    Covers patient creation logic and related actions.
    """

    def test_create_sets_user(self):
        """ Test that user_id is automatically assigned on patient creation.
        If user_id is not provided, it should default to the current user. """
        patient = self.Patient.create({
            'name': 'New Patient',
        })

        self.assertEqual(patient.user_id, self.env.user)

    def test_action_create_visit(self):
        """ Test that action_create_visit returns correct action dictionary.
        Ensures: - correct model is opened - patient is passed in context as default value """
        action = self.patient.action_create_visit()

        self.assertEqual(action['res_model'], 'hr_hospital.visit')
        self.assertEqual(action['context']['default_patient_id'], self.patient.id)