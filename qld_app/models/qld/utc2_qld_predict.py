# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class QLDPredict(models.Model):
    _name = 'utc2.qld.predict'
    _description = 'Dự đoán'

    def tinh_tong_stc(self):
        tongstc = 0
        for score in self.predict_scores_ids:
            if score.subject_id.is_dtl:
                tongstc = tongstc + score.subject_id.stc
        return tongstc

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

    @api.depends("predict_scores_ids")
    def _compute_tong_stc(self):
        for record in self:
            record.tong_stc = record.tinh_tong_stc()

    @api.depends("predict_scores_ids")
    def _compute_stc_current(self):
        for record in self:
            stc = 0
            for score in record.predict_scores_ids:
                if score.subject_id.is_dtl and score.scores_4 > 0:
                    stc = stc + score.subject_id.stc
            record.stc_current = stc

    @api.depends("predict_scores_ids")
    def _compute_scores_4end(self):
        for record in self:
            tong_diem = 0
            if record.stc_current >= 1:
                for score in record.predict_scores_ids:
                    if score.subject_id.is_dtl:
                        tong_diem = tong_diem + (score.scores_4 * score.subject_stc)
                record.scores_4end = tong_diem / self.stc_current

    @api.depends("predict_scores_ids")
    def _compute_scores_4cus(self):
        for record in self:
            tong_diem = 0
            if record.tong_stc >= 1:
                for score in record.predict_scores_ids:
                    if score.subject_id.is_dtl:
                        diem = self.get_diem_tich_luy(record.student_id.name, score.scores_4custom)
                        tong_diem = tong_diem + (diem * score.subject_stc)
                record.scores_4cus = tong_diem / self.tong_stc

    @api.depends("predict_scores_ids")
    def _compute_scores_predict(self):
        for record in self:
            tong_diem = 0
            if record.tong_stc >= 1:
                for score in record.predict_scores_ids:
                    if score.subject_id.is_dtl:
                        diem = self.get_diem_tich_luy(record.student_id.name, score.scores_predict)
                        tong_diem = tong_diem + (diem * score.subject_stc)
                record.scores_predict = tong_diem / self.tong_stc

    name = fields.Char('Mã dự đoán', readonly=True, default='New')
    student_id = fields.Many2one('utc2.qld.students', string='Mã sinh viên', required=True)
    predict_scores_ids = fields.One2many('utc2.qld.predict.scores', 'predict_id', string='Bảng điểm dự đoán')
    scores_4end = fields.Float(string='Điểm tích lũy', compute=_compute_scores_4end, store=True)
    scores_predict = fields.Float(string='Điểm tích dự đoán', compute=_compute_scores_predict, store=True)
    scores_4cus = fields.Float(string='Điểm tích mục tiêu', compute=_compute_scores_4cus, store=True)
    tong_stc = fields.Integer(string='Tổng số tín chỉ', compute=_compute_tong_stc, default=1, store=True)
    stc_current = fields.Integer(string='Số tín chỉ hiện tại', compute=_compute_stc_current, default=1, store=True)

    @api.onchange('predict_scores_ids', 'student_id')
    def onchange_predict_scores_ids(self):
        if self.student_id and self.predict_scores_ids:
            self.tong_stc = self.student_id.tong_stc
            self.scores_4end = self.student_id.scores_4end

    @api.model
    def create(self, vals):
        predict = []
        subject_current = []
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'utc2.qld.predict') or 'New'
        scores_ids = self.env['utc2.qld.scores'].search([('student_id', '=', vals.get('student_id'))])
        for record in scores_ids:
            predict_scores = self.env['utc2.qld.predict.scores'].create({
                'scores_8': record.scores_8,
                'scores_word': record.scores_word,
                'scores_4': record.scores_4,
                'subject_id': record.subject_id.id,
            })
            subject_current.append(record.subject_id.id)
            predict.append(predict_scores.id)
        class_id = self.env['utc2.qld.students'].search([('id', '=', vals.get('student_id'))]).class_id
        if class_id.subject_ids:
            for subject in class_id.subject_ids:
                if not subject.id in subject_current:
                    predict_scores = self.env['utc2.qld.predict.scores'].create({
                        'subject_id': subject.id,
                    })
                    subject_current.append(subject.id)
                    predict.append(predict_scores.id)
            vals['predict_scores_ids'] = [(6, 0, predict)]
        result = super(QLDPredict, self).create(vals)
        return result

    def action_get_scores(self):
        self.student_id.action_sync_scores()
        subject_current = []
        if not self.predict_scores_ids:
            scores_ids = self.env['utc2.qld.scores'].search([('student_id', '=', self.student_id.id)])
            for record in scores_ids:
                predict_scores = self.env['utc2.qld.predict.scores'].create({
                    'scores_8': record.scores_8,
                    'scores_word': record.scores_word,
                    'scores_4': record.scores_4,
                    'subject_id': record.subject_id.id,
                    'predict_id': self.id,
                })
                subject_current.append(record.subject_id.id)

            class_id = self.student_id.class_id
            if class_id.subject_ids:
                for subject in class_id.subject_ids:
                    if not subject.id in subject_current:
                        predict_scores = self.env['utc2.qld.predict.scores'].create({
                            'subject_id': subject.id,
                            'predict_id': self.id,
                        })
                        subject_current.append(subject.id)
        else:
            scores_ids = self.env['utc2.qld.scores'].search([('student_id', '=', self.student_id.id)])
            scores_id = []
            for record in scores_ids:
                for predict in self.predict_scores_ids:
                    if predict.subject_id.id == record.subject_id.id:
                        predict.scores_8 = record.scores_8
                        predict.scores_word = record.scores_word
                        predict.scores_4 = record.scores_4
                        subject_current.append(predict.subject_id.id)
                    elif not record in scores_id and not record.subject_id in self.predict_scores_ids.subject_id:
                        scores_id.append(record)
            for record in scores_id:
                predict_scores = self.env['utc2.qld.predict.scores'].create({
                    'scores_8': record.scores_8,
                    'scores_word': record.scores_word,
                    'scores_4': record.scores_4,
                    'subject_id': record.subject_id.id,
                    'predict_id': self.id,
                })
                subject_current.append(record.subject_id.id)
            class_id = self.student_id.class_id
            if class_id.subject_ids:
                for subject in class_id.subject_ids:
                    if not subject in self.predict_scores_ids.subject_id:
                        predict_scores = self.env['utc2.qld.predict.scores'].create({
                            'subject_id': subject.id,
                            'predict_id': self.id,
                        })
                        subject_current.append(subject.id)
