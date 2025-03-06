from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'    

    pcontacto = fields.Char(string='Persona Contacto')