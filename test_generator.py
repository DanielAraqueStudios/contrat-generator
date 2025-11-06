"""
Script de prueba para el generador de contratos
"""

import os
from contract_generator import ContractGeneratorBackend, generate_contract_from_json

def test_basic_generation():
    """Prueba básica de generación de contrato"""
    
    # Rutas
    template_path = "templates/contrato_ejemplo.txt"
    json_path = "datos/example_data.json"
    output_path = "contratos_generados/contrato_generado.pdf"
    
    print("🚀 Iniciando generación de contrato...")
    print(f"📄 Plantilla: {template_path}")
    print(f"📊 Datos: {json_path}")
    print(f"💾 Salida: {output_path}")
    print("-" * 50)
    
    try:
        # Generar contrato
        result = generate_contract_from_json(json_path, template_path, output_path)
        
        print("✅ ¡Contrato generado exitosamente!")
        print(f"📍 Ubicación: {os.path.abspath(result)}")
        
        # Verificar que el archivo existe
        if os.path.exists(result):
            file_size = os.path.getsize(result)
            print(f"📦 Tamaño del archivo: {file_size:,} bytes")
        
    except Exception as e:
        print(f"❌ Error al generar contrato: {e}")
        raise


def test_validation():
    """Prueba de validación de datos"""
    
    print("\n🔍 Probando validación de datos...")
    print("-" * 50)
    
    backend = ContractGeneratorBackend("templates/contrato_ejemplo.txt")
    
    # Datos válidos
    valid_data = {
        "contratante_razon_social": "Test S.A.S",
        "contratante_nit": "123456789-0",
        "contratista_nombre": "Juan Pérez",
        "contratista_cc": "123456789",
        "objeto_servicios": "Servicios de prueba",
        "valor_total": 1000000
    }
    
    result = backend.validate_contract_data(valid_data)
    
    if result['valid']:
        print("✅ Validación exitosa")
    else:
        print(f"❌ Validación fallida: {result['message']}")
    
    # Datos inválidos (falta campo obligatorio)
    invalid_data = {
        "contratante_razon_social": "Test S.A.S",
        # Falta contratante_nit
    }
    
    result = backend.validate_contract_data(invalid_data)
    
    if not result['valid']:
        print(f"✅ Validación correctamente detectó error: {result['message']}")
    else:
        print("❌ Validación no detectó error esperado")


def test_number_conversion():
    """Prueba de conversión de números a letras"""
    
    from contract_generator import NumberToSpanish
    
    print("\n🔢 Probando conversión de números a letras...")
    print("-" * 50)
    
    test_numbers = [
        1000000,
        7040667,
        2904400,
        1320000,
        500000
    ]
    
    for number in test_numbers:
        text = NumberToSpanish.convert(number)
        formatted = NumberToSpanish.format_currency(number)
        print(f"{formatted:>20} -> {text}")


if __name__ == "__main__":
    print("=" * 50)
    print("GENERADOR DE CONTRATOS - SUITE DE PRUEBAS")
    print("=" * 50)
    
    # Ejecutar pruebas
    test_number_conversion()
    test_validation()
    test_basic_generation()
    
    print("\n" + "=" * 50)
    print("✅ Todas las pruebas completadas")
    print("=" * 50)
