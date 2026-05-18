import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HospitalDisease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

    parent_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string="Parent Disease"
    )

    child_ids = fields.One2many(
        comodel_name='hr_hospital.disease',
        inverse_name='parent_id',
        string="Child Diseases"
    )

    # перевірка циклів
    @api.constrains('parent_id')
    def _check_no_recursion(self):
        if not self._check_recursion():
            raise ValidationError("Recursive hierarchy is not allowed")

    # відображення ієрархії
    def name_get(self):
        result = []
        for rec in self:
            name = rec.name
            parent = rec.parent_id

            while parent:
                name = f"{parent.name} / {name}"
                parent = parent.parent_id

            result.append((rec.id, name))

        return result

    short_name = fields.Char(
        string="Short Name",
        compute="_compute_short_name"
    )

    def _compute_short_name(self):
        for rec in self:
            rec.short_name = rec.name
