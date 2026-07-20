import os
import sys
from google import genai

# Initialize the Gemini client using the API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: La variable de entorno GEMINI_API_KEY no está configurada.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

def generar_expediente(cat_key, cat_nombre, url):
    """
    Función para generar un expediente o artículo de misterio usando Gemini 2.5 Flash.
    """
    prompt = f"""
    Actúa como un investigador experto en misterios, enigmas históricos y arqueología.
    Genera un expediente detallado y atractivo para la categoría '{cat_nombre}' ({cat_key}).
    
    Referencia o tema de origen: {url}
    
    El informe debe incluir:
    1. Título impactante.
    2. Contexto histórico o antecedentes del suceso.
    3. Hallazgos o evidencias principales.
    4. Conclusión abierta o preguntas para la comunidad.
    
    Redacta en un estilo divulgativo, riguroso pero misterioso.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error al generar contenido con Gemini: {e}")
        return None

def main():
    print("Iniciando Bot de Misterios Globales...")
    
    # Datos de ejemplo o prueba (ajusta según tus necesidades)
    cat_key = "arqueologia"
    cat_nombre = "Arqueología Prohibida"
    url = "https://misteriosglobales.com"
    
    expediente = generar_expediente(cat_key, cat_nombre, url)
    
    if expediente:
        print("\n--- EXPEDIENTE GENERADO CON ÉXITO ---\n")
        print(expediente)
        print("\n------------------------------------\n")
    else:
        print("No se pudo generar el expediente.")

if __name__ == "__main__":
    main()
