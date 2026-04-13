// ===== Map Page JavaScript =====

document.addEventListener('DOMContentLoaded', function() {
    // Initialize map
    const map = L.map('worldMap', {
        center: [20, 0],
        zoom: 2,
        minZoom: 2,
        maxZoom: 18,
        worldCopyJump: true
    });
    
    // Add dark theme tile layer
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);
    
    // Sample data points
    const sightings = [
        { lat: 32.375, lng: -103.263, title: 'Roswell, NM', category: 'uap', credibility: 'contested', date: '1947-07-08', description: 'Famous 1947 crash incident' },
        { lat: 37.234, lng: -115.814, title: 'Area 51, NV', category: 'disclosure', credibility: 'high', date: '1955-01-01', description: 'Classified Air Force facility' },
        { lat: 33.448, lng: -112.074, title: 'Phoenix, AZ', category: 'uap', credibility: 'verified', date: '1997-03-13', description: 'Phoenix Lights mass sighting' },
        { lat: 32.5, lng: -117.0, title: 'USS Nimitz Location', category: 'uap', credibility: 'verified', date: '2004-11-14', description: 'Tic Tac UAP encounter' },
        { lat: -13.163, lng: -72.545, title: 'Nazca Lines, Peru', category: 'ancient', credibility: 'high', date: 'ancient', description: '168 new geoglyphs discovered' },
        { lat: 51.179, lng: -1.826, title: 'Stonehenge, UK', category: 'ancient', credibility: 'high', date: 'ancient', description: 'Prehistoric monument' },
        { lat: 29.979, lng: 31.134, title: 'Giza Pyramids', category: 'ancient', credibility: 'verified', date: 'ancient', description: 'Ancient engineering marvel' },
        { lat: 52.228, lng: 1.315, title: 'Rendlesham Forest, UK', category: 'uap', credibility: 'high', date: '1980-12-26', description: 'RAF personnel encounters' },
        { lat: 35.5, lng: -79.0, title: 'USS Roosevelt Area', category: 'uap', credibility: 'verified', date: '2014-01-01', description: 'Multiple Navy encounters' },
        { lat: 38.9072, lng: -77.0369, title: 'Washington, DC', category: 'disclosure', credibility: 'verified', date: '2023-07-26', description: 'Congressional hearings' }
    ];
    
    // Category colors
    const categoryColors = {
        uap: '#3b82f6',
        et: '#8b5cf6',
        ancient: '#f59e0b',
        disclosure: '#06b6d4',
        space: '#10b981'
    };
    
    // Store markers
    const markers = [];
    
    // Create markers
    function createMarkers(filteredSightings = sightings) {
        // Clear existing markers
        markers.forEach(m => map.removeLayer(m));
        markers.length = 0;
        
        filteredSightings.forEach(sighting => {
            const color = categoryColors[sighting.category] || '#3b82f6';
            
            // Create custom icon
            const icon = L.divIcon({
                className: 'custom-marker',
                html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 3px solid #0a0e1a; box-shadow: 0 0 10px ${color};"></div>`,
                iconSize: [20, 20]
            });
            
            const marker = L.marker([sighting.lat, sighting.lng], { icon })
                .bindPopup(`
                    <div class="map-popup">
                        <h4>${sighting.title}</h4>
                        <div class="popup-category ${sighting.category}">${sighting.category.toUpperCase()}</div>
                        <div class="popup-details">
                            <div><strong>Date:</strong> ${sighting.date}</div>
                            <div><strong>Credibility:</strong> <span class="cred-${sighting.credibility}">${sighting.credibility}</span></div>
                            <div>${sighting.description}</div>
                        </div>
                        <a href="library.html" class="popup-link">View Details →</a>
                    </div>
                `)
                .addTo(map);
            
            markers.push(marker);
        });
        
        // Update visible count
        document.getElementById('visibleMarkers').textContent = filteredSightings.length.toLocaleString();
    }
    
    // Initial markers
    createMarkers();
    
    // Filter functionality
    const categoryCheckboxes = document.querySelectorAll('input[data-category]');
    const timelineSlider = document.getElementById('timelineSlider');
    const currentYearDisplay = document.getElementById('currentYear');
    const credibilityMapFilter = document.getElementById('credibilityMapFilter');
    
    function filterMarkers() {
        // Get selected categories
        const selectedCategories = Array.from(categoryCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.dataset.category);
        
        // Get time range
        const sliderValue = parseInt(timelineSlider?.value || 100);
        const currentYear = 2024;
        const startYear = 1940;
        const yearRange = currentYear - startYear;
        const maxYear = startYear + Math.floor((yearRange * sliderValue) / 100);
        
        if (currentYearDisplay) {
            currentYearDisplay.textContent = maxYear;
        }
        
        // Get credibility filter
        const credFilter = credibilityMapFilter?.value || 'all';
        
        // Filter sightings
        const filtered = sightings.filter(s => {
            // Category filter
            if (!selectedCategories.includes(s.category)) return false;
            
            // Time filter
            if (s.date !== 'ancient') {
                const sightingYear = parseInt(s.date.split('-')[0]);
                if (sightingYear > maxYear) return false;
            }
            
            // Credibility filter
            if (credFilter !== 'all') {
                if (credFilter === 'verified' && s.credibility !== 'verified') return false;
                if (credFilter === 'high' && !['verified', 'high'].includes(s.credibility)) return false;
                if (credFilter === 'medium+' && !['verified', 'high', 'medium'].includes(s.credibility)) return false;
            }
            
            return true;
        });
        
        createMarkers(filtered);
    }
    
    // Event listeners
    categoryCheckboxes.forEach(cb => {
        cb.addEventListener('change', filterMarkers);
    });
    
    if (timelineSlider) {
        timelineSlider.addEventListener('input', filterMarkers);
    }
    
    if (credibilityMapFilter) {
        credibilityMapFilter.addEventListener('change', filterMarkers);
    }
    
    // Hotspot card click handlers
    document.querySelectorAll('.btn-locate').forEach(btn => {
        btn.addEventListener('click', function() {
            const card = this.closest('.hotspot-card');
            const lat = parseFloat(card.dataset.lat);
            const lng = parseFloat(card.dataset.lng);
            
            if (!isNaN(lat) && !isNaN(lng)) {
                map.setView([lat, lng], 8);
                
                // Find and open marker popup
                markers.forEach(marker => {
                    const markerLat = marker.getLatLng().lat;
                    const markerLng = marker.getLatLng().lng;
                    if (Math.abs(markerLat - lat) < 0.5 && Math.abs(markerLng - lng) < 0.5) {
                        marker.openPopup();
                    }
                });
            }
        });
    });
    
    // Display mode (placeholder for future implementation)
    const displayMode = document.getElementById('displayMode');
    if (displayMode) {
        displayMode.addEventListener('change', function() {
            const mode = this.value;
            window.UnknownBeyond?.showToast(`Display mode: ${mode}`, 'info');
            // TODO: Implement heatmap and cluster views
        });
    }
});
