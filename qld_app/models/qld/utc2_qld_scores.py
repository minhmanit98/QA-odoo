# -*- coding: utf-8 -*-
from odoo import fields, models, api


class QLDScores(models.Model):
    _name = 'utc2.qld.scores'
    _description = 'Điểm'

    def _compute_name(self):
        for record in self:
            record.name = str(record.student_id.name) + '/' + str(record.subject_id.name) + '/' + str(record.scores_8)

    name = fields.Char(string='Tên', compute=_compute_name, store=True)
    scores_8 = fields.Float(string='Điểm số', readonly=True)
    scores_word = fields.Float(string='Điểm chữ', readonly=True)
    scores_4 = fields.Float(string='Điểm tích lũy', readonly=True, store=True)
    scores_4custom = fields.Float(string='Điểm tích lũy tùy chỉnh', default=5.5)
    student_id = fields.Many2one('utc2.qld', string='MSV')
    subject_id = fields.Many2one('utc2.qld.subjects', string='Môn')
    subject_name = fields.Char('Tên môn', related="subject_id.name_display")
    subject_stc = fields.Integer('Số tín chỉ', related="subject_id.stc", store=True)

    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        return new_record