# -*- coding: utf-8 -*-
from odoo import fields, models, api


class QLDScores(models.Model):
    _name = 'utc2.qld.scores'
    _description = 'Điểm'

    def get_diem_truoc_59(self, diem):
        if diem >= 8.5 and diem <= 10:
            return 4
        else:
            if diem >= 7 and diem <= 8.4:
                return 3
            else:
                if diem >= 5.5 and diem <= 6.9:
                    return 2
                else:
                    if diem >= 5 and diem <= 5.4:
                        return 1.5
                    else:
                        if diem >= 4 and diem <= 4.9:
                            return 1
                        else:
                            if diem >= 3 and diem <= 3.9:
                                return 0.5
                            else:
                                return 0
    def get_diem_sau_59(self, diem):
        if diem >= 9.5 and diem <= 10:
            return 4
        else:
            if diem >= 8.5 and diem <= 9.4:
                return 3.8
            else:
                if diem >= 8 and diem <= 8.4:
                    return 3.5
                else:
                    if diem >= 7 and diem <= 7.9:
                        return 3
                    else:
                        if diem >= 6 and diem <= 6.9:
                            return 2.5
                        else:
                            if diem >= 5.5 and diem <= 5.9:
                                return 2
                            else:
                                if diem >= 4.5 and diem <= 5.4:
                                    return 1.5
                                else:
                                    if diem >= 4 and diem <= 4.4:
                                        return 1
                                    else:
                                        if diem >= 2 and diem <= 3.9:
                                            return 0.5
                                        else:
                                            return 0

    def get_diem_tich_luy(self, msv, diem):
        if msv[0].lower() == 'v':
            return self.get_diem_truoc_59(diem)
        elif int(msv[0:1]) < 59:
            return self.get_diem_truoc_59(diem)
        else:
            return self.get_diem_sau_59(diem)

    @api.depends('scores_8')
    def _compute_scores_4(self):
        for record in self:
            if record.student_id:
                record.scores_4 = self.get_diem_tich_luy(record.student_id.name, record.scores_8)

    name = fields.Char(string='Tên', store=True)
    scores_8 = fields.Float(string='Điểm số', readonly=True)
    scores_word = fields.Float(string='Điểm chữ', readonly=True)
    scores_4 = fields.Float(string='Điểm tích lũy', compute=_compute_scores_4, readonly=True, store=True)
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