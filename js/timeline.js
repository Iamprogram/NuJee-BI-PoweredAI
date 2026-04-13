// ===== Timeline Page JavaScript =====

document.addEventListener('DOMContentLoaded', function() {
    const eraButtons = document.querySelectorAll('.era-btn');
    const timelineEras = document.querySelectorAll('.timeline-era');
    const timelineItems = document.querySelectorAll('.timeline-item');
    const categoryFilter = document.getElementById('timelineCategoryFilter');
    const significanceFilter = document.getElementById('timelineSignificance');
    const zoomInBtn = document.getElementById('zoomIn');
    const zoomOutBtn = document.getElementById('zoomOut');
    
    let currentZoom = 1;
    
    // Era filtering
    eraButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons
            eraButtons.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            const selectedEra = this.dataset.era;
            
            if (selectedEra === 'all') {
                // Show all eras
                timelineEras.forEach(era => {
                    era.style.display = 'block';
                });
            } else {
                // Show only selected era
                timelineEras.forEach(era => {
                    if (era.dataset.era === selectedEra) {
                        era.style.display = 'block';
                    } else {
                        era.style.display = 'none';
                    }
                });
            }
            
            // Re-apply other filters
            applyFilters();
        });
    });
    
    // Category and significance filtering
    function applyFilters() {
        const selectedCategory = categoryFilter?.value || 'all';
        const selectedSignificance = significanceFilter?.value || 'all';
        
        timelineItems.forEach(item => {
            const itemCategory = item.dataset.category;
            const itemSignificance = item.dataset.significance;
            const parentEra = item.closest('.timeline-era');
            
            // Check if parent era is visible
            const eraVisible = parentEra && parentEra.style.display !== 'none';
            
            // Category filter
            const matchesCategory = selectedCategory === 'all' || itemCategory === selectedCategory;
            
            // Significance filter
            const matchesSignificance = selectedSignificance === 'all' || itemSignificance === selectedSignificance;
            
            // Show/hide based on filters
            if (eraVisible && matchesCategory && matchesSignificance) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
        
        // Hide eras with no visible items
        timelineEras.forEach(era => {
            if (era.style.display !== 'none') {
                const visibleItems = era.querySelectorAll('.timeline-item[style*="display: block"], .timeline-item:not([style])');
                if (visibleItems.length === 0) {
                    era.style.display = 'none';
                }
            }
        });
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', applyFilters);
    }
    
    if (significanceFilter) {
        significanceFilter.addEventListener('change', applyFilters);
    }
    
    // Zoom functionality
    function updateZoom() {
        const timelineWrapper = document.querySelector('.timeline-wrapper');
        if (timelineWrapper) {
            timelineWrapper.style.transform = `scale(${currentZoom})`;
            timelineWrapper.style.transformOrigin = 'top left';
        }
    }
    
    if (zoomInBtn) {
        zoomInBtn.addEventListener('click', function() {
            if (currentZoom < 1.5) {
                currentZoom += 0.1;
                updateZoom();
                window.UnknownBeyond?.showToast('Zoomed in', 'info');
            }
        });
    }
    
    if (zoomOutBtn) {
        zoomOutBtn.addEventListener('click', function() {
            if (currentZoom > 0.6) {
                currentZoom -= 0.1;
                updateZoom();
                window.UnknownBeyond?.showToast('Zoomed out', 'info');
            }
        });
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Zoom with + and - keys
        if (e.key === '+' || e.key === '=') {
            e.preventDefault();
            zoomInBtn?.click();
        } else if (e.key === '-' || e.key === '_') {
            e.preventDefault();
            zoomOutBtn?.click();
        }
        
        // Era navigation with number keys
        if (e.key >= '1' && e.key <= '7') {
            e.preventDefault();
            const index = parseInt(e.key) - 1;
            if (eraButtons[index]) {
                eraButtons[index].click();
            }
        }
    });
    
    // Smooth scrolling to timeline items when era button is clicked
    eraButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const era = this.dataset.era;
            if (era !== 'all') {
                const eraElement = document.querySelector(`.timeline-era[data-era="${era}"]`);
                if (eraElement) {
                    setTimeout(() => {
                        eraElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 100);
                }
            }
        });
    });
    
    // Highlight timeline items on scroll
    const timelineObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('highlighted');
                setTimeout(() => {
                    entry.target.classList.remove('highlighted');
                }, 2000);
            }
        });
    }, {
        threshold: 0.5
    });
    
    timelineItems.forEach(item => {
        timelineObserver.observe(item);
    });
    
    // Add highlight animation
    const highlightStyle = document.createElement('style');
    highlightStyle.textContent = `
        .timeline-item.highlighted .timeline-content {
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
            border-color: var(--accent-primary);
            transition: all 0.3s ease;
        }
    `;
    document.head.appendChild(highlightStyle);
    
    // Initialize - show all by default
    applyFilters();
});
