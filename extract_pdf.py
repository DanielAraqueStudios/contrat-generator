"""
Script para extraer texto del PDF de referencia
"""

from pypdf import PdfReader

def extract_pdf_text(pdf_path):
    """Extrae todo el texto de un PDF"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    pdf_path = r"c:\Users\danie\Downloads\CONTRATO_DULCES_EL_TRAPICHE (1).pdf"
    text = extract_pdf_text(pdf_path)
    
    if text:
        # Guardar en archivo para análisis
        with open("reference_contract.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("✅ Texto extraído y guardado en: reference_contract.txt")
        print("\n" + "="*60)
        print("CONTENIDO DEL PDF:")
        print("="*60)
        print(text)
    else:
        print("❌ No se pudo extraer el texto")
