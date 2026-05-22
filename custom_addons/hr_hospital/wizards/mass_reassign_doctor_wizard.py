from odoo import fields, models


class MassReassignDoctorWizard(models.TransientModel):
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
        patients = self.env['hr_hospital.patient'].browse(
            self.env.context.get('active_ids', [])
        )

        for patient in patients:
            patient.personal_doctor_id = self.doctor_id

            self.env['hr_hospital.doctor.history'].create({
                'patient_id': patient.id,
                'doctor_id': self.doctor_id.id,
                'change_date': self.change_date,
            })

        return {'type': 'ir.actions.act_window_close'}
