(() => {
  const current = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-menu a[href]').forEach((a) => {
    const href = a.getAttribute('href');
    if (href === current) a.classList.add('active');
  });

  const toggle = document.querySelector('.mobile-menu-toggle');
  const menu = document.querySelector('.nav-menu');
  toggle?.addEventListener('click', () => menu?.classList.toggle('open'));

  const starfield = document.getElementById('starfield');
  if (starfield) {
    for (let i = 0; i < 80; i++) {
      const s = document.createElement('span');
      s.style.position = 'absolute';
      s.style.left = `${Math.random() * 100}%`;
      s.style.top = `${Math.random() * 100}%`;
      s.style.width = s.style.height = `${Math.random() * 2 + 1}px`;
      s.style.background = 'rgba(255,255,255,0.75)';
      s.style.borderRadius = '50%';
      starfield.appendChild(s);
    }
  }

  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
