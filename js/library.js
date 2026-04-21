(() => {
  const cards = [...document.querySelectorAll('.case-card')];
  const search = document.getElementById('search');
  const category = document.getElementById('category');
  const credibility = document.getElementById('credibility');

  function apply() {
    const q = search.value.toLowerCase().trim();
    cards.forEach((card) => {
      const okQ = card.dataset.search.includes(q);
      const okC = category.value === 'all' || card.dataset.category === category.value;
      const okCr = credibility.value === 'all' || card.dataset.credibility === credibility.value;
      card.style.display = okQ && okC && okCr ? '' : 'none';
    });
  }

  [search, category, credibility].forEach((el) => el?.addEventListener('input', apply));
})();
