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
            # Asegúrate de que 'account.report_invoice_with_payments' es el XML ID correcto
            report_ref = 'account.report_invoice_with_payments'
            _logger.info('WSEM: report_ref usado: %s', report_ref)
            report = self.env['ir.actions.report']._get_report_from_name(report_ref)
            _logger.info('WSEM: Referencia al reporte obtenida correctamente: %s', report)
            
            # Loguear detalles del reporte
            _logger.info('WSEM: Modelo del Reporte: %s', report._name)
            _logger.info('WSEM: Tipo de Reporte: %s', report.report_type)
            _logger.info('WSEM: Nombre del Reporte (report_name): %s', report.report_name)
            _logger.info('WSEM: Archivo del Reporte (report_file): %s', report.report_file)
            _logger.info('WSEM: Modelo Relacionado: %s', report.model)
        except ValueError as ve:
            _logger.error('WSEM: No se pudo obtener el reporte %s: %s', report_ref, ve)
            return False
        except Exception as e:
            _logger.error('WSEM: Error inesperado al obtener el reporte %s: %s', report_ref, e)
            return False

        # Verificar que el objeto report tiene el método get_pdf
        if not hasattr(report, 'get_pdf'):
            _logger.error('WSEM: El objeto referenciado no tiene el método get_pdf')
            return False

        _logger.info('WSEM: Generando PDF para el ID de factura %s', invoice_id)
        try:
            # Usa el método get_pdf en lugar de _render_qweb_pdf
            pdf_content, content_type = report.get_pdf([invoice_id], {})
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
