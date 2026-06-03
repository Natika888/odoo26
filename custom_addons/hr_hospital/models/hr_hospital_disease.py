import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HospitalDisease(models.Model):
    """
    Model representing a disease classification.

    Supports hierarchical structure of diseases using parent-child relationships.
    This allows grouping diseases into categories and subcategories.
    """
    _name = 'hr_hospital.disease'
    _description = 'Disease'

    _parent_name = "parent_id"
    _parent_store = True

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

    parent_path = fields.Char(index=True)

    @api.constrains('parent_id')
    def _check_no_recursion(self):
        """
        Prevent recursive hierarchy in diseases.

        Ensures that a disease cannot be its own ancestor,
        avoiding infinite loops in parent-child relationships.

        :raises ValidationError: if recursion is detected
        """
        if not self._check_recursion():
            raise ValidationError("Recursive hierarchy is not allowed")

    def name_get(self):
        """
        Customize display name of diseases.

        Builds a full hierarchical name including parent diseases,
        e.g. "Parent / Child / Subchild".

        :return: list of tuples (id, display_name)
        """
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
        """
        Compute short name for disease.

        Currently duplicates the main name, but can be extended
        for abbreviations or simplified labels.

        :return: None
        """
        for rec in self:
            rec.short_name = rec.name
