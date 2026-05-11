import { onMount } from "solid-js"
import L from "leaflet"
import "leaflet/dist/leaflet.css"
import "leaflet.markercluster/dist/MarkerCluster.css"
import "leaflet.markercluster/dist/MarkerCluster.Default.css"
import "leaflet.markercluster"

function Map() {
  let mapDiv;

  onMount(async () => {
    const map = L.map(mapDiv).setView([-31.42497, -62.08404], 14);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    const res = await fetch("/noticias.json");
    const noticias = await res.json();

    const cluster = L.markerClusterGroup();

    noticias.forEach(noticia => {
      if (!noticia.lat || !noticia.lon) return;

      const marker = L.marker([noticia.lat, noticia.lon]);

      marker.bindPopup(`
      <div style="width: 250px; font-family: sans-serif;">
        <p style="font-size: 14px; font-weight: bold; margin: 0 0 6px 0; line-height: 1.4;">
          ${noticia.titulo}
        </p>
        <p style="font-size: 12px; color: #666; margin: 0 0 10px 0;">
          ${noticia.lugar}
        </p>
        <a 
          href="${noticia.url}" 
          target="_blank"
          style="font-size: 13px; color: #2563eb; text-decoration: none; font-weight: 500;"
        >
          Leer nota →
        </a>
      </div>
    `,{ maxWidth: 280 });

      cluster.addLayer(marker);
    });

    map.addLayer(cluster);
  });

  return (
    <div class="w-full flex justify-center">
      <div ref={mapDiv} style="height: 800px; width: 80%;"></div>
    </div>
  );
}

export default Map;