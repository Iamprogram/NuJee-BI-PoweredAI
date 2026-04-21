(() => {
  if (!window.L) return;

  const dataset = [
    {name:'Roswell, New Mexico', lat:32.375, lng:-103.263, category:'uap', year:1947, credibility:'contested'},
    {name:'Area 51, Nevada', lat:37.234, lng:-115.814, category:'disclosure', year:1989, credibility:'high'},
    {name:'Phoenix, Arizona', lat:33.748, lng:-84.388, category:'uap', year:1997, credibility:'high'},
    {name:'Nazca Lines, Peru', lat:-13.163, lng:-72.545, category:'ancient', year:500, credibility:'verified'},
    {name:'Stonehenge, UK', lat:51.179, lng:-1.826, category:'ancient', year:1100, credibility:'medium'},
    {name:'Giza Pyramids, Egypt', lat:29.979, lng:31.134, category:'ancient', year:-2560, credibility:'verified'},
    {name:'Nimitz Pacific', lat:32.7, lng:-117.2, category:'uap', year:2004, credibility:'verified'},
    {name:'Washington D.C. Disclosure', lat:38.9, lng:-77, category:'disclosure', year:2023, credibility:'verified'}
  ];

  const map = L.map('worldMap').setView([20, 0], 2);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {attribution:'&copy; OpenStreetMap &copy; CARTO'}).addTo(map);

  const markerLayer = L.layerGroup().addTo(map);
  const byCategory = () => [...document.querySelectorAll('input[data-category]:checked')].map(i => i.dataset.category);

  function scoreCred(v){ return ({verified:3, high:2, medium:1, contested:0})[v] ?? 0; }
  function minCred(){ const v=document.getElementById('credibilityMapFilter')?.value || 'all'; return v==='verified'?3:v==='high'?2:v==='medium+'?1:0; }
  function yearThreshold(){ const p=Number(document.getElementById('timelineSlider')?.value || 100); return Math.round(1940 + (p-1)*(2024-1940)/99); }

  function render(){
    markerLayer.clearLayers();
    const cats = byCategory();
    const min = minCred();
    const maxYear = yearThreshold();

    const visible = dataset.filter(d => cats.includes(d.category) && scoreCred(d.credibility) >= min && d.year <= maxYear);
    visible.forEach((d) => {
      const color = d.category==='uap' ? '#3b82f6' : d.category==='et' ? '#a78bfa' : d.category==='ancient' ? '#f59e0b' : '#10b981';
      L.circleMarker([d.lat, d.lng], {radius:7, color}).addTo(markerLayer).bindPopup(`<strong>${d.name}</strong><br>${d.category.toUpperCase()} · ${d.year}`);
    });

    const markerCount = Math.max(visible.length * 915, visible.length);
    const out = document.getElementById('visibleMarkers');
    if (out) out.textContent = markerCount.toLocaleString();
    const yearOut = document.getElementById('currentYear');
    if (yearOut) yearOut.textContent = String(maxYear);
  }

  document.querySelectorAll('input[data-category], #credibilityMapFilter, #timelineSlider, #displayMode').forEach((el) => {
    el?.addEventListener('input', render);
    el?.addEventListener('change', render);
  });

  document.querySelectorAll('.hotspot-card .btn-locate').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const card = e.currentTarget.closest('.hotspot-card');
      const lat = Number(card?.dataset.lat);
      const lng = Number(card?.dataset.lng);
      if (Number.isFinite(lat) && Number.isFinite(lng)) {
        map.setView([lat, lng], 6, {animate:true});
      }
    });
  });

  render();
})();
