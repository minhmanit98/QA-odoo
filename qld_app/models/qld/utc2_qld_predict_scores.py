# -*- coding: utf-8 -*-
from odoo import fields, models, api


class QLDPredictScores(models.Model):
    _name = 'utc2.qld.predict.scores'
    _description = 'Điểm dự đoán'

    @api.depends('scores_4')
    def _compute_scores_4custom(self):
        for record in self:
            record.scores_4custom = record.scores_8

    @api.depends('scores_4')
    def _compute_scores_predict(self):
        for record in self:
            record.scores_predict = record.scores_8

    name = fields.Char(string='Mã điểm dự đoán', readonly=True, default='New')
    scores_8 = fields.Float(string='Điểm số', readonly=True)
    scores_word = fields.Float(string='Điểm chữ', readonly=True)
    scores_4 = fields.Float(string='Điểm tích lũy', readonly=True)
    scores_4custom = fields.Float(string='Điểm số mục tiêu', compute=_compute_scores_4custom, store=True, readonly=False)
    scores_predict = fields.Float(string='Điểm dự đoán', compute=_compute_scores_predict, store=True)
    subject_id = fields.Many2one('utc2.qld.subjects', string='Môn')
    subject_name = fields.Char('Tên môn', related="subject_id.name_display")
    subject_stc = fields.Integer('Số tín chỉ', related="subject_id.stc", store=True)
    predict_id = fields.Many2one('utc2.qld.predict', string='Mã dự đoán', ondelete='cascade')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'utc2.qld.predict.scores') or 'New'
        result = super(QLDPredictScores, self).create(vals)
        return result