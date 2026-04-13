// ===== Library Page JavaScript =====

document.addEventListener('DOMContentLoaded', function() {
    // Get all filter elements
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const evidenceFilter = document.getElementById('evidenceFilter');
    const credibilityFilter = document.getElementById('credibilityFilter');
    const timeFilter = document.getElementById('timeFilter');
    const sortBy = document.getElementById('sortBy');
    const clearFiltersBtn = document.getElementById('clearFilters');
    const contentGrid = document.getElementById('contentGrid');
    const resultCount = document.getElementById('resultCount');
    
    // Get all content cards
    let allCards = Array.from(document.querySelectorAll('.content-card'));
    
    // Filter function
    function filterContent() {
        const searchTerm = searchInput?.value.toLowerCase() || '';
        const selectedCategory = categoryFilter?.value || 'all';
        const selectedEvidence = evidenceFilter?.value || 'all';
        const selectedCredibility = credibilityFilter?.value || 'all';
        const selectedTime = timeFilter?.value || 'all';
        
        let visibleCount = 0;
        
        allCards.forEach(card => {
            const cardText = card.textContent.toLowerCase();
            const cardCategory = card.dataset.category;
            const cardEvidence = card.dataset.evidence || '';
            const cardCredibility = card.dataset.credibility;
            const cardDate = card.dataset.date || '';
            
            // Search filter
            const matchesSearch = searchTerm === '' || cardText.includes(searchTerm);
            
            // Category filter
            const matchesCategory = selectedCategory === 'all' || cardCategory === selectedCategory;
            
            // Evidence filter
            const matchesEvidence = selectedEvidence === 'all' || cardEvidence.includes(selectedEvidence);
            
            // Credibility filter
            const matchesCredibility = selectedCredibility === 'all' || cardCredibility === selectedCredibility;
            
            // Time filter
            let matchesTime = true;
            if (selectedTime !== 'all' && cardDate) {
                const currentYear = new Date().getFullYear();
                const cardYear = cardDate === 'ancient' ? 0 : parseInt(cardDate.split('-')[0]);
                
                switch(selectedTime) {
                    case 'recent':
                        matchesTime = (currentYear - cardYear) <= 0.1;
                        break;
                    case 'year':
                        matchesTime = (currentYear - cardYear) <= 1;
                        break;
                    case '5years':
                        matchesTime = (currentYear - cardYear) <= 5;
                        break;
                    case 'modern':
                        matchesTime = cardYear >= 2000;
                        break;
                    case 'cold-war':
                        matchesTime = cardYear >= 1945 && cardYear <= 1991;
                        break;
                    case 'ancient':
                        matchesTime = cardDate === 'ancient';
                        break;
                }
            }
            
            // Show/hide card based on all filters
            if (matchesSearch && matchesCategory && matchesEvidence && matchesCredibility && matchesTime) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Update result count
        if (resultCount) {
            resultCount.textContent = `Showing ${visibleCount} result${visibleCount !== 1 ? 's' : ''}`;
        }
        
        // Show message if no results
        const noResults = document.getElementById('noResults');
        if (visibleCount === 0) {
            if (!noResults) {
                const message = document.createElement('div');
                message.id = 'noResults';
                message.className = 'no-results';
                message.innerHTML = `
                    <i class="fas fa-search"></i>
                    <h3>No Results Found</h3>
                    <p>Try adjusting your filters or search terms</p>
                `;
                contentGrid?.appendChild(message);
                
                // Add CSS for no results
                const style = document.createElement('style');
                style.textContent = `
                    .no-results {
                        grid-column: 1 / -1;
                        text-align: center;
                        padding: 4rem 2rem;
                        color: var(--text-secondary);
                    }
                    .no-results i {
                        font-size: 4rem;
                        color: var(--text-muted);
                        margin-bottom: 1rem;
                    }
                    .no-results h3 {
                        color: var(--text-primary);
                        margin-bottom: 0.5rem;
                    }
                `;
                document.head.appendChild(style);
            }
        } else {
            noResults?.remove();
        }
    }
    
    // Sort function
    function sortContent() {
        const sortValue = sortBy?.value || 'date-desc';
        
        allCards.sort((a, b) => {
            switch(sortValue) {
                case 'date-desc':
                    return (b.dataset.date || '0') .localeCompare(a.dataset.date || '0');
                case 'date-asc':
                    return (a.dataset.date || '0').localeCompare(b.dataset.date || '0');
                case 'credibility':
                    const credOrder = { verified: 5, high: 4, medium: 3, contested: 2, speculative: 1 };
                    return (credOrder[b.dataset.credibility] || 0) - (credOrder[a.dataset.credibility] || 0);
                case 'relevance':
                default:
                    return 0;
            }
        });
        
        // Re-append sorted cards
        allCards.forEach(card => contentGrid?.appendChild(card));
        filterContent(); // Re-apply filters after sorting
    }
    
    // Clear filters
    function clearFilters() {
        if (searchInput) searchInput.value = '';
        if (categoryFilter) categoryFilter.value = 'all';
        if (evidenceFilter) evidenceFilter.value = 'all';
        if (credibilityFilter) credibilityFilter.value = 'all';
        if (timeFilter) timeFilter.value = 'all';
        filterContent();
        window.UnknownBeyond?.showToast('Filters cleared', 'info');
    }
    
    // Event listeners with debouncing for search
    if (searchInput) {
        searchInput.addEventListener('input', window.UnknownBeyond?.debounce(filterContent, 300) || filterContent);
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterContent);
    }
    
    if (evidenceFilter) {
        evidenceFilter.addEventListener('change', filterContent);
    }
    
    if (credibilityFilter) {
        credibilityFilter.addEventListener('change', filterContent);
    }
    
    if (timeFilter) {
        timeFilter.addEventListener('change', filterContent);
    }
    
    if (sortBy) {
        sortBy.addEventListener('change', sortContent);
    }
    
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', clearFilters);
    }
    
    // Check for URL parameters to pre-filter
    const urlParams = new URLSearchParams(window.location.search);
    const catParam = urlParams.get('cat');
    if (catParam && categoryFilter) {
        categoryFilter.value = catParam;
        filterContent();
    }
    
    // Initialize with current filters
    filterContent();
});
