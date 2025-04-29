
function initializeMap(restaurants, user) {
    const map = L.map('map').setView([user.lat, user.lng], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
  
    // red user marker icon
    const redIcon = new L.Icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
  
    // User marker with red icon
    L.marker([user.lat, user.lng], {icon: redIcon, title: 'You'}).addTo(map).bindPopup('You are here');
  
    restaurants.forEach(r => {
      const marker = L.marker([r.lat, r.lng]).addTo(map);
      marker.bindPopup(`
        <b>${r.name}</b><br>
        Distance: ${r.distance_km} km<br>
        Prep time: ${r.Preparation_Time_min} min<br>
        <a href='/order/${r.id}'>Order here</a>
      `);
    });
  }
  
  if (typeof restaurants !== 'undefined' && typeof user !== 'undefined') {
    initializeMap(restaurants, user);
  }
  