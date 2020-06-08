# -*- coding: utf-8 -*-
from odoo import fields, models, api
import urllib.request
from html_table_parser import HTMLTableParser


class QLD(models.Model):
    _name = 'utc2.qld.students'
    _description = 'Danh sách sinh viên'
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    def check_mon(self, mon):
        list_mon = ['GQP201.3', 'GQP202.2', 'GQP203.3', 'GDT01.1', 'GDT02.1',
                    'GDT03.1', 'GDT03.12', 'GDT04.1', 'GDT05.1', 'ANH01.3', 'ANHA1.4', 'ANHA2.4']
        if mon in list_mon:
           return False
        else:
            return True

    def get_tin_chi(self, string):
        if len(string) > 2:
            if string[1] == '0':
                return 10
            else:
                return int(string[0])
        elif len(string) == 1:
            return int(string[0])

    def tinh_tong_stc(self):
        tongstc = 0
        for score in self.scores_ids:
            if score.subject_id.is_dtl:
                tongstc = tongstc + score.subject_id.stc
        return tongstc

    def _compute_tong_stc(self):
        for record in self:
            record.tong_stc = record.tinh_tong_stc()

    def diem_tich_luy(self):
        tong_diem = 0
        if self.tong_stc >= 1:
            for score in self.scores_ids:
                if score.subject_id.is_dtl:
                    tong_diem = tong_diem + (score.scores_4 * score.subject_id.stc)
            diem_tl = tong_diem / self.tong_stc
        else:
            self.state = 'missed'
            diem_tl = 0
        return diem_tl

    def _compute_scores_4end(self):
        for record in self:
            record.scores_4end = record.diem_tich_luy()

    def update_sv(self):
        self.tong_stc = self.tinh_tong_stc()
        self.scores_4end = self.diem_tich_luy()

    name = fields.Char('MSV', required=True)
    user_id = fields.Many2one('res.users', string='Student', ondelete='restrict')
    scores_4end = fields.Float(string='Điểm tích lũy', compute=_compute_scores_4end, store=True)
    scores_4end_cus = fields.Float(string='Điểm tích lũy tùy chỉnh', default=5.5)
    scores_ids = fields.One2many('utc2.qld.scores', 'student_id', string='Điểm các môn')
    tong_stc = fields.Integer(string='Tổng số tín chỉ', compute=_compute_tong_stc, default=1, store=True)
    class_id = fields.Many2one('utc2.qld.class', string='Lớp', ondelete='restrict')
    state = fields.Selection([
        ('studying', 'Đang học'),
        ('missed', 'Nghỉ học'),
        ('graduated', 'Đã tốt nghiệp'),
    ], string='Status', default='studying')


    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        return new_record

    def url_get_contents(self, url):
        """ Opens a website and read its binary contents (HTTP Response Body) """
        req = urllib.request.Request(url=url)
        f = urllib.request.urlopen(req)
        return f.read()

    def request_diem(self, msv):
        request = 'http://xemdiem.utc2.edu.vn/svxemdiem.aspx?ID=' + msv + '&m_lopID=C%C3%B4ng%20ngh%E1%BB%87%20th%C3%B4ng%20tin%20%20K57&m_lopID_ID=4363&istinchi=1'
        xhtml = self.url_get_contents(request).decode('utf-8')
        p = HTMLTableParser()
        p.feed(xhtml)
        csvData = p.tables
        return csvData

    def xuly(self, diem):
        diem_clean = []
        for mon in range(1, len(diem)):
            if len(diem[mon]) == 5:
                diem_clean.append(diem[mon])
        return diem_clean

    def getdiem(self, string, string2):
        diem1 = '0'
        diem2 = '0'
        if string[len(string) - 1].find("0") > -1:
            if string[len(string) - 3].find(".") > -1:
                diem1 = string[len(string) - 4:len(string)]
            else:
                if string[len(string) - 2].find('1') > -1:
                    diem1 = string[len(string) - 2:len(string)]
                else:
                    diem1 = 0
        else:
            diem1 = string[len(string) - 1]

        if len(string2) > 0:
            diem2 = string2
            if float(diem1) > float(diem2):
                return diem1
            else:
                return diem2
        else:
            return diem1

    def get_diem_tich_luy(self, msv, diem):
        if int(msv[0:1]) < 59:
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
        else:
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

    def action_sync_scores(self):
        msv = self.name
        data_diem = self.request_diem(msv)
        diem_all = self.xuly(data_diem[3])
        data_info = data_diem[2]

        if len(data_info) > 1:
            class_name = data_info[3][0][4:len(data_info[3][0])]
            if self.env['utc2.qld.class'].search_count([('name', '=', class_name)]) > 0:
                self.class_id = self.env['utc2.qld.class'].search([('name', '=', class_name)]).id
            else:
                class_id = self.env['utc2.qld.class'].create({
                    'name': class_name,
                })
                self.class_id = class_id
        else:
            self.state = 'missed'
            return

        for mon in diem_all:
            if self.env['utc2.qld.subjects'].search_count([('name', '=', str(mon[1]))]) > 0:
                if self.env['utc2.qld.scores'].search_count([('name', '=', str(msv) + '/' + str(mon[1]) + '/' + str(self.getdiem(mon[3], mon[4])))]) > 0:
                    self.update_sv()
                else:
                    scores = self.env['utc2.qld.scores'].create({
                        'name': str(msv) + '/' + str(mon[1]) + '/' + str(self.getdiem(mon[3], mon[4])),
                        'scores_8': float(self.getdiem(mon[3], mon[4])),
                        'scores_4': float(self.get_diem_tich_luy(msv, float(self.getdiem(mon[3], mon[4])))),
                        'student_id': self.id,
                        'subject_id': self.env['utc2.qld.subjects'].search([('name', '=', mon[1])]).id
                    })
            else:
                subjects = self.env['utc2.qld.subjects'].create({
                    'name': str(mon[1]),
                    'name_display': str(mon[2]),
                    'stc': self.get_tin_chi(mon[3]),
                    'is_dtl': self.check_mon(mon[1])
                })
                scores = self.env['utc2.qld.scores'].create({
                    'name': str(msv) + '/' + str(mon[1]) + '/' + str(self.getdiem(mon[3], mon[4])),
                    'scores_8': float(self.getdiem(mon[3], mon[4])),
                    'scores_4': float(self.get_diem_tich_luy(msv, float(self.getdiem(mon[3], mon[4])))),
                    'student_id': self.id,
                    'subject_id': subjects.id
                })
        self.update_sv()
        return 'Thanh cong chua'
