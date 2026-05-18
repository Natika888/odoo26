import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HospitalVisit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Visit'

    state = fields.Selection(
        [
            ('planned', 'Planned'),
            ('done', 'Done'),
            ('canceled', 'Canceled'),
        ],
        string="Status",
        default='planned',
        required=True,
    )

    planned_datetime = fields.Datetime(
        string="Planned Datetime",
        required=True,
    )

    visit_datetime = fields.Datetime(
        string="Visit Datetime"
    )

    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string="Doctor",
        required=True,
    )

    patient_id = fields.Many2one(
        comodel_name='hr_hospital.patient',
        string="Patient",
        required=True,
    )

    disease_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string="Disease"
    )

    disease_name = fields.Char(
        related='disease_id.name',
        string="Disease",
        store=True
    )

    summary = fields.Html(
        string="Summary"
    )

    active = fields.Boolean(default=True)

    def write(self, vals):
        for rec in self:
            # ❗ заборона архівації
            if 'active' in vals and rec.state == 'done':
                raise ValidationError("You cannot archive completed visits")

            if rec.state == 'done':
                if any(field in vals for field in ['planned_datetime', 'visit_datetime', 'doctor_id']):
                    raise ValidationError("You cannot modify doctor or date for completed visit")

        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError("You cannot delete completed visits")

        return super().unlink()

    def action_done(self):
        for rec in self:
            vals = {'state': 'done'}
            if not rec.visit_datetime:
                vals['visit_datetime'] = fields.Datetime.now()
            rec.write(vals)

    def action_cancel(self):
        for rec in self:
            rec.state = 'canceled'

    def action_set_planned(self):
        for rec in self:
            rec.state = 'planned'

    @api.constrains('doctor_id')
    def _check_doctor_not_intern(self):
        for rec in self:
            if rec.doctor_id and rec.doctor_id.is_intern:
                raise ValidationError("Intern cannot be selected as doctor")
