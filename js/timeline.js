(() => {
  const era = document.getElementById('era-filter');
  const items = [...document.querySelectorAll('.timeline-item')];
  era?.addEventListener('change', () => {
    items.forEach((item) => {
      item.style.display = era.value === 'all' || item.dataset.era === era.value ? '' : 'none';
    });
  });
})();
