# Datos de Contratos

Esta carpeta contiene archivos JSON con datos para generar contratos.

## 📊 Estructura de Datos

Ver `example_data.json` para la estructura completa.

## 🔐 Seguridad

- Los archivos JSON no se suben al repositorio (ver `.gitignore`)
- No incluyas datos sensibles en `example_data.json`
- Mantén backup de datos importantes

## 📝 Uso

```python
from contract_generator import generate_contract_from_json

generate_contract_from_json(
    json_path="datos/mi_contrato.json",
    template_path="templates/contrato_ejemplo.txt",
    output_path="contratos_generados/mi_contrato.pdf"
)
```
