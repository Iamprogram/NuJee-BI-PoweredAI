(() => {
  const progress = document.getElementById('scrollProgress');
  const revealItems = Array.from(document.querySelectorAll('.reveal'));

  const updateProgress = () => {
    const scrollTop = window.scrollY;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = maxScroll > 0 ? (scrollTop / maxScroll) * 100 : 0;
    progress.style.width = `${Math.min(Math.max(ratio, 0), 100)}%`;
  };

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: '0px 0px -8% 0px',
    }
  );

  revealItems.forEach((item) => observer.observe(item));
  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();
})();
