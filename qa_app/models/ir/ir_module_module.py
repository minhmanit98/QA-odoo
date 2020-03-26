# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class IrModule(models.Model):

    _inherit = "ir.module.module"

    @api.model
    def _utc2_install_theme(self):
        website = self.env['website'].get_current_website()
        website.theme_id._theme_upgrade_upstream()

    def button_refresh_theme(self):
        """
            Refresh the current theme of the current website.

            To refresh it, we only need to upgrade the modules.
            Indeed the (re)loading of the theme will be done automatically on ``write``.
        """
        website = self.env['website'].get_current_website()
        website.theme_id._theme_upgrade_upstream()
