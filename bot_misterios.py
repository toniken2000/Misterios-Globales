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


def generar_imagen(cat_nombre, titulo, cat_key):
  """Genera una imagen ilustrativa para el expediente y la guarda en la carpeta imagenes/."""
  prompt_imagen = (
      f"Ilustración fotorrealista, atmosférica y cinematográfica para un expediente "
      f"de investigación titulado '{titulo}', sobre la categoría '{cat_nombre}'. "
      f"Estilo misterioso, tonos oscuros, sin texto ni letras visibles en la imagen."
  )

  try:
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt_imagen,
    )

    for part in response.candidates[0].content.parts:
      if getattr(part, "inline_data", None) is not None:
        os.makedirs("imagenes", exist_ok=True)
        nombre_archivo = f"{cat_key}_{int(datetime.now().timestamp())}.png"
        ruta_relativa = f"imagenes/{nombre_archivo}"
        with open(ruta_relativa, "wb") as f:
          f.write(part.inline_data.data)
        return ruta_relativa

    print(f"⚠️ La respuesta de imagen para '{cat_nombre}' no incluyó datos de imagen.")
    return None
  except Exception as e:
    print(f"Error al generar imagen para '{cat_nombre}': {e}")
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
    print(f"Generando expediente para: {cat_nombre}...")
    texto_generado = generar_expediente(cat_key, cat_nombre, url)

    if not texto_generado:
      print(f"❌ No se pudo generar el expediente de {cat_nombre}. Se omite.")
      continue

    # Procesar la respuesta para separar título y contenido
    titulo = f"Expediente del Día: {cat_nombre}"
    contenido = texto_generado

    if "TITULO:" in texto_generado and "CONTENIDO:" in texto_generado:
      partes = texto_generado.split("CONTENIDO:")
      titulo = partes[0].replace("TITULO:", "").strip()
      contenido = partes[1].strip()

    print(f"Generando imagen para: {cat_nombre}...")
    ruta_imagen = generar_imagen(cat_nombre, titulo, cat_key)

    fecha_actual = datetime.now().strftime("%d/%m/%Y - %H:%M")

    nuevos_expedientes.append({
        "titulo": titulo,
        "categoria": cat_nombre,
        "fecha": f"Expediente registrado el {fecha_actual}",
        "contenido": contenido.replace("\n", "<br>"),
        "imagen": ruta_imagen,
    })

  if not nuevos_expedientes:
    print("❌ No se generó ningún expediente nuevo en esta ejecución.")
    return

  # Añadir los nuevos expedientes al principio de la lista
  expedientes = nuevos_expedientes + expedientes

  # Mantener solo los últimos 20 expedientes para no sobrecargar la web
  expedientes = expedientes[:20]

  # GUARDAR EN EL ARCHIVO NOTICIAS.JSON
  with open("noticias.json", "w", encoding="utf-8") as f:
    json.dump(expedientes, f, ensure_ascii=False, indent=2)

  print(f"\n✅ {len(nuevos_expedientes)} EXPEDIENTES NUEVOS GUARDADOS CON ÉXITO EN noticias.json.")


if __name__ == "__main__":
  main()
