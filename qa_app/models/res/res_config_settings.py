# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.base.models.res_partner import _lang_get


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auth_signup_uninvited = fields.Selection([
        ('b2b', 'On invitation'),
        ('b2c', 'Free sign up'),
    ], string='Customer Account', default='b2c', config_parameter='auth_signup.invitation_scope')

    def _default_lang(self):
        return self.utc2_default_lang

    def _default_tz(self):
        return self.utc2_default_tz

    utc2_default_lang = fields.Selection(_lang_get, string='Language', default=_default_lang)
    utc2_default_tz = fields.Selection(_tz_get, string='Timezone', default=_default_tz)

    def action_utc2_default(self):
        res = super(ResConfigSettings, self).get_values()
        partners1 = self.env['res.partner'].search([('lang', '!=', res.utc2_default_lang)])
        for partner in partners1:
            partner.lang = res.utc2_default_lang

        partners2 = self.env['res.partner'].search([('tz', '!=', res.utc2_default_tz)])
        for partner in partners2:
            partner.tz = res.utc2_default_tz
