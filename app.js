const myMap = L.map('map').setView([18.5204, 73.8567], 5); 
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const attribution ='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
L.tileLayer(tileUrl, { attribution }).addTo(myMap);


function generateList(stores) {
  const ul = document.querySelector('.list');
  ul.innerHTML = '';

  stores.forEach((shop) => {
    const li = document.createElement('li');
    const div = document.createElement('div');
    const a = document.createElement('a');
    const p = document.createElement('p');

    a.innerText = shop.properties.name;
    a.href = '#';
    a.addEventListener('click', () => flyToStore(shop));

    p.innerText = shop.properties.address;

    div.classList.add('shop-item');
    div.appendChild(a);
    div.appendChild(p);
    li.appendChild(div);
    ul.appendChild(li);
  });
}

function makePopupContent(shop) {
  return `
    <div>
      <h4>${shop.properties.name}</h4>
      <p>${shop.properties.address}</p>
      <div class="phone-number">
        <a>${shop.properties.phone}</a>
      </div>
    </div>
  `;
}

function onEachFeature(feature, layer) {
  layer.bindPopup(makePopupContent(feature));
}

let shopsLayer = L.geoJSON(storeList, {
  onEachFeature: onEachFeature,
  pointToLayer: (feature, latlng) => L.marker(latlng)
}).addTo(myMap);

function flyToStore(store) {
  const lat = store.geometry.coordinates[1];
  const lng = store.geometry.coordinates[0];
  myMap.flyTo([lat, lng], 14);
}

generateList(storeList);

const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('input', () => {
  const query = searchInput.value.toLowerCase();

  const filteredStores = storeList.filter(store => 
    store.properties.name.toLowerCase().includes(query) ||
    store.properties.sector.toLowerCase().includes(query)
  );

  generateList(filteredStores);

  
});
