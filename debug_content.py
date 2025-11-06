"""
Debug script to see what content is being processed
"""

from contract_generator import ContractTemplate, ContractData
import json

# Load data
with open("datos/example_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Create contract data
contract_data = ContractData(data)

# Load and process template
template = ContractTemplate("templates/contrato_ejemplo.txt")
processed_content = template.replace_placeholders(contract_data)

# Save processed content
with open("debug_processed_content.txt", "w", encoding="utf-8") as f:
    f.write(processed_content)

print("✅ Contenido procesado guardado en: debug_processed_content.txt")
print("\n" + "="*60)
print("LONGITUD DEL CONTENIDO:")
print("="*60)
print(f"Template original: {len(template.template_content)} caracteres")
print(f"Contenido procesado: {len(processed_content)} caracteres")
print(f"Líneas en template: {len(template.template_content.split(chr(10)))}")
print(f"Líneas procesadas: {len(processed_content.split(chr(10)))}")

print("\n" + "="*60)
print("PRIMERAS 500 CARACTERES:")
print("="*60)
print(processed_content[:500])

print("\n" + "="*60)
print("ÚLTIMAS 500 CARACTERES:")
print("="*60)
print(processed_content[-500:])
