from odoo import api, models
from odoo.exceptions import AccessError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _is_commercial_user(self):
        return self.env.user.has_group('wsramsons.group_comercial')

    @staticmethod
    def _is_allowed_chatter_update(vals):
        if not vals:
            return True

        allowed_prefixes = ('message_', 'activity_')
        allowed_fields = {'message_follower_ids', 'message_ids', 'activity_ids'}

        for field_name in vals.keys():
            if field_name in allowed_fields:
                continue
            if field_name.startswith(allowed_prefixes):
                continue
            return False
        return True

    def _check_commercial_block(self, message):
        if self._is_commercial_user():
            raise AccessError(message)

    ''' 
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.note:
            invoice_vals['narration'] = self.note
        return invoice_val
    '''
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        # Evitamos que se copie el contenido del campo 'note' al campo 'narration'
        if 'narration' in invoice_vals:
            invoice_vals['narration'] = ''  # O puedes asignarle otro valor si lo deseas
        return invoice_vals

    def write(self, vals):
        if self._is_commercial_user() and not self._is_allowed_chatter_update(vals):
            self._check_commercial_block("No tienes permisos para modificar presupuestos.")
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.user.has_group('wsramsons.group_comercial'):
            raise AccessError("No tienes permisos para crear presupuestos.")
        return super().create(vals_list)

    def unlink(self):
        if self._is_commercial_user():
            self._check_commercial_block("No tienes permisos para eliminar presupuestos.")
        return super().unlink()

    def action_set_to_draft(self):
        self._check_commercial_block("No tienes permisos para reabrir presupuestos.")
        return super().action_set_to_draft()
        
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        for line in self:
            # Verificar si el pedido está confirmado, el producto no ha cambiado y el cliente no ha cambiado
            if (line.order_id.state in ['sale', 'done'] and
                line.product_id == line._origin.product_id and
                line.order_id.partner_id == line._origin.order_id.partner_id):
                continue

            # Si no se cumplen todas las condiciones anteriores, usar el comportamiento estándar
            super(SaleOrderLine, line)._compute_price_unit()
            
