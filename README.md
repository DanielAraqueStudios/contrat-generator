# 📄 Generador de Contratos Colombianos

Sistema backend para generación automática de contratos civiles de prestación de servicios en Colombia.

## 🎯 Características

- ✅ Generación de contratos PDF desde plantillas
- ✅ Conversión automática de números a letras (español colombiano)
- ✅ Validación de datos contractuales
- ✅ Formato profesional con estilos optimizados
- ✅ Manejo de múltiples pagos y desgloses
- ✅ Preservación de terminología jurídica colombiana
- ✅ Verificación de coherencia documental

## 📦 Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🚀 Uso

### 1. Preparar datos del contrato

Crea un archivo JSON con los datos del contrato (ver `example_data.json`):

```json
{
  "contratante_razon_social": "Empresa S.A.S",
  "contratante_nit": "123456789-0",
  "contratante_representante": "Nombre Representante",
  "contratante_cc_representante": "12345678",
  "contratante_domicilio": "Ciudad, Departamento",
  "contratante_direccion": "Dirección completa",
  
  "contratista_nombre": "NOMBRE CONTRATISTA",
  "contratista_cc": "98765432",
  "contratista_domicilio": "Ciudad",
  "contratista_direccion": "Dirección completa",
  
  "objeto_servicios": "Descripción detallada de servicios...",
  
  "valor_total": 5000000,
  "valor_total_letras": "",
  
  "pagos": [
    {
      "concepto": "Servicio 1",
      "anticipo": 2500000,
      "fecha_anticipo": "15 de febrero de 2025",
      "saldo": 2500000
    }
  ],
  
  "banco": "Banco",
  "tipo_cuenta": "cuenta de ahorros",
  "numero_cuenta": "123-456789-01",
  "titular_cuenta": "Titular Cuenta",
  "cc_titular": "12345678",
  
  "fecha_firma": "quince (15) días del mes de febrero de 2025",
  "lugar_firma": "Ciudad, Departamento"
}
```

### 2. Generar contrato

#### Opción A: Desde archivo JSON

```python
from contract_generator import generate_contract_from_json

# Generar contrato
pdf_path = generate_contract_from_json(
    json_path="datos_contrato.json",
    template_path="contrato_ejemplo.txt",
    output_path="contrato_generado.pdf"
)

print(f"Contrato generado: {pdf_path}")
```

#### Opción B: Desde diccionario Python

```python
from contract_generator import generate_contract_from_dict

data = {
    "contratante_razon_social": "Mi Empresa S.A.S",
    "contratante_nit": "123456789-0",
    # ... resto de datos
}

pdf_path = generate_contract_from_dict(
    data=data,
    template_path="contrato_ejemplo.txt",
    output_path="mi_contrato.pdf"
)
```

#### Opción C: Usando la clase Backend

```python
from contract_generator import ContractGeneratorBackend

# Inicializar backend
backend = ContractGeneratorBackend("contrato_ejemplo.txt")

# Validar datos antes de generar
validation = backend.validate_contract_data(data)
if validation['valid']:
    # Generar contrato
    pdf_path = backend.generate_contract(data, "salida.pdf")
else:
    print(f"Errores de validación: {validation['errors']}")
```

### 3. Ejecutar pruebas

```bash
python test_generator.py
```

## 📊 Estructura de Datos

### Campos Obligatorios
- `contratante_razon_social`: Razón social del contratante
- `contratante_nit`: NIT del contratante
- `contratista_nombre`: Nombre completo del contratista
- `contratista_cc`: Cédula del contratista
- `objeto_servicios`: Descripción de servicios a prestar
- `valor_total`: Valor total del contrato (número)

### Campos Opcionales
- `valor_total_letras`: Se genera automáticamente si no se proporciona
- `retencion_minima`: Default "1'344.573"
- `penalidad_porcentaje`: Default "20"
- `dias_gracia`: Default "5"
- `fecha_firma`: Default fecha actual
- `lugar_firma`: Ciudad y departamento

### Estructura de Pagos

```json
"pagos": [
  {
    "concepto": "Descripción del servicio",
    "anticipo": 1000000,
    "fecha_anticipo": "dd de mes de año",
    "saldo": 500000
  }
]
```

## 🔧 API del Backend

### `ContractGeneratorBackend`

```python
class ContractGeneratorBackend:
    def __init__(self, template_path: str)
    def generate_contract(self, data: Dict, output_path: str) -> str
    def validate_contract_data(self, data: Dict) -> Dict
```

### `ContractData`

Clase que encapsula y valida los datos del contrato.

```python
class ContractData:
    def __init__(self, data: Dict[str, Any])
    def validate(self) -> bool
```

### `NumberToSpanish`

Utilidad para conversión de números.

```python
class NumberToSpanish:
    @staticmethod
    def convert(number: float) -> str  # Convierte a letras
    
    @staticmethod
    def format_currency(number: float) -> str  # Formatea como moneda
```

### `PDFGenerator`

Genera PDFs con formato profesional.

```python
class PDFGenerator:
    def __init__(self, output_path: str)
    def generate(self, contract_content: str, contract_data: ContractData)
```

## 🎨 Personalización

### Modificar Plantilla

Edita `contrato_ejemplo.txt` con tu propia plantilla. El sistema automáticamente identificará y reemplazará:
- Nombres de partes contratantes
- Valores monetarios
- Fechas
- Datos bancarios
- Direcciones
- Objetos contractuales

### Modificar Estilos PDF

Edita la clase `PDFGenerator` en `contract_generator.py`:

```python
def _create_styles(self):
    # Personaliza fuentes, tamaños, espaciados, etc.
    styles.add(ParagraphStyle(
        name='ContractTitle',
        fontSize=14,
        # ... más opciones
    ))
```

## 🔍 Validación

El sistema valida:
- ✅ Campos obligatorios presentes
- ✅ Formato de valores monetarios
- ✅ Coherencia de datos
- ✅ Estructura de pagos

## 🐛 Manejo de Errores

```python
try:
    pdf_path = backend.generate_contract(data, "output.pdf")
except ValueError as e:
    print(f"Error de validación: {e}")
except Exception as e:
    print(f"Error al generar contrato: {e}")
```

## 📝 Notas Legales

- Este sistema genera contratos basados en plantillas
- Los contratos generados deben ser revisados por un profesional legal
- Asegúrate de cumplir con la normativa vigente colombiana
- Las cláusulas incluidas son referenciales

## 🤝 Soporte

Para reportar problemas o sugerir mejoras, contacta al desarrollador.

## 📄 Licencia

Sistema desarrollado para uso interno de generación de contratos.

---

**Versión:** 1.0.0  
**Última actualización:** Noviembre 2025
