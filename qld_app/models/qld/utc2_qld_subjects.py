# -*- coding: utf-8 -*-
from odoo import fields, models, api , exceptions


class QLDSubjects(models.Model):
    _name = 'utc2.qld.subjects'
    _description = 'Môn - Điểm'

    name = fields.Char('Mã môn', required=True)
    name_display = fields.Char('Tên môn', required=True)
    stc = fields.Integer(string='Số tín chỉ')
    parent_id = fields.Many2one('utc2.qld.subjects', string='Môn cha', ondelete='restrict')
    child_ids = fields.One2many('utc2.qld.subjects', 'parent_id', string='Môn con')

    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        return new_record

