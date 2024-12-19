# my_module/models/account_move.py
import logging
from odoo import models, api
import base64

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def get_invoice_pdf(self, invoice_id):
        _logger.info('WSEM: Iniciando get_invoice_pdf con invoice_id=%s', invoice_id)
        
        # Buscar la factura
        move = self.browse(invoice_id)
        if not move.exists():
            _logger.warning('WSEM: No se encontró la factura con ID=%s', invoice_id)
            return False

        _logger.info('WSEM: Obteniendo referencia al reporte')
        try:
            # Usa el método adecuado para obtener el reporte desde ir.actions.report
            report = self.env['ir.actions.report']._get_report_from_name('account.report_invoice_with_payments')
            _logger.info('WSEM: Referencia al reporte obtenida correctamente: %s', report)
            
            # Loguear el tipo de objeto
            _logger.info('WSEM: Tipo del objeto report: %s', report._name)
            _logger.info('WSEM: Clase del objeto report: %s', report.__class__)
        except ValueError:
            _logger.error('WSEM: No se pudo obtener el reporte account.report_invoice_with_payments')
            return False

        # Verificar que el objeto report tiene el método _render_qweb_pdf
        if not hasattr(report, '_render_qweb_pdf'):
            _logger.error('WSEM: El objeto referenciado no tiene el método _render_qweb_pdf')
            return False

        _logger.info('WSEM: Generando PDF para el ID de factura %s', invoice_id)
        try:
            pdf_content, content_type = report._render_qweb_pdf([invoice_id])
            _logger.info('WSEM: PDF generado exitosamente. Longitud del contenido: %d bytes', len(pdf_content))
        except Exception as e:
            _logger.error('WSEM: Error al generar el PDF: %s', e)
            return False

        if not pdf_content:
            _logger.error('WSEM: El contenido del PDF está vacío para invoice_id=%s', invoice_id)
            return False

        try:
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            _logger.info('WSEM: PDF convertido a base64 exitosamente. Longitud base64: %d caracteres', len(pdf_base64))
        except Exception as e:
            _logger.error('WSEM: Error al convertir el PDF a base64: %s', e)
            return False

        _logger.info('WSEM: Finalizando get_invoice_pdf para invoice_id=%s', invoice_id)
        return pdf_base64
