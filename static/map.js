function initializeMap(restaurants, user) {
    const map = L.map('map').setView([user.lat, user.lng], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
  
    // User marker
    L.marker([user.lat, user.lng], {title: 'You'}).addTo(map).bindPopup('You are here');
  
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
  
  // when loaded
  if (typeof restaurants !== 'undefined' && typeof user !== 'undefined') {
    initializeMap(restaurants, user);
  }
  