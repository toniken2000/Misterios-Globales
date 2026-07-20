import os
import sys
from google import genai

# 1. Configuración del cliente con la API Key desde los Secrets de GitHub
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: La variable de entorno GEMINI_API_KEY no está configurada.")
    sys.exit(1)

client = genai.Client(api_key=api_key)


def generar_expediente(cat_key, cat_nombre, url):
    """
    Genera la estructura de un expediente de investigación utilizando Gemini 2.5 Flash.
    """
    prompt = f"""
    Actúa como un investigador experto en misterios, enigmas históricos, sucesos paranormales y arqueología.
    Genera un expediente detallado y cautivador para la sección '{cat_nombre}' ({cat_key}).
    
    Referencia / Contexto: {url}
    
    Estructura requerida del informe:
    1. Título sugerente e impactante.
    2. Resumen ejecutivo del caso.
    3. Antecedentes y contexto histórico.
    4. Anomalyas, hallazgos o testimonios clave.
    5. Conclusión abierta y preguntas para la comunidad de investigadores.
    
    Usa un tono divulgativo, riguroso pero lleno de intriga.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error al generar contenido con la API de Gemini: {e}")
        return None


def main():
    print("=== Iniciando Bot de Misterios Globales ===")

    # Parámetros de prueba / ejecución
    cat_key = "arqueologia"
    cat_nombre = "Arqueología Prohibida y Objetos Fuera de Tiempo"
    url = "https://misteriosglobales.com"

    print(f"Generando expediente para: {cat_nombre}...")

    expediente = generar_expediente(cat_key, cat_nombre, url)

    if expediente:
        print("\n" + "=" * 50)
        print(" EXPEDIENTE GENERADO CON ÉXITO")
        print("=" * 50 + "\n")
        print(expediente)
        print("\n" + "=" * 50)
    else:
        print("No se pudo completar la generación del expediente.")


if __name__ == "__main__":
    main()
