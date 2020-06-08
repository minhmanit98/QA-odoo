# -*- coding: utf-8 -*-
from odoo import fields, models, api , exceptions


class QLDSubjects(models.Model):
    _name = 'utc2.qld.subjects'
    _description = 'Môn'


    def _compute_is_dtl(self):
        list_mon = ['GQP201.3', 'GQP202.2', 'GQP203.3', 'GDT01.1', 'GDT02.1',
                    'GDT03.1', 'GDT03.12', 'GDT04.1', 'GDT05.1', 'ANH01.3', 'ANHA1.4', 'ANHA2.4']
        for record in self:
            if record.name in list_mon:
                record.is_dtl = False

    name = fields.Char('Mã môn', required=True)
    name_display = fields.Char('Tên môn', required=True)
    stc = fields.Integer('Số tín chỉ', required=True)
    parent_id = fields.Many2one('utc2.qld.subjects', string='Môn cha', ondelete='restrict')
    child_ids = fields.One2many('utc2.qld.subjects', 'parent_id', string='Môn con')
    is_dtl = fields.Boolean('Dùng để tính điểm', default=True, compute=_compute_is_dtl, store=True, readonly=False)

    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        return new_record