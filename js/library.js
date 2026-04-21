(() => {
  const cards = [...document.querySelectorAll('.content-card')];
  const q = document.getElementById('searchInput');
  const category = document.getElementById('categoryFilter');
  const evidence = document.getElementById('evidenceFilter');
  const cred = document.getElementById('credibilityFilter');
  const time = document.getElementById('timeFilter');
  const sortBy = document.getElementById('sortBy');
  const out = document.getElementById('resultCount');

  function dateNum(v){
    if (!v || v === 'ancient') return -999999;
    const [y,m='01'] = v.split('-');
    return Number(`${y}${m}`);
  }

  function matchesTime(v, f){
    const n = dateNum(v);
    if (f === 'all') return true;
    if (f === 'modern') return n >= 200001;
    if (f === 'cold-war') return n >= 194501 && n <= 199112;
    if (f === 'ancient') return v === 'ancient' || n < 180001;
    if (f === '5years') return n >= 201901;
    if (f === 'year') return n >= 202301;
    if (f === 'recent') return n >= 202403;
    return true;
  }

  function apply(){
    const term = (q?.value || '').toLowerCase().trim();
    const c = category?.value || 'all';
    const e = evidence?.value || 'all';
    const cr = cred?.value || 'all';
    const t = time?.value || 'all';

    let visible = cards.filter((card) => {
      const txt = card.textContent.toLowerCase();
      const okQ = !term || txt.includes(term);
      const okC = c === 'all' || card.dataset.category === c;
      const ev = (card.dataset.evidence || '').split(',');
      const okE = e === 'all' || ev.includes(e);
      const okCr = cr === 'all' || card.dataset.credibility === cr;
      const okT = matchesTime(card.dataset.date, t);
      return okQ && okC && okE && okCr && okT;
    });

    const s = sortBy?.value || 'date-desc';
    const credRank = {verified:3, high:2, medium:1, contested:0, speculative:-1};
    visible.sort((a,b)=>{
      if (s === 'date-asc') return dateNum(a.dataset.date)-dateNum(b.dataset.date);
      if (s === 'date-desc') return dateNum(b.dataset.date)-dateNum(a.dataset.date);
      if (s === 'credibility') return (credRank[b.dataset.credibility]??-1)-(credRank[a.dataset.credibility]??-1);
      return a.textContent.length - b.textContent.length;
    });

    cards.forEach(c=>c.style.display='none');
    visible.forEach(v=>{v.style.display=''; v.parentElement.appendChild(v);});
    if (out) out.textContent = `Showing ${visible.length} results`;
  }

  [q, category, evidence, cred, time, sortBy].forEach((el)=>el?.addEventListener('input', apply));
  [category, evidence, cred, time, sortBy].forEach((el)=>el?.addEventListener('change', apply));
  document.getElementById('clearFilters')?.addEventListener('click', ()=>{
    if (q) q.value='';
    [category, evidence, cred, time].forEach(sel=>{ if(sel) sel.value='all'; });
    if (sortBy) sortBy.value='date-desc';
    apply();
  });
  apply();
})();
