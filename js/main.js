(() => {
  const page = document.body.dataset.page;
  document.querySelectorAll('[data-page-link]').forEach((a) => {
    if (a.dataset.pageLink === page) a.classList.add('active');
  });
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
