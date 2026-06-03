from odoo import fields, models


class DiseaseReportWizard(models.TransientModel):
    """
    Wizard for generating disease-based visit reports.

    Allows filtering visits by:
    - doctors
    - diseases
    - date range

    Results are displayed grouped by disease.
    """
    _name = 'hr_hospital.disease.report.wizard'
    _description = 'Disease Report Wizard'

    doctor_ids = fields.Many2many(
        'hr_hospital.doctor',
        string="Doctors"
    )

    disease_ids = fields.Many2many(
        'hr_hospital.disease',
        string="Diseases"
    )

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")

    def action_show_report(self):
        """ Generate and display filtered visit report.
        Builds domain based on selected filters and opens visit records grouped by disease.
        :return: action dictionary for opening report view """
        self.ensure_one()

        domain = []

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        if self.date_from:
            domain.append(('planned_datetime', '>=', self.date_from))

        if self.date_to:
            domain.append(('planned_datetime', '<=', self.date_to))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Visits Report',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {
                'group_by': ['disease_id']
            }
        }