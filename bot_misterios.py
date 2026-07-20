import os
import json
import feedparser
import os
from google import genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

FEEDS = {
    "crimen": ("Crimen Real", "https://news.google.com/rss/search?q=true+crime+investigacion&hl=es"),
    "arqueologia": ("Arqueología", "https://news.google.com/rss/search?q=descubrimiento+arqueologico&hl=es"),
    "mar_aire": ("Mar y Aire", "https://news.google.com/rss/search?q=misterio+maritimo+o+aviacion&hl=es"),
    "paranormal": ("Paranormal", "https://news.google.com/rss/search?q=UAP+fenomeno+anomalo+desclasificado&hl=es")
}

def generar_expediente(cat_key, cat_nombre, url):
    parsed = feedparser.parse(url)
    if not parsed.entries:
        return None
    entry = parsed.entries[0]
    
    prompt = f"""
    Eres el editor de un portal de misterio. Redacta una ficha rápida en JSON sobre esta noticia:
    Título: {entry.title}
    Resumen: {entry.summary}
    
    Responde ÚNICAMENTE en formato JSON válido con estas claves:
    {{
        "titulo": "Título atractivo de 8 palabras máximo",
        "resumen": "Redacción de 3 párrafos cortos explicando el suceso con rigor.",
        "destacado": "Una frase corta intrigante o dato impactante sobre el caso",
        "fuente": "Nombre del medio original"
    }}
    """
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

res = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

    
    try:
        texto = res.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(texto)
        data["categoria"] = cat_key
        data["categoria_nombre"] = cat_nombre
        return data
    except Exception as e:
        print(f"Error procesando {cat_key}: {e}")
        return None

if __name__ == "__main__":
    expedientes = []
    for cat_key, (cat_nombre, url) in FEEDS.items():
        exp = generar_expediente(cat_key, cat_nombre, url)
        if exp:
            expedientes.append(exp)
            
    with open("noticias.json", "w", encoding="utf-8") as f:
        json.dumps(expedientes, f, ensure_ascii=False, indent=2)
