"""
Contract Generator - Backend System
Sistema de generación automática de contratos legales colombianos
"""

import os
import re
from datetime import datetime
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from num2words import num2words


class ContractData:
    """Clase para almacenar y validar datos del contrato"""
    
    def __init__(self, data: Dict[str, Any]):
        # Datos del contratante
        self.contratante_razon_social = data.get('contratante_razon_social', '')
        self.contratante_nit = data.get('contratante_nit', '')
        self.contratante_representante = data.get('contratante_representante', '')
        self.contratante_cc_representante = data.get('contratante_cc_representante', '')
        self.contratante_domicilio = data.get('contratante_domicilio', '')
        self.contratante_direccion = data.get('contratante_direccion', '')
        
        # Datos del contratista
        self.contratista_nombre = data.get('contratista_nombre', '')
        self.contratista_cc = data.get('contratista_cc', '')
        self.contratista_domicilio = data.get('contratista_domicilio', '')
        self.contratista_direccion = data.get('contratista_direccion', '')
        
        # Objeto del contrato
        self.objeto_servicios = data.get('objeto_servicios', '')
        
        # Valores monetarios
        self.valor_total = data.get('valor_total', 0)
        self.valor_total_letras = data.get('valor_total_letras', '')
        
        # Desglose de pagos
        self.pagos = data.get('pagos', [])
        
        # Datos bancarios
        self.banco = data.get('banco', '')
        self.tipo_cuenta = data.get('tipo_cuenta', '')
        self.numero_cuenta = data.get('numero_cuenta', '')
        self.titular_cuenta = data.get('titular_cuenta', '')
        self.cc_titular = data.get('cc_titular', '')
        
        # Fechas
        self.fecha_firma = data.get('fecha_firma', datetime.now().strftime('%d de %B de %Y'))
        self.lugar_firma = data.get('lugar_firma', '')
        
        # Otros parámetros
        self.retencion_minima = data.get('retencion_minima', '1.344.573')
        self.penalidad_porcentaje = data.get('penalidad_porcentaje', '20')
        self.dias_gracia = data.get('dias_gracia', '5')
        
    def validate(self) -> bool:
        """Valida que los datos obligatorios estén presentes"""
        required_fields = [
            'contratante_razon_social', 'contratante_nit',
            'contratista_nombre', 'contratista_cc',
            'objeto_servicios', 'valor_total'
        ]
        
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"Campo obligatorio faltante: {field}")
        
        return True


class NumberToSpanish:
    """Convierte números a texto en español (formato colombiano)"""
    
    @staticmethod
    def convert(number: float) -> str:
        """
        Convierte un número a su representación en letras en español
        Formato: SIETE MILLONES CUARENTA MIL SEISCIENTOS SESENTA Y SIETE PESOS M/Cte
        """
        try:
            # Separar la parte entera de los decimales
            integer_part = int(number)
            
            # Convertir a palabras en español
            words = num2words(integer_part, lang='es').upper()
            
            # Agregar "PESOS M/CTE" al final
            result = f"{words} PESOS M/Cte"
            
            return result
        except Exception as e:
            raise ValueError(f"Error al convertir número a letras: {e}")
    
    @staticmethod
    def format_currency(number: float) -> str:
        """
        Formatea un número como moneda colombiana
        Ejemplo: 7040667 -> $ 7'040.667
        """
        # Convertir a string y separar por miles con apóstrofo
        num_str = f"{int(number):,}".replace(',', "'")
        return f"$ {num_str}"


class ContractTemplate:
    """Clase para manejar la plantilla del contrato"""
    
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.template_content = self._load_template()
    
    def _load_template(self) -> str:
        """Carga el contenido de la plantilla"""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def replace_placeholders(self, data: ContractData) -> str:
        """Reemplaza todos los marcadores de posición con los datos reales"""
        content = self.template_content
        
        # Reemplazar datos del contratante
        replacements = {
            'Dulces El Trapiche S.A.S': data.contratante_razon_social,
            '890932227- 3': data.contratante_nit,
            '890932227-3': data.contratante_nit,
            'Edison Ramírez Serna Quintero': data.contratante_representante,
            'Cra 51 # 95A Sur -13': data.contratante_direccion,
            
            # Datos del contratista
            'GERMÁN GARCÍA PÉREZ': data.contratista_nombre,
            '79155480': data.contratista_cc,
            '79.155.480': data.contratista_cc,
            
            # Banco
            'Bancolombia': data.banco,
            '912-381559-89': data.numero_cuenta,
            'Daniel García Araque': data.titular_cuenta,
            '1000718485': data.cc_titular,
        }
        
        # Realizar reemplazos básicos
        for old_value, new_value in replacements.items():
            content = content.replace(old_value, str(new_value))
        
        # Reemplazar domicilios (más complejo debido a variaciones en el texto)
        content = re.sub(
            r'domicilio principal en el municipio de La Estrella, Antioquia',
            f'domicilio principal en el municipio de {data.contratante_domicilio}',
            content
        )
        
        content = re.sub(
            r'con domicilio en el municipio de\s+Sabaneta',
            f'con domicilio en el municipio de {data.contratista_domicilio}',
            content
        )
        
        content = re.sub(
            r'dirección: carera 40 # 71 sur-15',
            f'dirección: {data.contratista_direccion}',
            content
        )
        
        # Reemplazar objeto del contrato
        content = re.sub(
            r'prestará los servicios de:.*?Estos servicios',
            f'prestará los servicios de: {data.objeto_servicios}\nEstos servicios',
            content,
            flags=re.DOTALL
        )
        
        # Reemplazar valores monetarios y desglose de pagos
        content = self._replace_payment_section(content, data)
        
        # Reemplazar fecha de firma
        content = re.sub(
            r'Sabaneta, Antioquia a los siete \(14\) días del mes de enero',
            f'{data.lugar_firma} a los {data.fecha_firma}',
            content
        )
        
        # Reemplazar retención en la fuente
        content = content.replace('$ 1\'344.573', f'$ {data.retencion_minima}')
        
        # Reemplazar porcentaje de penalidad
        content = content.replace('20%', f'{data.penalidad_porcentaje}%')
        
        # Reemplazar días de gracia
        content = content.replace('(5) días', f'({data.dias_gracia}) días')
        
        return content
    
    def _replace_payment_section(self, content: str, data: ContractData) -> str:
        """Reemplaza la sección de honorarios con los valores correctos"""
        
        # Construir el texto de honorarios
        honorarios_text = f"la suma de: {data.valor_total_letras}, {NumberToSpanish.format_currency(data.valor_total)}"
        
        # Reemplazar el valor total
        content = re.sub(
            r'la suma de: SIETE MILLONES.*?\$ 7\'040\.667',
            honorarios_text,
            content,
            flags=re.DOTALL
        )
        
        # Construir el desglose de pagos
        if data.pagos:
            desglose = " discriminados de la siguiente manera:\n"
            for pago in data.pagos:
                concepto = pago.get('concepto', '')
                anticipo = pago.get('anticipo', 0)
                anticipo_letras = NumberToSpanish.convert(anticipo)
                anticipo_formato = NumberToSpanish.format_currency(anticipo)
                fecha_anticipo = pago.get('fecha_anticipo', '')
                
                saldo = pago.get('saldo', 0)
                saldo_letras = NumberToSpanish.convert(saldo)
                saldo_formato = NumberToSpanish.format_currency(saldo)
                
                desglose += f"• {concepto} pagaderos: {anticipo_letras} {anticipo_formato} el día {fecha_anticipo} y {saldo_letras} {saldo_formato} al momento de la entrega.\n"
            
            # Reemplazar el desglose completo
            pattern = r'discriminados de la siguiente manera:.*?El contratista podrá'
            replacement = desglose + "El contratista podrá"
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        return content


class PDFGenerator:
    """Genera el PDF del contrato con formato profesional"""
    
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.styles = self._create_styles()
    
    def _create_styles(self):
        """Crea los estilos para el documento PDF - Diseño profesional limpio"""
        from reportlab.lib import colors
        
        styles = getSampleStyleSheet()
        
        # Título principal - Elegante y profesional
        styles.add(ParagraphStyle(
            name='ContractTitle',
            fontSize=14,
            textColor=colors.black,
            spaceAfter=24,
            spaceBefore=0,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=18
        ))
        
        # Subtítulo CLÁUSULAS
        styles.add(ParagraphStyle(
            name='ContractSubtitle',
            fontSize=12,
            textColor=colors.black,
            spaceAfter=12,
            spaceBefore=18,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=14
        ))
        
        # Texto normal del contrato - Justificado perfectamente
        styles.add(ParagraphStyle(
            name='ContractBody',
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            spaceBefore=0,
            fontName='Times-Roman',
            textColor=colors.black,
            firstLineIndent=0,
            leftIndent=0,
            rightIndent=0
        ))
        
        # Títulos de cláusulas - Destacados pero profesionales
        styles.add(ParagraphStyle(
            name='ClauseTitle',
            fontSize=11,
            textColor=colors.black,
            spaceAfter=8,
            spaceBefore=16,
            fontName='Helvetica-Bold',
            leading=14,
            alignment=TA_JUSTIFY
        ))
        
        # PARÁGRAFO - Negrita
        styles.add(ParagraphStyle(
            name='SpecialParagraph',
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            spaceBefore=8,
            fontName='Times-Bold',
            textColor=colors.black
        ))
        
        return styles
    
    def generate(self, contract_content: str, contract_data: ContractData):
        """Genera el PDF del contrato con formato limpio y profesional"""
        from reportlab.lib import colors
        from reportlab.platypus import Table, TableStyle
        
        # Configuración del documento
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # === TÍTULO ===
        title = Paragraph("CONTRATO CIVIL DE PRESTACIÓN DE SERVICIOS", self.styles['ContractTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3 * inch))
        
        # === PROCESAR CONTENIDO ===
        # Limpiar y dividir contenido
        lines = [line.strip() for line in contract_content.split('\n')]
        
        i = 0
        clausulas_shown = False
        
        while i < len(lines):
            line = lines[i]
            
            # Saltar título (ya mostrado)
            if 'CONTRATO CIVIL DE PRESTACIÓN DE SERVICIOS' in line:
                i += 1
                continue
            
            # Mostrar CLÁUSULAS una sola vez
            if 'CLÁUSULAS' in line and not clausulas_shown:
                story.append(Spacer(1, 0.2 * inch))
                clausulas_para = Paragraph("CLÁUSULAS", self.styles['ContractSubtitle'])
                story.append(clausulas_para)
                story.append(Spacer(1, 0.15 * inch))
                clausulas_shown = True
                i += 1
                continue
            elif 'CLÁUSULAS' in line:
                i += 1
                continue
            
            # Detectar cláusulas (PRIMERA, SEGUNDA, etc.)
            if re.match(r'^(PRIMERA|SEGUNDA|TERCERA|CUARTA|QUINTA|SEXTA|SÉPTIMA|OCTAVA|NOVENA|DECIMA|DÉCIMA)', line, re.IGNORECASE):
                clause_para = Paragraph(line, self.styles['ClauseTitle'])
                story.append(clause_para)
                i += 1
                continue
            
            # Detectar PARÁGRAFO
            if line.startswith('PARÁGRAFO'):
                para_para = Paragraph(line, self.styles['SpecialParagraph'])
                story.append(para_para)
                i += 1
                continue
            
            # Saltar líneas de firma
            if line in ['EL CONTRATANTE', 'EL CONTRATISTA', '.'] or line.startswith('EDISÓN') or line.startswith('GERMÁN') or line.startswith('CC '):
                i += 1
                continue
            
            # Construir párrafos
            if line:
                paragraph_text = [line]
                i += 1
                
                # Continuar agregando líneas al mismo párrafo
                while i < len(lines):
                    next_line = lines[i]
                    
                    # Detener si es línea vacía, cláusula, o palabra clave
                    if (not next_line or 
                        'CLÁUSULAS' in next_line or
                        re.match(r'^(PRIMERA|SEGUNDA|TERCERA|CUARTA|QUINTA|SEXTA|SÉPTIMA|OCTAVA|NOVENA|DECIMA|DÉCIMA)', next_line, re.IGNORECASE) or
                        next_line.startswith('PARÁGRAFO') or
                        next_line in ['EL CONTRATANTE', 'EL CONTRATISTA', '.'] or
                        next_line.startswith('EDISÓN') or next_line.startswith('GERMÁN') or next_line.startswith('CC ')):
                        break
                    
                    paragraph_text.append(next_line)
                    i += 1
                
                # Crear párrafo
                full_text = ' '.join(paragraph_text)
                if len(full_text) > 5:  # Evitar párrafos muy cortos
                    para = Paragraph(full_text, self.styles['ContractBody'])
                    story.append(para)
            else:
                i += 1
        
        # === FIRMAS ===
        story.append(Spacer(1, 0.5 * inch))
        
        # Tabla de firmas con líneas profesionales
        firma_data = [
            ['', ''],
            ['_' * 50, '_' * 50],
            
            [contract_data.contratante_representante.upper(), contract_data.contratista_nombre.upper()],
            [f'CC: {contract_data.contratante_cc_representante}', f'CC: {contract_data.contratista_cc}']
        ]
        
        firma_table = Table(firma_data, colWidths=[3.25*inch, 3.25*inch])
        firma_table.setStyle(TableStyle([
            # Líneas de firma reales
            ('LINEABOVE', (0, 1), (0, 1), 1.5, colors.black),
            ('LINEABOVE', (1, 1), (1, 1), 1.5, colors.black),
            
            # Alineación
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            
            # Fuentes - Títulos
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica'),
            ('FONTSIZE', (0, 2), (-1, 2), 9),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.black),
            
            # Fuentes - Nombres
            ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 3), (-1, 3), 10),
            ('TEXTCOLOR', (0, 3), (-1, 3), colors.black),
            
            # Fuentes - CC
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica'),
            ('FONTSIZE', (0, 4), (-1, 4), 9),
            ('TEXTCOLOR', (0, 4), (-1, 4), colors.black),
            
            # Espaciado
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 1), (-1, 1), 0),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 8),
            ('TOPPADDING', (0, 2), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 2), (-1, -1), 4),
        ]))
        
        story.append(firma_table)
        
        # Construir PDF
        doc.build(story)


class ContractGeneratorBackend:
    """Backend principal del generador de contratos"""
    
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.template = ContractTemplate(template_path)
    
    def generate_contract(self, data: Dict[str, Any], output_path: str) -> str:
        """
        Genera un contrato PDF a partir de los datos proporcionados
        
        Args:
            data: Diccionario con los datos del contrato
            output_path: Ruta donde se guardará el PDF
        
        Returns:
            Ruta del archivo PDF generado
        """
        try:
            # Crear objeto de datos del contrato
            contract_data = ContractData(data)
            
            # Validar datos
            contract_data.validate()
            
            # Convertir valores monetarios a letras si no están proporcionados
            if not contract_data.valor_total_letras:
                contract_data.valor_total_letras = NumberToSpanish.convert(contract_data.valor_total)
            
            # Reemplazar placeholders en la plantilla
            contract_content = self.template.replace_placeholders(contract_data)
            
            # Generar PDF
            pdf_generator = PDFGenerator(output_path)
            pdf_generator.generate(contract_content, contract_data)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error al generar el contrato: {str(e)}")
    
    def validate_contract_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida los datos del contrato y retorna información sobre errores
        
        Args:
            data: Diccionario con los datos del contrato
        
        Returns:
            Diccionario con información de validación
        """
        try:
            contract_data = ContractData(data)
            contract_data.validate()
            return {
                'valid': True,
                'message': 'Datos válidos',
                'errors': []
            }
        except Exception as e:
            return {
                'valid': False,
                'message': str(e),
                'errors': [str(e)]
            }


# Funciones auxiliares para uso directo

def generate_contract_from_dict(data: Dict[str, Any], template_path: str, output_path: str) -> str:
    """
    Función de conveniencia para generar un contrato desde un diccionario
    
    Args:
        data: Datos del contrato
        template_path: Ruta de la plantilla
        output_path: Ruta de salida del PDF
    
    Returns:
        Ruta del PDF generado
    """
    backend = ContractGeneratorBackend(template_path)
    return backend.generate_contract(data, output_path)


def generate_contract_from_json(json_path: str, template_path: str, output_path: str) -> str:
    """
    Genera un contrato desde un archivo JSON
    
    Args:
        json_path: Ruta del archivo JSON con los datos
        template_path: Ruta de la plantilla
        output_path: Ruta de salida del PDF
    
    Returns:
        Ruta del PDF generado
    """
    import json
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return generate_contract_from_dict(data, template_path, output_path)
