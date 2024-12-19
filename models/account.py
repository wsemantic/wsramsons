import logging
from odoo import models, api
import base64

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def get_invoice_pdf(self, invoice_id):
        _logger.info('WSEM: Iniciando get_invoice_pdf con invoice_id=%s', invoice_id)
        
        # Buscar la factura (opcional, solo para log adicional)
        move = self.browse(invoice_id)
        if not move or not move.exists():
            _logger.warning('WSEM: No se encontró la factura con ID=%s', invoice_id)
        
        _logger.info('WSEM: Obteniendo referencia al reporte')
        report = self.env.ref('account.report_invoice_with_payments')
        
        if not report:
            _logger.error('WSEM: No se pudo obtener el reporte account.report_invoice_with_payments')
            return False
        
        _logger.info('WSEM: Generando PDF para el ID de factura %s', invoice_id)
        pdf_content, content_type = report._render_qweb_pdf([invoice_id])
        
        if not pdf_content:
            _logger.error('WSEM: El contenido del PDF está vacío para invoice_id=%s', invoice_id)
            return False
        
        _logger.info('WSEM: PDF generado exitosamente. Longitud del contenido: %d bytes', len(pdf_content))
        
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
        _logger.info('WSEM: PDF convertido a base64 exitosamente. Longitud base64: %d caracteres', len(pdf_base64))
        
        _logger.info('WSEM: Finalizando get_invoice_pdf para invoice_id=%s', invoice_id)
        return pdf_base64
