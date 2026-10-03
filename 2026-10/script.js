(() => {
  'use strict';

  const slides = [...document.querySelectorAll('.slide')];
  const previous = document.querySelector('#previous');
  const next = document.querySelector('#next');
  const counter = document.querySelector('#slide-counter');
  const progress = document.querySelector('.progress-track');
  const fill = document.querySelector('.progress-fill');
  const deck = document.querySelector('.deck');
  let current = 0;
  let wheelTotal = 0;
  let wheelTimestamp = 0;
  let wheelLockedUntil = 0;
  let touchStart = null;

  function showSlide(index) {
    current = Math.max(0, Math.min(slides.length - 1, index));
    slides.forEach((slide, i) => { slide.hidden = i !== current; });
    previous.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    counter.textContent = `${current + 1} / ${slides.length}`;
    progress.setAttribute('aria-valuenow', String(current + 1));
    fill.style.width = `${((current + 1) / slides.length) * 100}%`;
  }

  previous.addEventListener('click', () => showSlide(current - 1));
  next.addEventListener('click', () => showSlide(current + 1));
  document.addEventListener('keydown', (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.target.closest('input, textarea, select, [contenteditable="true"]')) return;
    if (event.key === ' ' && event.target.closest('button, a')) return;
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft' || event.key === ' ') {
      event.preventDefault();
      if (!event.repeat) showSlide(current + (event.key === 'ArrowLeft' ? -1 : 1));
    }
  });

  deck.addEventListener('wheel', (event) => {
    if (event.ctrlKey) return; // Preserve browser pinch-to-zoom.
    event.preventDefault();
    const now = performance.now();
    const delta = Math.abs(event.deltaX) > Math.abs(event.deltaY) ? event.deltaX : event.deltaY;
    const pixels = delta * (event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? deck.clientHeight : 1);
    if (now < wheelLockedUntil) {
      wheelLockedUntil = now + 180; // Wait for trackpad momentum to settle.
      return;
    }
    if (now - wheelTimestamp > 180 || Math.sign(pixels) !== Math.sign(wheelTotal)) wheelTotal = 0;
    wheelTimestamp = now;
    wheelTotal += pixels;
    if (Math.abs(wheelTotal) >= 45) {
      showSlide(current + Math.sign(wheelTotal));
      wheelTotal = 0;
      wheelLockedUntil = now + 320;
    }
  }, { passive: false });

  deck.addEventListener('touchstart', (event) => {
    touchStart = event.touches.length === 1 ? { x: event.touches[0].clientX, y: event.touches[0].clientY } : null;
  }, { passive: true });
  deck.addEventListener('touchend', (event) => {
    if (!touchStart || !event.changedTouches.length) return;
    const dx = event.changedTouches[0].clientX - touchStart.x;
    const dy = event.changedTouches[0].clientY - touchStart.y;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.25) showSlide(current + (dx < 0 ? 1 : -1));
    touchStart = null;
  }, { passive: true });
  deck.addEventListener('touchcancel', () => { touchStart = null; }, { passive: true });
  showSlide(0);
})();
