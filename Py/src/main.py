import os
import json
import httpx
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
URL_BASE = "https://www.lavozdesanjusto.com.ar"


def geocodificar(lugar):
    try:
        r = requests.get(
            "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates",
            params={
                "SingleLine": f"{lugar}, Argentina",
                "f": "json",
                "maxLocations": 1,
                "outFields": "Match_addr"
            },
            timeout=10
        )
        candidatos = r.json().get("candidates", [])
        if candidatos:
            loc = candidatos[0]["location"]
            return loc["y"], loc["x"]
    except Exception as e:
        print(f"ArcGIS error: {e}")

    return -31.4249815, -62.0840299


def extraer_lugar(titulo, contenido):
    respuesta = httpx.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "temperature": 0.1,
            "max_tokens": 30,
            "messages": [
                {"role": "system", "content": "Extraé el lugar más específico donde ocurrió el hecho (calle, barrio, ciudad). Devolvé SOLO el nombre del lugar, nada más. Ejemplos: 'Calle Fleming, San Francisco, Córdoba' o 'Barrio Cottolengo, San Francisco, Córdoba'"},
                {"role": "user", "content": f"Título: {titulo}\n\n{contenido}"}
            ],
        },
        timeout=20,
    )
    return respuesta.json()["choices"][0]["message"]["content"].strip()


def main():
    response = requests.get(f"{URL_BASE}/categoria/policiales")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    noticias = []

    for h2 in soup.find_all('h2'):
        titulo = h2.get_text(strip=True)
        parent_a = h2.find_parent('a')
        if not parent_a:
            continue

        link = f"{URL_BASE}{parent_a.get('href')}"

        articulo = requests.get(link)
        soup_art = BeautifulSoup(articulo.text, 'html.parser')
        for tag in soup_art(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        contenido = soup_art.get_text(separator=" ", strip=True)[:3000]

        lugar = extraer_lugar(titulo, contenido)
        lat, lon = geocodificar(lugar)

        print(json.dumps({
            "titulo": titulo,
            "url": link,
            "lugar": lugar,
            "lat": lat,
            "lon": lon
        }, ensure_ascii=False, indent=2))

        noticias.append({
            "titulo": titulo,
            "url": link,
            "lugar": lugar,
            "lat": lat,
            "lon": lon
        })

    output_path = r"C:/Users/Leper/OneDrive/Escritorio/NewRadar/website/public/noticias.json" 
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(noticias, f, ensure_ascii=False, indent=2)
    
    print(f"{len(noticias)} noticias guardadas en {output_path}")

main()