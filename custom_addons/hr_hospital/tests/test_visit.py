from odoo.exceptions import ValidationError
from .common import HospitalTestCommon
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestVisit(HospitalTestCommon):
    """
    Test cases for HospitalVisit model.

    Covers visit state transitions and validation rules.
    """

    def test_action_done_sets_datetime(self):
        """ Test that action_done:
        - sets state to 'done' - assigns visit_datetime if it was not set """
        visit = self.Visit.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'disease_id': self.disease.id,
            'planned_datetime': '2024-01-01 10:00:00',
        })

        visit.action_done()

        self.assertEqual(visit.state, 'done')
        self.assertTrue(visit.visit_datetime)

    def test_cannot_modify_done_visit(self):
        """ Test that completed visits cannot be modified.
        Ensures that write operation raises ValidationError if trying to change planned datetime after visit is done. """
        visit = self.Visit.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_datetime': '2024-01-01 10:00:00',
        })

        visit.action_done()

        with self.assertRaises(ValidationError):
            visit.write({'planned_datetime': '2025-01-01 10:00:00'})

