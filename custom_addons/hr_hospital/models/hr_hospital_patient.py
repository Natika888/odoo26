import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient'
    _inherit = ['hr_hospital.medic.info']

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string="Phone")

    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor')

    personal_doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string="Personal Doctor"
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User"
    )

    doctor_history_ids = fields.One2many(
        comodel_name='hr_hospital.doctor.history',
        inverse_name='patient_id',
        string="Doctor History"
    )

    insurance_policy = fields.Char(
        string="Insurance Policy",
        size=20
    )

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('user_id'):
                vals['user_id'] = self.env.user.id
        return super().create(vals_list)
    #check
    # def create(self, vals):
    #     if not vals.get('user_id'):
    #         vals['user_id'] = self.env.user.id
    #     return super().create(vals)

    def action_open_patient_visits(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Patient Visits',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
        }

    def action_create_visit(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_patient_id': self.id,
            }
        }
