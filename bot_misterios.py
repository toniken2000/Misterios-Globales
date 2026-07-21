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

# Las 4 categorías que se generan en cada ejecución
CATEGORIAS = [
    ("arqueologia", "Arqueología Prohibida y Objetos Fuera de Tiempo", "https://misteriosglobales.com"),
    ("ovnis", "Avistamientos OVNI y Fenómenos Aéreos No Identificados", "https://misteriosglobales.com"),
    ("civilizaciones", "Civilizaciones Perdidas y Ruinas Ancestrales", "https://misteriosglobales.com"),
    ("conspiracion", "Conspiraciones y Secretos Ocultos", "https://misteriosglobales.com"),
]


def generar_expediente(cat_key, cat_nombre, url):
  """Genera la estructura de un expediente utilizando Gemini en formato de texto simple."""
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
        model="gemini-flash-latest", contents=prompt
    )
    return response.text
  except Exception as e:
    print(f"Error al generar contenido con la API de Gemini ({cat_nombre}): {e}")
    return None


def main():
  print("=== Iniciando Bot de Misterios Globales ===")

  # Cargar expedientes anteriores si ya existen para no borrarlos
  expedientes = []
  if os.path.exists("noticias.json"):
    try:
      with open("noticias.json", "r", encoding="utf-8") as f:
        expedientes = json.load(f)
    except Exception:
      expedientes = []

  nuevos_expedientes = []

  for cat_key, cat_nombre, url in CATEGORIAS:
    print(f"Gen
