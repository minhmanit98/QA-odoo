# -*- coding: utf-8 -*-

from odoo import models, fields , tools
import base64
import requests


class ImageMixin(models.AbstractModel):
    _inherit = 'image.mixin'
    _description = "Image Mixin"

    def _default_avartar(self):
        response = requests.get('https://api.adorable.io/avatars/nmm').content
        return base64.b64encode(response)

    image_1920 = fields.Image("Image", max_width=1920, max_height=1920, default=_default_avartar)