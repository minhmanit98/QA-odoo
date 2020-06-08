# -*- coding: utf-8 -*-
from odoo import fields, models, api


class QLDClass(models.Model):
    _name = 'utc2.qld.class'
    _description = 'Lớp'

    name = fields.Char('Mã lớp', required=True)
    name_display = fields.Char('Tên lớp')
    student_ids = fields.One2many('utc2.qld.students', 'class_id', string='Sinh viên')
    subject_ids = fields.One2many('utc2.qld.subjects', 'name', string='Môn')
    parent_id = fields.Many2one('utc2.qld.class', string='Lớp trên', ondelete='restrict')
    child_ids = fields.One2many('utc2.qld.class', 'parent_id', string='Lớp dưới')
