(() => {
  if (!window.L) return;
  const map = L.map('world-map').setView([25, 0], 2);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO'
  }).addTo(map);

  const points = [
    {name:'USS Nimitz (2004)', lat:32.7, lon:-117.2, category:'uap'},
    {name:'Nazca Lines (Peru)', lat:-14.7, lon:-75.1, category:'ancient'},
    {name:'Pentagon UAP Report (DC)', lat:38.9, lon:-77.0, category:'disclosure'}
  ];
  points.forEach((p) => L.circleMarker([p.lat,p.lon], {radius:7,color:'#3b82f6'}).addTo(map).bindPopup(p.name));
})();
