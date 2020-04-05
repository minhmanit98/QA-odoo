# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Tags(models.Model):
    _inherit = "forum.tag"
    parent_id = fields.Many2one('forum.tag', string='Parent Tag', ondelete='restrict')
    parent_path = fields.Char(index=True)
    # Optional, but good to have
    child_ids = fields.One2many('forum.tag', 'parent_id', string='Subtag')
    highlighted_id = fields.Reference([('forum.post', 'Post')], 'Tags Highlight')