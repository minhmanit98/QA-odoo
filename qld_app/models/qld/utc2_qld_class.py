# -*- coding: utf-8 -*-
from odoo import fields, models, api


class QLDClass(models.Model):
    _name = 'utc2.qld.class'
    _description = 'Lớp'

    @api.depends("student_ids")
    def _compute_stc_current(self):
        list_stc = []
        for record in self:
            for student in record.student_ids:
                list_stc.append(student.tong_stc)
            record.stc_current = max(list_stc)
            list_stc = []

    @api.depends("stc_current", "student_ids")
    def _compute_subject_current(self):
        list_mon = []
        for record in self:
            student = self.env['utc2.qld.students'].search([('tong_stc', '=', record.stc_current), ('class_id', '=', record.id)], limit=1)
            scores = self.env['utc2.qld.scores'].search([('student_id', '=', student.id)])
            for subject in scores.subject_id:
                list_mon.append(subject.id)
            record.subject_current = [(6, 0, list_mon)]
            list_mon = []

    @api.depends("parent_id.parent_id")
    def _compute_subject_ids(self):
        for record in self:
            list_mon1 = []
            list_mon2 = []
            for sub in record.subject_current:
                list_mon1.append(sub.id)
            print(record.parent_id)
            for parent_id in record.parent_id:
                for sub in parent_id.subject_current:
                    list_mon2.append(sub.id)
                record.subject_ids = [(6, 0, list(set().union(list_mon1, list_mon2)))]
                print(parent_id.subject_current)
                print(list_mon2)
                record.update_subject_ids = 'Update'



    name = fields.Char('Mã lớp', required=True)
    name_display = fields.Char('Tên lớp')
    student_ids = fields.One2many('utc2.qld.students', 'class_id', string='Sinh viên')
    subject_ids = fields.Many2many('utc2.qld.subjects', 'utc2_qld_class_subjects_rel', 'subject_ids', 'class_ids',
                                   string='Môn')
    parent_id = fields.Many2many('utc2.qld.class', 'parent_id_child_id_rel', 'child_ids', 'parent_id', string='Lớp trên')
    child_ids = fields.Many2many('utc2.qld.class', 'parent_id_child_id_rel', 'parent_id', 'child_ids', string='Lớp dưới')
    stc_current = fields.Integer(string='Số tín chỉ hiện tại', compute=_compute_stc_current, store=True, readonly=False)
    subject_current = fields.Many2many('utc2.qld.subjects', string='Môn đã học',
                                       compute=_compute_subject_current, store=True, readonly=False)

    def write(self, vals):
        list_mon1 = []
        for sub in self.subject_current:
            list_mon1.append(sub.id)
        if vals.get('parent_id'):
            list_mon2 = []
            for parent_id in vals['parent_id'][0][2]:
                subject_current = self.env['utc2.qld.class'].search([('id', '=', parent_id)]).subject_current
                for subject in subject_current:
                    if not (subject.id in list_mon2):
                        list_mon2.append(subject.id)
            vals['subject_ids'] = [(6, 0, list(set().union(list_mon1, list_mon2)))]
        res = super(QLDClass, self).write(vals)
        return res
