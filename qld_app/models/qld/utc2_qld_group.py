# -*- coding: utf-8 -*-
from odoo import fields, models, api , exceptions


class QLDGroup(models.Model):
    _name = 'utc2.qld.group'
    _description = 'Nhóm môn'


    def _compute_is_dtl(self):
        list_mon = ['GQP201.3', 'GQP202.2', 'GQP203.3', 'GDT01.1', 'GDT02.1',
                    'GDT03.1', 'GDT03.12', 'GDT04.1', 'GDT05.1', 'ANH01.3', 'ANHA1.4', 'ANHA2.4']
        for record in self:
            if record.name in list_mon:
                record.is_dtl = False

    name = fields.Char('Nhóm môn', required=True)
    name_display = fields.Char('Tên nhóm môn', required=True)
    subject_ids = fields.One2many('utc2.qld.subjects', 'group_id', string='Môn')

    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        return new_record
