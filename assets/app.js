(() => {
  const page = document.body.dataset.page;
  document.querySelectorAll('.nav-links a[data-page]').forEach((link) => {
    if (link.dataset.page === page) link.classList.add('active');
  });

  const yearNode = document.getElementById('year');
  if (yearNode) yearNode.textContent = String(new Date().getFullYear());
})();
