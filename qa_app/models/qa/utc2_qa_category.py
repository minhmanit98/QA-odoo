from odoo import fields, models, api


class CategoryQA (models.Model):
    _name = 'utc2.qa.category'
    _description = 'Question and Answer Category'
    _parent_store = True

    name = fields.Char(translate=True, required=True)
    # Hierarchy fields
    username = fields.Many2many('res.partner', string='Username')
    parent_id = fields.Many2one(
        'utc2.qa.category',
        string='Parent Category',
        ondelete='restrict',
    )
    parent_path = fields.Char(index=True)

    # Optional, but good to have
    child_ids = fields.One2many(
        'utc2.qa.category',
        'parent_id',
        string='Subcategories',
    )

    highlighted_id = fields.Reference(
        [('utc2.qa', 'QA')],
        'Category Highlight',
    )


    


