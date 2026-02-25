// ─── NEXUS STORE — main.js ──────────────────────────────────

// ─── AJAX Add to Cart (optional enhancement) ─────────────────
document.addEventListener('DOMContentLoaded', () => {

  // Auto-dismiss toasts after 4 seconds
  const toasts = document.querySelectorAll('.toast-msg');
  toasts.forEach((toast, i) => {
    setTimeout(() => dismissToast(toast), 4000 + i * 300);
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Quantity input safeguards
  document.querySelectorAll('input[type="number"][name="quantity"]').forEach(input => {
    input.addEventListener('change', () => {
      const min = parseInt(input.min) || 1;
      const max = parseInt(input.max) || 999;
      let val = parseInt(input.value) || min;
      if (val < min) val = min;
      if (val > max) val = max;
      input.value = val;
    });
  });

  // Product image lazy load / reveal on scroll
  const cards = document.querySelectorAll('.product-card');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    cards.forEach((card, i) => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      card.style.transition = `opacity 0.5s ease ${i * 0.05}s, transform 0.5s ease ${i * 0.05}s`;
      observer.observe(card);
    });
  }
});

// ─── Toast dismiss helper ────────────────────────────────────
function dismissToast(el) {
  if (!el || !el.parentNode) return;
  el.style.transition = 'all 0.35s ease';
  el.style.opacity = '0';
  el.style.transform = 'translateX(120%)';
  setTimeout(() => el.remove(), 350);
}

// ─── Show toast programmatically ────────────────────────────
function showToast(message, type = 'info') {
  const colors = {
    success: 'border-success-neon/40 text-success-neon',
    error:   'border-danger/40 text-danger',
    warning: 'border-yellow-400/40 text-yellow-400',
    info:    'border-cyan-neon/40 text-cyan-neon',
  };
  const container = document.getElementById('toast-container') || (() => {
    const el = document.createElement('div');
    el.id = 'toast-container';
    el.className = 'fixed top-20 right-4 z-50 flex flex-col gap-2';
    document.body.appendChild(el);
    return el;
  })();

  const toast = document.createElement('div');
  toast.className = `toast-msg glass-card px-5 py-3 flex items-center gap-3 min-w-64 shadow-lg ${colors[type] || colors.info}`;
  toast.innerHTML = `<span class="text-sm font-mono">${message}</span><button onclick="this.parentElement.remove()" class="ml-auto opacity-60 hover:opacity-100 text-lg">&times;</button>`;
  container.appendChild(toast);
  setTimeout(() => dismissToast(toast), 4000);
}
