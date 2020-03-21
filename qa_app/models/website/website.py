from odoo import fields, models, api


class Website(models.Model):

    _inherit = "website"
    _description = "Website"

    @api.model
    def _default_language(self):
        lang_code = self.env['ir.default'].get('res.partner', 'lang')
        def_lang_id = self.env['res.lang']._lang_get_id(lang_code)
        return def_lang_id or self._active_languages()[0]


    


