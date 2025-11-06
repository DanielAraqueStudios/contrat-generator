"""
Script simple para probar la generación de PDF
"""

from contract_generator import generate_contract_from_json
import os

def test_pdf_generation():
    """Genera un PDF de prueba usando los datos de ejemplo"""
    
    print("=" * 60)
    print("PROBANDO GENERACIÓN DE PDF")
    print("=" * 60)
    
    # Rutas de archivos
    json_path = "datos/example_data.json"
    template_path = "templates/contrato_ejemplo.txt"
    output_path = "contratos_generados/contrato_test.pdf"
    
    print(f"\n📄 Plantilla: {template_path}")
    print(f"📊 Datos JSON: {json_path}")
    print(f"💾 PDF de salida: {output_path}")
    print("\n🚀 Generando contrato...\n")
    
    try:
        # Generar el contrato
        result_path = generate_contract_from_json(
            json_path=json_path,
            template_path=template_path,
            output_path=output_path
        )
        
        print("=" * 60)
        print("✅ ¡CONTRATO GENERADO EXITOSAMENTE!")
        print("=" * 60)
        print(f"\n📍 Ubicación: {os.path.abspath(result_path)}")
        
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            print(f"📦 Tamaño: {file_size:,} bytes")
            print(f"\n💡 Abre el archivo para verificar el PDF:")
            print(f"   {os.path.abspath(result_path)}")
        
        return True
        
    except Exception as e:
        print("=" * 60)
        print("❌ ERROR AL GENERAR CONTRATO")
        print("=" * 60)
        print(f"\n{str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_pdf_generation()
