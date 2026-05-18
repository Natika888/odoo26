from datetime import datetime

from odoo import fields, models


class VisitReportWizard(models.TransientModel):
    _name = 'visit.report.wizard'
    _description = 'Visit Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='hr_hospital.doctor',
        string="Doctors"
    )

    patient_ids = fields.Many2many(
        comodel_name='hr_hospital.patient',
        string="Patients"
    )

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")

    only_done = fields.Boolean(string="Only Completed")

    disease_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string="Disease"
    )

    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])

        if active_model == 'hr_hospital.patient':
            res['patient_ids'] = [(6, 0, active_ids)]

        if active_model == 'hr_hospital.doctor':
            res['doctor_ids'] = [(6, 0, active_ids)]

        return res

    def action_show_visits(self):
        domain = []

        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.date_from:
            domain.append(('planned_datetime', '>=', datetime.combine(self.date_from, datetime.min.time())))

        if self.date_to:
            domain.append(('planned_datetime', '<=', datetime.combine(self.date_to, datetime.max.time())))

        if self.only_done:
            domain.append(('state', '=', 'done'))

        if self.disease_id:
            domain.append(('disease_id', '=', self.disease_id.id))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Visits',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
        }
