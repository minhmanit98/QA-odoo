# -*- coding: utf-8 -*-
from odoo import fields, models, api , exceptions


class QLDPredict(models.Model):
    _name = 'utc2.qld.predict'
    _description = 'Dự đoán'

    name = fields.Char('Mã dự đoán', required=True)
    student_id = fields.Many2one('utc2.qld.students', string='Mã sinh viên')
    predict_scores_id = fields.One2Many('utc2.qld.predict.scores', 'predict_id', string='Bảng điểm dự đoán')
