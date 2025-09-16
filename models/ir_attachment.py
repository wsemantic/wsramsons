# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import AccessError


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def unlink(self):
        if self.env.user.has_group("wsramsons.group_comercial"):
            raise AccessError("No tienes permisos para eliminar adjuntos.")
        return super().unlink()
