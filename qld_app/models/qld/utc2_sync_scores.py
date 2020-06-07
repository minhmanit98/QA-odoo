from odoo import _, fields, models

class SyncScore(models.Model):
    _name = 'utc2.sync.scores'
    _description = 'Đồng bộ điểm'

    state = fields.Selection([
        ('all', 'Update all'),
        ('selected', 'Update đã chọn'),
        ('cancel', 'Hủy bỏ'),
    ], string='Status', default='all')

    limit_update = fields.Integer(string='Giới hạn update', default=100)

    def utc2_sync_score(self):
        # if self.state == 'all':
        i = 0
        print(self.env['utc2.qld'].search([('tong_stc', '=', 1)]))
        for record in self.env['utc2.qld'].search([('tong_stc', '=', 1), ('scores_4end', '!=', 11)], limit=self.limit_update):
            record.action_sync_scores()
            i = i + 1
            print(i)
