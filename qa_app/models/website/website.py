from odoo import fields, models, api, tools
import base64
from odoo.modules.module import get_resource_path


class Website(models.Model):

    _inherit = "website"
    _description = "Website"

    @api.model
    def _default_language(self):
        lang_code = self.env['ir.default'].get('res.partner', 'lang')
        def_lang_id = self.env['res.lang']._lang_get_id(lang_code)
        return def_lang_id or self._active_languages()[0]

    # odoo / addons / website / models / website.py
    def _default_favicon(self):
        img_path = get_resource_path('web', 'static/src/img/favicon.ico')
        with tools.file_open(img_path, 'rb') as f:
            return base64.b64encode(f.read())

    # odoo / addons / website / models / website.py
    def _default_logo(self):
        image_path = get_resource_path('qa_app', 'static/src/img', 'website_logo.png')
        with tools.file_open(image_path, 'rb') as f:
            return base64.b64encode(f.read())
