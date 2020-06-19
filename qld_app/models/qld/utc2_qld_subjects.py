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
    group_id = fields.Many2one('utc2.qld.group', string='Nhóm môn', ondelete='restrict')
    predict_subject_ids = fields.One2many('utc2.qld.predict.subjects', 'subject_id', string='Công thức dự đoán')
    is_dtl = fields.Boolean('Dùng để tính điểm', default=True, compute=_compute_is_dtl, store=True, readonly=False)

    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        return new_record

    def name_get(self):
        return [(rec.id, "%s / %s" % (rec.name, rec.name_display)) for rec in self]

    def action_group_subject(self):
        group_name = self.name[0:3]
        if not self.group_id:
            if self.env['utc2.qld.group'].search_count([('name', '=', group_name)]) > 0:
                self.group_id = self.env['utc2.qld.group'].search([('name', '=', group_name)]).id
            else:
                group_id = self.env['utc2.qld.group'].create({
                    'name': group_name,
                    'name_display': group_name,
                })
                self.group_id = group_id

