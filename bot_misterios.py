from datetime import datetime
import json
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
  """Genera la estructura de un expediente utilizando Gemini 2.5 Flash en formato JSON simple."""
  prompt = f"""
    Actúa como un investigador experto en misterios, enigmas históricos, sucesos paranormales y arqueología.
    Genera un expediente detallado y cautivador para la sección '{cat_nombre}' ({cat_key}).
    
    Referencia / Contexto: {url}
    
    Devuelve la respuesta ÚNICAMENTE en este formato de texto claro:
    TITULO: [Escribe aquí un título impactante]
    CONTENIDO: [Escribe aquí el resumen, antecedentes, hallazgos y conclusión en párrafos limpios sin usar Markdown complejo]
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

  cat_key = "arqueologia"
  cat_nombre = "Arqueología Prohibida y Objetos Fuera de Tiempo"
  url = "https://misteriosglobales.com"

  print(f"Generando expediente para: {cat_nombre}...")

  texto_generado = generar_expediente(cat_key, cat_nombre, url)

  if texto_generado:
    # Procesar la respuesta para separar título y contenido
    titulo = "Expediente del Día: " + cat_nombre
    contenido = texto_generado

    if "TITULO:" in texto_generado and "CONTENIDO:" in texto_generado:
      partes = texto_generado.split("CONTENIDO:")
      titulo = partes[0].replace("TITULO:", "").strip()
      contenido = partes[1].strip()

    # Formatear la fecha actual en español
    fecha_actual = datetime.now().strftime("%d/%m/%Y - %H:%M")

    # Crear la lista de expedientes
    noticia_nueva = {
        "titulo": titulo,
        "fecha": f"Expediente registrado el {fecha_actual}",
        "contenido": contenido.replace("\n", "<br>"),
    }

    # Cargar expedientes anteriores si ya existen para no borrarlos
    expedientes = []
    if os.path.exists("noticias.json"):
      try:
        with open("noticias.json", "r", encoding="utf-8") as f:
          expedientes = json.load(f)
      except Exception:
        expedientes = []

    # Añadir el nuevo expediente al principio de la lista
    expedientes.insert(0, noticia_nueva)

    # Mantener solo los últimos 10 expedientes para no sobrecargar la web
    expedientes = expedientes[:10]

    # GUARDAR EN EL ARCHIVO NOTICIAS.JSON (Esto es lo que faltaba)
    with open("noticias.json", "w", encoding="utf-8") as f:
      json.dump(expedientes, f, ensure_ascii=False, indent=2)

    print("\n✅ ARCHIVO noticias.json GUARDADO Y ACTUALIZADO CON ÉXITO.")
  else:
    print("❌ No se pudo completar la generación del expediente.")


if __name__ == "__main__":
  main()
