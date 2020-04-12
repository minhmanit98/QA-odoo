# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.base.models.res_partner import _lang_get
import subprocess
import logging

from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _default_lang(self):
        return self.utc2_default_lang

    def _default_tz(self):
        return self.utc2_default_tz

    utc2_default_lang = fields.Selection(_lang_get, string='Language', default=_default_lang)
    utc2_default_tz = fields.Selection(_tz_get, string='Timezone', default=_default_tz)

    cal_client_id = fields.Char("Client_id", config_parameter='google_calendar_client_id', default='112710195791-8skohicsf0fmnie0ialj1qp2nvqglip9.apps.googleusercontent.com')
    cal_client_secret = fields.Char("Client_key", config_parameter='google_calendar_client_secret', default='gEfMz15X_7wSETwgQJOY7gWJ')
    server_uri = fields.Char('URI for tuto')

    def action_utc2_default(self):
        res = super(ResConfigSettings, self).get_values()
        partners1 = self.env['res.partner'].search([('lang', '!=', res.utc2_default_lang)])
        for partner in partners1:
            partner.lang = res.utc2_default_lang

        partners2 = self.env['res.partner'].search([('tz', '!=', res.utc2_default_tz)])
        for partner in partners2:
            partner.tz = res.utc2_default_tz

    def action_utc2_update(self):
        ls = subprocess.check_output("ls", shell=True)
        print(ls)
        # output = subprocess.check_output("./script.sh", shell=True)
        raise UserError(_(ls))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            server_uri="%s/google_account/authentication" % get_param('web.base.url',
                                                                      default="http://localhost:8070"),
        )
        return res
