import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HospitalVisit(models.Model):
    """
    Model representing a patient visit.

    Stores information about planned and completed visits,
    including doctor, patient, disease, and visit status.
    """
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
        """ Restrict modifications for completed visits.
        Prevents: - archiving completed visits - changing doctor or dates for completed visits
        :param vals: values to update
        :raises ValidationError: if modification is not allowed """
        for rec in self:
            if 'active' in vals and rec.state == 'done':
                raise ValidationError("You cannot archive completed visits")

            if rec.state == 'done':
                if any(field in vals for field in ['planned_datetime', 'visit_datetime', 'doctor_id']):
                    raise ValidationError("You cannot modify doctor or date for completed visit")

        return super().write(vals)

    def unlink(self):
        """ Prevent deletion of completed visits.
        :raises ValidationError: if trying to delete a completed visit """
        for rec in self:
            if rec.state == 'done':
                raise ValidationError("You cannot delete completed visits")

        return super().unlink()

    def action_done(self):
        """ Mark visit as done and set visit datetime if not provided. """
        for rec in self:
            vals = {'state': 'done'}
            if not rec.visit_datetime:
                vals['visit_datetime'] = fields.Datetime.now()
            rec.write(vals)

    def action_cancel(self):
        """ Mark visit as canceled. """
        for rec in self:
            rec.state = 'canceled'

    def action_set_planned(self):
        """ Set visit state back to planned. """
        for rec in self:
            rec.state = 'planned'

    def action_open_same_disease_visits(self):
        """ Open list of visits with the same disease.
        :return: action dictionary """
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Visits with same disease',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'list,form',
            'domain': [('disease_id', '=', self.disease_id.id)],
        }


    @api.constrains('doctor_id')
    def _check_doctor_not_intern(self):
        """ Prevent assigning interns as doctors for visits.
        :raises ValidationError: if selected doctor is an intern """
        for rec in self:
            if rec.doctor_id and rec.doctor_id.is_intern:
                raise ValidationError("Intern cannot be selected as doctor")