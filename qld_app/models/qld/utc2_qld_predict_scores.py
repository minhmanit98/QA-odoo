# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions
import statsmodels.api as sm
import numpy as np


class QLDPredictScores(models.Model):
    _name = 'utc2.qld.predict.scores'
    _description = 'Điểm dự đoán'

    def reg_m(self, y, x):
        ones = np.ones(len(x[0]))
        X = sm.add_constant(np.column_stack((x[0], ones)))
        for ele in x[1:]:
            X = sm.add_constant(np.column_stack((ele, X)))
        results = sm.OLS(y, X).fit()
        return results

    def reg2(self, y, x):
        X = sm.add_constant(x)
        model = sm.OLS(y, X)
        results = model.fit()
        return results

    def predict_score(self, predict_subject1, dx, dy):
        est = self.reg2(dy, dx)
        diem = est.params[0] + est.params[1] * predict_subject1
        if diem > 10:
            diem = 10
        return diem

    @api.depends('scores_8')
    def _compute_scores_4custom(self):
        for record in self:
            if record.scores_8:
                record.scores_4custom = record.scores_8
            else:
                record.scores_4custom = 0

    @api.depends('predict_subject_id')
    def _compute_scores_predict(self):
        for record in self:
            if record.predict_subject_id:
                if record.predict_subject_id.predict_subject1 and record.predict_subject_id.predict_subject2:
                    diem1 = self.env['utc2.qld.scores'].search([
                        ('student_id', '=', record.predict_id.student_id.id),
                        ('subject_id', '=', record.predict_subject_id.predict_subject1.id)]).scores_8
                    diem2 = self.env['utc2.qld.scores'].search([
                        ('student_id', '=', record.predict_id.student_id.id),
                        ('subject_id', '=', record.predict_subject_id.predict_subject2.id)]).scores_8
                    if diem1 == 0:
                        diem1 = self.env['utc2.qld.predict.scores'].search([
                            ('predict_id', '=', record.predict_id.id),
                            ('subject_id', '=', record.predict_subject_id.predict_subject1.id)]).scores_predict
                    if diem2 == 0:
                        diem2 = self.env['utc2.qld.predict.scores'].search([
                            ('predict_id', '=', record.predict_id.id),
                            ('subject_id', '=', record.predict_subject_id.predict_subject2.id)]).scores_predict
                    diem = diem1 * record.predict_subject_id.predict_a + diem2 * record.predict_subject_id.predict_b + record.predict_subject_id.predict_c
                    if diem > 10:
                        diem = 10-0.3
                    record.scores_predict = diem
                elif record.predict_subject_id.predict_subject1 and not record.predict_subject_id.predict_subject2:
                    diem = record.predict_subject_id.predict_c + record.predict_subject_id.predict_a * self.env['utc2.qld.scores'].search([
                        ('student_id', '=', record.predict_id.student_id.id),
                        ('subject_id', '=', record.predict_subject_id.predict_subject1.id)]).scores_8
                    if diem > 10:
                        diem = 10-0.3
                    record.scores_predict = diem
            else:
                record.scores_predict = record.scores_8

    name = fields.Char(string='Mã điểm dự đoán', readonly=True, default='New')
    scores_8 = fields.Float(string='Điểm số', readonly=True)
    scores_word = fields.Float(string='Điểm chữ', readonly=True)
    scores_4 = fields.Float(string='Điểm tích lũy', readonly=True)
    scores_4custom = fields.Float(string='Điểm số mục tiêu', compute=_compute_scores_4custom, store=True,
                                  readonly=False)
    scores_predict = fields.Float(string='Điểm dự đoán', compute=_compute_scores_predict, store=True)
    subject_id = fields.Many2one('utc2.qld.subjects', string='Môn')
    subject_name = fields.Char('Tên môn', related="subject_id.name_display")
    subject_stc = fields.Integer('Số tín chỉ', related="subject_id.stc", store=True)
    predict_id = fields.Many2one('utc2.qld.predict', string='Mã dự đoán', ondelete='cascade')
    predict_subject_id = fields.Many2one('utc2.qld.predict.subjects', string='Công thức dự đoán')

    # @api.onchange('predict_subject_id')
    # def onchange_predict_subject_id(self):
    #     print(self)
    #     if self.predict_subject_id.predict_subject1:
    #         if not self.env['utc2.qld.scores'].search([('student_id', '=', self.predict_id.student_id.id),
    #                                                    ('subject_id', '=',
    #                                                     self.predict_subject_id.predict_subject1.id)]):
    #             if self.env['utc2.qld.predict.scores'].search_count([
    #                 ('predict_id', '=', self.predict_id.id),
    #                  ('subject_id', '=', self.predict_subject_id.predict_subject1.id)]) == 0:
    #                 raise exceptions.UserError(
    #                     'Môn ' + str(self.predict_subject_id.predict_subject1.name_display)
    #                     + ' không có trong chương trình học của sinh viên này')
    #
    #     if self.predict_subject_id.predict_subject2:
    #         if not self.env['utc2.qld.scores'].search([('student_id', '=', self.predict_id.student_id.id),
    #                                                    ('subject_id', '=',
    #                                                     self.predict_subject_id.predict_subject2.id)]):
    #             if self.env['utc2.qld.predict.scores'].search_count([
    #                 ('predict_id', '=', self.predict_id.id),
    #                  ('subject_id', '=', self.predict_subject_id.predict_subject2.id)]) == 0:
    #                 raise exceptions.UserError(
    #                     'Môn ' + str(self.predict_subject_id.predict_subject2.name_display)
    #                     + ' không có trong chương trình học của sinh viên này')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'utc2.qld.predict.scores') or 'New'
        result = super(QLDPredictScores, self).create(vals)
        return result

    def write(self, vals):
        if vals.get('predict_subject_id'):
            predict_subject_id = self.env['utc2.qld.predict.subjects'].search([
                ('id', '=', vals.get('predict_subject_id'))])
            if predict_subject_id.predict_subject1:
                if not self.env['utc2.qld.scores'].search([('student_id', '=', self.predict_id.student_id.id),
                                                           ('subject_id', '=',
                                                            predict_subject_id.predict_subject1.id)]):
                    if self.env['utc2.qld.predict.scores'].search_count([
                        ('predict_id', '=', self.predict_id.id),
                         ('subject_id', '=', predict_subject_id.predict_subject1.id)]) == 0:
                        raise exceptions.UserError(
                            'Môn ' + str(self.predict_subject_id.predict_subject1.name_display)
                            + ' không có trong chương trình học của sinh viên này')
            elif predict_subject_id.predict_subject2:
                if not self.env['utc2.qld.scores'].search([('student_id', '=', self.predict_id.student_id.id),
                                                           ('subject_id', '=',
                                                            predict_subject_id.predict_subject2.id)]):
                    if self.env['utc2.qld.predict.scores'].search_count([
                        ('predict_id', '=', self.predict_id.id),
                         ('subject_id', '=', predict_subject_id.predict_subject2.id)]) == 0:
                        raise exceptions.UserError(
                            'Môn ' + str(self.predict_subject_id.predict_subject2.name_display)
                            + ' không có trong chương trình học của sinh viên này')
            else:
                self._compute_scores_predict()
        result = super(QLDPredictScores, self).write(vals)
        return result

