from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctorHistory(models.Model):
    _name = 'hr_hospital.doctor.history'
    _description = 'Doctor History'

    patient_id = fields.Many2one(
        comodel_name='hr_hospital.patient',
        string="Patient",
        required=True
    )

    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string="Doctor",
        required=True
    )

    assign_date = fields.Date(
        string="Assign Date",
        required=True,
        default=fields.Date.today
    )

    change_date = fields.Date(
        string="Change Date"
    )

    active = fields.Boolean(
        string="Active",
        default=True
    )

    # display_name = fields.Char(compute='_compute_display_name')

    @api.onchange('assign_date', 'change_date')
    def _onchange_dates(self):
        if self.assign_date and self.change_date:
            if self.change_date < self.assign_date:
                raise ValidationError(
                    "Дата зміни лікаря не може бути раніше ніж дата призначення"
                )

    @api.depends('patient_id', 'doctor_id', 'assign_date')
    def _compute_display_name(self):
        for rec in self:
            patient = rec.patient_id.name or ''
            doctor = rec.doctor_id.name or ''
            category = rec.doctor_id.category_id.name or ''
            date = rec.assign_date or ''

            rec.display_name = f"{patient} - {doctor} ({category}) {date}"
