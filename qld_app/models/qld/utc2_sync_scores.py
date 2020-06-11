from odoo import _, fields, models, api

class SyncScore(models.Model):
    _name = 'utc2.sync.scores'
    _description = 'Đồng bộ điểm'

    state = fields.Selection([
        ('all', 'Update all'),
        ('selected', 'Update đã chọn'),
        ('cancel', 'Hủy bỏ'),
    ], string='Status', default='all')

    limit_update = fields.Integer(string='Giới hạn update', default=100)

    # @api.model
    # def default_get(self, field_names):
    #     defaults = super().default_get(field_names)
    #     student_ids = self.env.context.get('active_id')
    #     defaults['student_ids'] = student_ids
    #     return defaults

    def utc2_sync_score(self):
        if self.state == "selected":
            i = 0
            student_ids = self.env.context.get("active_ids")
            for student in student_ids:
                record = self.env['utc2.qld.students'].browse(int(student))
                record.action_sync_scores()
                i = i + 1
                print(record.name + '/' + str(i))
        elif self.state == 'all':
            i = 0
            print(self.env['utc2.qld.students'].search([('tong_stc', '=', 1)]))
            for record in self.env['utc2.qld.students'].search([('tong_stc', '=', 1), ('state', '!=', 'missed')], limit=self.limit_update):
                record.action_sync_scores()
                i = i + 1
                print(record.name + '/' + str(i))

    def utc2_group_subject(self):
        if self.state == "selected":
            i = 0
            subject_ids = self.env.context.get("active_ids")
            for subject in subject_ids:
                record = self.env['utc2.qld.subjects'].browse(int(subject))
                record.action_group_subject()
                i = i + 1
                print(record.name + '/' + str(i))
        elif self.state == 'all':
            i = 0
            for record in self.env['utc2.qld.subjects'].search([('group_id', '=', False)], limit=self.limit_update):
                record.action_group_subject()
                i = i + 1
                print(record.name + '/' + str(i))