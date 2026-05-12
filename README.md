# 📍 NewsRadar

Mapa interactivo de noticias policiales locales, actualizado diariamente de forma automática.

NewsRadar scrapea el diario [La Voz de San Justo](https://www.lavozdesanjusto.com.ar/categoria/policiales), usa IA para extraer la ubicación geográfica de cada hecho y la muestra como un punto en un mapa interactivo.

---

## ¿Cómo funciona?

```
Diario online
    → Python scrapea las noticias (BeautifulSoup)
    → LLaMA 3 vía Groq extrae el lugar del hecho
    → ArcGIS convierte el lugar en coordenadas (lat/lon)
    → Se guarda en Supabase
    → SolidJS + Leaflet muestra el mapa
```

---

## Stack

### Backend (Python)
- `requests` + `BeautifulSoup` — scraping del HTML del diario
- `Groq API` + `LLaMA 3.3 70B` — extracción del lugar mediante IA
- `ArcGIS Geocoding API` — conversión de texto a coordenadas geográficas
- `Supabase` — base de datos donde se almacenan las noticias

### Frontend (SolidJS)
- `SolidJS` + `Vite` + `TailwindCSS` — framework y estilos
- `Leaflet` + `leaflet.markercluster` — mapa interactivo con agrupación de markers

### Infraestructura
- `Render` — cron job diario que ejecuta el scraper
- `Supabase` — almacenamiento y API de datos
- `Vercel` — deploy del frontend

> Todo el stack utiliza planes gratuitos.

---

## Estructura del proyecto

```
NewsRadar/
├── Py/
│   └── src/
│       └── main.py        # Scraper + extracción IA + geocoding
├── website/
│   ├── public/
│   │   └── noticias.json  # JSON generado (desarrollo local)
│   └── src/
│       └── components/
│           └── Map.jsx    # Componente del mapa
```

---

## Instalación local

### Requisitos
- Python 3.10+
- Node.js + pnpm

### Backend

```bash
cd Py
pip install requests beautifulsoup4 httpx python-dotenv
```

Creá un archivo `.env` en `Py/src/`:

```env
GROQ_API_KEY=tu_api_key_de_groq
```

Corrés el scraper:

```bash
python src/main.py
```

Genera `website/public/noticias.json` con todas las noticias del día.

### Frontend

```bash
cd website
pnpm install
pnpm dev
```

---

## Formato del JSON generado

```json
[
  {
    "titulo": "Dos choques en calle Fleming durante la tarde del viernes",
    "url": "https://www.lavozdesanjusto.com.ar/...",
    "lugar": "Calle Fleming, San Francisco, Córdoba",
    "lat": -31.434822,
    "lon": -62.090626
  }
]
```

---

## Funcionalidades del mapa

- 📍 Marker por cada noticia con ubicación detectada
- 🔵 Clustering automático — cuando hay varias noticias cercanas se agrupan en un círculo con el número total
- 🪟 Popup con título, lugar y link a la nota original
- 🗺️ Centrado en San Francisco, Córdoba por defecto

---

## API Keys necesarias

| Servicio | Uso | Costo |
|----------|-----|-------|
| [Groq](https://console.groq.com) | Extracción de lugares con IA | Gratuito |
| [ArcGIS](https://developers.arcgis.com) | Geocoding | Gratuito |
| [Supabase](https://supabase.com) | Base de datos | Gratuito |

---

## Autor

Hecho con 🧉 en San Francisco, Córdoba, Argentina.