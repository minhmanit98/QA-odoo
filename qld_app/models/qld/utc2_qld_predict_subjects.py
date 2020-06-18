# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions
import pandas as pd
import statsmodels.api as sm
import numpy as np

class QLDPredictSubjects(models.Model):
    _name = 'utc2.qld.predict.subjects'
    _description = 'Môn tiên đoán'

    def reg_predict_2(self, y, x):
        ones = np.ones(len(x[0]))
        X = sm.add_constant(np.column_stack((x[0], ones)))
        for ele in x[1:]:
            X = sm.add_constant(np.column_stack((ele, X)))
        results = sm.OLS(y, X).fit()
        return results

    def reg_predict_1(self, y, x):
        X = sm.add_constant(x)
        model = sm.OLS(y, X)
        results = model.fit()
        return results

    def get_predict_score(self, x1, x2):
        if self.predict_subject1 and not self.predict_subject2:
            return x1*self.predict_a + self.predict_c
        elif self.predict_subject1 and self.predict_subject2:
            return x1 * self.predict_a + x2 * self.predict_b + self.predict_c

    def _compute_predict(self):
        for record in self:
            if record.predict_subject1 and not record.predict_subject2:
                x = []
                y = []
                list_score_x = self.env['utc2.qld.scores'].search([
                    ('scores_8', '>=', 5.5), ('subject_id', '=', record.predict_subject1.id)])
                list_score_y = self.env['utc2.qld.scores'].search([
                    ('scores_8', '>=', 5.5), ('subject_id', '=', record.subject_id.id)])
                for score_y in list_score_y:
                    for score_x in list_score_x:
                        if score_x.student_id == score_y.student_id:
                            x.append(score_x.scores_8)
                            y.append(score_y.scores_8)
                est = self.reg_predict_1(y, x)
                record.predict_a = est.params[1]
                record.predict_c = est.params[0]
            elif record.predict_subject1 and record.predict_subject2:
                x = []
                x1 = []
                x2 = []
                y = []
                list_score_y = self.env['utc2.qld.scores'].search([
                    ('scores_8', '>=', 5.5), ('subject_id', '=', record.subject_id.id)])
                list_score_x1 = self.env['utc2.qld.scores'].search([
                    ('scores_8', '>=', 5.5), ('subject_id', '=', record.predict_subject1.id)])
                list_score_x2 = self.env['utc2.qld.scores'].search([
                    ('scores_8', '>=', 5.5), ('subject_id', '=', record.predict_subject2.id)])
                for score_y in list_score_y:
                    for score_x1 in list_score_x1:
                        for score_x2 in list_score_x2:
                            if score_x1.student_id == score_y.student_id and score_x1.student_id == score_x2.student_id:
                                x1.append(score_x1.scores_8)
                                x2.append(score_x2.scores_8)
                                y.append(score_y.scores_8)
                x.append(x1)
                x.append(x2)
                est = self.reg_predict_2(y, x)
                record.predict_a = est.params[0]
                record.predict_b = est.params[1]
                record.predict_c = est.params[2]

    name = fields.Char('Mã môn', default='New', readonly=True)
    subject_id = fields.Many2one('utc2.qld.subjects', string='Môn dự đoán')
    student_id = fields.Many2one('utc2.qld.students', string='Mã sinh viên')
    state = fields.Selection([('current', 'Học như hiện tại'), ('try_hard', 'Cố gắng hơn')], 'Chế độ')
    predict_subject1 = fields.Many2one('utc2.qld.subjects', string='Môn liên quan 1', ondelete='restrict')
    predict_subject2 = fields.Many2one('utc2.qld.subjects', string='Môn liên quan 2', ondelete='restrict')
    class_id = fields.Many2one('utc2.qld.class', string='Lớp')
    predict_a = fields.Float('Predict A', compute=_compute_predict, store=True)
    predict_b = fields.Float('Predict B', compute=_compute_predict, store=True)
    predict_c = fields.Float('Predict C', compute=_compute_predict, store=True)
