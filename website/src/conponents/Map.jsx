import { onMount } from "solid-js"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

function Map(){
  let mapDiv;
  let map;

  onMount(() => {
    map = L.map(mapDiv).setView([-31.42497, -62.08404],14);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
  })

  return(
    <div class="w-full flex justify-center">
      <div ref={mapDiv} style="height: 800px; width: 80%;"></div>
    </div>
  )
}

export default Map