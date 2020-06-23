# -*- coding: utf-8 -*-
from odoo import fields, models, api


class QLDScores(models.Model):
    _name = 'utc2.qld.scores'
    _description = 'Điểm'

    name = fields.Char(string='Tên', store=True)
    scores_8 = fields.Float(string='Điểm số', readonly=True)
    scores_word = fields.Float(string='Điểm chữ', readonly=True)
    scores_4 = fields.Float(string='Điểm tích lũy', readonly=True, store=True)
    scores_4custom = fields.Float(string='Điểm tích lũy tùy chỉnh', default=5.5)
    student_id = fields.Many2one('utc2.qld.students', string='MSV', ondelete='cascade')
    subject_id = fields.Many2one('utc2.qld.subjects', string='Môn')
    subject_name = fields.Char('Tên môn', related="subject_id.name_display")
    subject_stc = fields.Integer('Số tín chỉ', related="subject_id.stc", store=True)

    def name_get(self):
        return [(rec.id, "%s/%s/%s/%s" % (rec.subject_id.name, rec.subject_id.name_display, rec.subject_id.stc, str(rec.scores_8))) for rec in self]

    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        return new_record