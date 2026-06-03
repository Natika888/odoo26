from odoo import fields, models


class MassReassignDoctorWizard(models.TransientModel):
    """
    Wizard for mass reassignment of doctors to patients.

    Allows selecting a new doctor and applying the change
    to multiple selected patients while creating history records.
    """
    _name = 'mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor Wizard'

    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string="New Doctor",
        required=True
    )

    change_date = fields.Date(
        string="Change Date",
        default=fields.Date.today
    )

    def action_apply(self):
        """ Apply doctor reassignment to selected patients.
        Performs the following: - creates doctor history records - updates personal doctor for each patient
        :return: action to close the wizard window """
        patients = self.env['hr_hospital.patient'].browse(
            self.env.context.get('active_ids', [])
        )

        for patient in patients:
            self.env['hr_hospital.doctor.history'].create({
                'patient_id': patient.id,
                'doctor_id': self.doctor_id.id,
                'change_date': fields.Datetime.now(),
            })

        patients.write({
            'personal_doctor_id': self.doctor_id.id
        })

        return {'type': 'ir.actions.act_window_close'}
