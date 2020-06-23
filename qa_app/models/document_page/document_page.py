# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError, AccessError

class DocumentPage(models.Model):
    _inherit = "document.page"
    tag_id = fields.Many2one('forum.tag', string='Tag Forum', ondelete='restrict')
