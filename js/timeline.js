(() => {
  const eraButtons = [...document.querySelectorAll('.era-btn')];
  const eraSections = [...document.querySelectorAll('.timeline-era')];
  const items = [...document.querySelectorAll('.timeline-item')];
  const cat = document.getElementById('timelineCategoryFilter');
  const sig = document.getElementById('timelineSignificance');
  const wrapper = document.querySelector('.timeline-wrapper');
  let zoom = 1;

  let currentEra = 'all';

  function apply() {
    items.forEach((item) => {
      const eraOk = currentEra === 'all' || item.closest('.timeline-era')?.dataset.era === currentEra;
      const catOk = !cat || cat.value === 'all' || item.dataset.category === cat.value;
      const sigOk = !sig || sig.value === 'all' || item.dataset.significance === sig.value;
      item.style.display = eraOk && catOk && sigOk ? '' : 'none';
    });

    eraSections.forEach((section) => {
      const visible = section.querySelector('.timeline-item:not([style*="display: none"])');
      section.style.display = visible ? '' : 'none';
    });
  }

  eraButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      eraButtons.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      currentEra = btn.dataset.era;
      apply();
    });
  });

  cat?.addEventListener('change', apply);
  sig?.addEventListener('change', apply);

  document.getElementById('zoomIn')?.addEventListener('click', () => {
    zoom = Math.min(1.6, zoom + 0.1);
    wrapper.style.transform = `scale(${zoom})`;
    wrapper.style.transformOrigin = 'top center';
  });

  document.getElementById('zoomOut')?.addEventListener('click', () => {
    zoom = Math.max(0.8, zoom - 0.1);
    wrapper.style.transform = `scale(${zoom})`;
    wrapper.style.transformOrigin = 'top center';
  });

  window.addEventListener('keydown', (e) => {
    if (e.key.toLowerCase() === 'f') document.getElementById('timelineCategoryFilter')?.focus();
  });

  apply();
})();
