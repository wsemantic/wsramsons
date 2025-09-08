from odoo import models, fields, api
from odoo.exceptions import AccessError

class ResPartner(models.Model):
    _inherit = 'res.partner'    

    pcontacto = fields.Char(string='Persona Contacto')
    

    def write(self, vals):
        """Bloquear edición para grupo comercial"""
        if self.env.user.has_group('wsramsons.group_comercial'):
            raise AccessError("No tienes permisos para editar contactos")
        return super().write(vals)

    @api.model_create_multi  
    def create(self, vals_list):
        """Bloquear creación para grupo comercial"""
        if self.env.user.has_group('wsramsons.group_comercial'):
            raise AccessError("No tienes permisos para crear contactos")
        return super().create(vals_list)

    def unlink(self):
        """Bloquear eliminación para grupo comercial"""
        if self.env.user.has_group('wsramsons.group_comercial'):
            raise AccessError("No tienes permisos para eliminar contactos")
        return super().unlink()