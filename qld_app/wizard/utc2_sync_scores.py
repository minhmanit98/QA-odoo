from odoo import _, fields, models
import time

class SyncScore(models.TransientModel):
    _name = 'utc2.sync.score'
    _description = 'Đồng bộ điểm'

    state = fields.Selection([
        ('all', 'Update all'),
        ('selected', 'Update đã chọn'),
        ('cancel', 'Hủy bỏ'),
    ], string='Status', default='all')

    def utc2_sync_score(self):
        # if self.state == 'all':
        i = 0
        print(self.env['utc2.qld'].search([('tong_stc', '=', 1)]))
        for record in self.env['utc2.qld'].search([('tong_stc', '=', 1), ('scores_4end', '!=', 11)], limit=100):
            record.sync_scores()
            i = i + 1
            print(i)
