/* Biblioteca Personal: theme toggle and client-side search for the static site. */
(function () {
  'use strict';

  const THEME_KEY = 'biblioteca-theme';
  const root = document.documentElement;

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    try { localStorage.setItem(THEME_KEY, theme); } catch (error) { /* Storage can be disabled. */ }
  }

  let savedTheme = null;
  try { savedTheme = localStorage.getItem(THEME_KEY); } catch (error) { /* Storage can be disabled. */ }
  if (savedTheme === 'light' || savedTheme === 'dark') {
    applyTheme(savedTheme);
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    applyTheme('dark');
  } else {
    applyTheme('light');
  }

  const themeButton = document.getElementById('theme-toggle');
  if (themeButton) {
    themeButton.addEventListener('click', () => {
      applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
  }

  const input = document.getElementById('search-input');
  const suggestions = document.getElementById('search-suggestions');
  const results = document.getElementById('search-results');
  const booksPromise = fetch(new URL('search-index.json', document.baseURI))
    .then((response) => {
      if (!response.ok) throw new Error(`Search index request failed: ${response.status}`);
      return response.json();
    });

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function normalizeSearchText(value) {
    return String(value == null ? '' : value)
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLocaleLowerCase();
  }

  function matchesBook(book, query) {
    const searchableText = [
      book.title,
      book.author,
      book.publisher,
      book.isbn,
      book.synopsis,
      book.category,
    ].join(' ');
    return normalizeSearchText(searchableText).includes(query);
  }

  function hideSuggestions() {
    if (!suggestions) return;
    suggestions.hidden = true;
    suggestions.innerHTML = '';
  }

  function renderSuggestions(books, query) {
    if (!suggestions) return;
    const normalized = normalizeSearchText(query);
    const matches = books.filter((book) => matchesBook(book, normalized)).slice(0, 8);

    suggestions.innerHTML = matches.map((book) =>
      `<li class="search-suggestion is-suggestion" role="option">` +
        `<a href="${escapeHtml(book.url)}">` +
          `<span class="sugg-icon" aria-hidden="true">📕</span>` +
          `<span class="sugg-main"><span class="sugg-title">${escapeHtml(book.title)}</span>` +
          `<span class="sugg-sub">por ${escapeHtml(book.author)}</span></span>` +
        `</a>` +
      `</li>`
    ).join('');
    suggestions.hidden = matches.length === 0;
  }

  function renderBookCard(book) {
    const cover = book.cover_url
      ? `<img src="${escapeHtml(book.cover_url)}" alt="Portada de ${escapeHtml(book.title)}" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"><span class="cover-fallback" style="display:none;">${escapeHtml(book.title.charAt(0).toLocaleUpperCase())}</span>`
      : `<span class="cover-fallback">${escapeHtml(book.title.charAt(0).toLocaleUpperCase())}</span>`;
    return (
      `<a class="book-card" href="${escapeHtml(book.url)}">` +
        `<div class="book-cover">${cover}</div>` +
        `<div class="book-meta"><h3 class="book-title">${escapeHtml(book.title)}</h3>` +
        `<p class="book-author">${escapeHtml(book.author)}</p>` +
        `<div class="book-tags"><span class="status status-${escapeHtml(book.status)}">` +
        `${escapeHtml(book.status_icon)} ${escapeHtml(book.status_label)}</span>` +
        `<span class="year">${escapeHtml(book.category_icon)} ${escapeHtml(book.category)}` +
        `${book.year ? ` · ${escapeHtml(book.year)}` : ''}</span></div></div></a>`
    );
  }

  if (input && suggestions) {
    let activeSuggestion = -1;

    input.addEventListener('input', async () => {
      const query = input.value.trim();
      activeSuggestion = -1;
      if (query.length < 2) {
        hideSuggestions();
        return;
      }
      try {
        renderSuggestions(await booksPromise, query);
      } catch (error) {
        console.error('No se pudo cargar el índice de búsqueda.', error);
        hideSuggestions();
      }
    });
    input.addEventListener('blur', () => setTimeout(hideSuggestions, 120));
    input.addEventListener('keydown', (event) => {
      const options = suggestions.querySelectorAll('a');
      if (suggestions.hidden || options.length === 0) return;
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault();
        activeSuggestion = event.key === 'ArrowDown'
          ? (activeSuggestion + 1) % options.length
          : (activeSuggestion - 1 + options.length) % options.length;
        options[activeSuggestion].focus();
      } else if (event.key === 'Escape') {
        hideSuggestions();
      } else if (event.key === 'Enter' && activeSuggestion >= 0) {
        event.preventDefault();
        window.location.href = new URL(options[activeSuggestion].href).href;
      }
    });
  }

  if (results) {
    const query = new URLSearchParams(window.location.search).get('q') || '';
    const heading = document.getElementById('search-heading');
    const count = document.getElementById('search-count');
    if (input) input.value = query;
    if (heading && query) heading.textContent = `Resultados para “${query}”`;
    booksPromise.then((books) => {
      const normalized = normalizeSearchText(query.trim());
      const matches = normalized
        ? books.filter((book) => matchesBook(book, normalized))
        : [];
      results.innerHTML = matches.length
        ? matches.map(renderBookCard).join('')
        : '<div class="empty"><p>No encontramos libros. Prueba con otro título o autor.</p></div>';
      if (count) count.textContent = normalized
        ? `${matches.length} resultado${matches.length === 1 ? '' : 's'}`
        : 'Escribe un título o autor en el buscador.';
    }).catch((error) => {
      console.error('No se pudo cargar el índice de búsqueda.', error);
      results.innerHTML = '<div class="empty"><p>No se pudo cargar la biblioteca.</p></div>';
    });
  }

  const galleryItems = Array.from(document.querySelectorAll('.book-gallery-item'));
  const lightbox = document.getElementById('book-lightbox');
  if (galleryItems.length && lightbox) {
    const lightboxImage = document.getElementById('book-lightbox-image');
    const lightboxCount = document.getElementById('book-lightbox-count');
    const closeButton = document.getElementById('book-lightbox-close');
    const previousButton = document.getElementById('book-lightbox-previous');
    const nextButton = document.getElementById('book-lightbox-next');
    const stage = document.getElementById('book-lightbox-stage');
    const zoomOutButton = document.getElementById('book-lightbox-zoom-out');
    const zoomResetButton = document.getElementById('book-lightbox-zoom-reset');
    const zoomInButton = document.getElementById('book-lightbox-zoom-in');
    const minZoom = 1;
    const maxZoom = 4;
    let zoom = minZoom;
    let offsetX = 0;
    let offsetY = 0;
    let activeImage = 0;
    const pointers = new Map();
    let gesture = null;

    function renderZoom() {
      lightboxImage.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${zoom})`;
      lightboxImage.style.cursor = zoom > minZoom ? 'grab' : 'zoom-in';
      zoomResetButton.textContent = `${Math.round(zoom * 100)}%`;
      zoomOutButton.disabled = zoom <= minZoom;
      zoomInButton.disabled = zoom >= maxZoom;
    }

    function constrainOffset() {
      const maxX = stage.clientWidth * (zoom - minZoom) / 2;
      const maxY = stage.clientHeight * (zoom - minZoom) / 2;
      offsetX = Math.max(-maxX, Math.min(maxX, offsetX));
      offsetY = Math.max(-maxY, Math.min(maxY, offsetY));
    }

    function setZoom(value, nextOffsetX = offsetX, nextOffsetY = offsetY) {
      zoom = Math.max(minZoom, Math.min(maxZoom, value));
      offsetX = nextOffsetX;
      offsetY = nextOffsetY;
      constrainOffset();
      renderZoom();
    }

    function showImage(index) {
      activeImage = (index + galleryItems.length) % galleryItems.length;
      const item = galleryItems[activeImage];
      lightboxImage.src = item.dataset.image;
      lightboxImage.alt = item.dataset.alt || '';
      lightboxCount.textContent = `${activeImage + 1} de ${galleryItems.length}`;
      pointers.clear();
      gesture = null;
      setZoom(minZoom, 0, 0);
    }

    function openLightbox(index) {
      showImage(index);
      if (galleryItems.length < 2) {
        previousButton.hidden = true;
        nextButton.hidden = true;
      }
      lightbox.showModal();
    }

    galleryItems.forEach((item, index) => {
      item.addEventListener('click', () => openLightbox(index));
    });
    closeButton.addEventListener('click', () => lightbox.close());
    previousButton.addEventListener('click', () => showImage(activeImage - 1));
    nextButton.addEventListener('click', () => showImage(activeImage + 1));
    zoomOutButton.addEventListener('click', () => setZoom(zoom / 1.25));
    zoomInButton.addEventListener('click', () => setZoom(zoom * 1.25));
    zoomResetButton.addEventListener('click', () => setZoom(minZoom, 0, 0));

    lightboxImage.addEventListener('wheel', (event) => {
      event.preventDefault();
      setZoom(zoom * (event.deltaY < 0 ? 1.15 : 1 / 1.15));
    }, { passive: false });
    lightboxImage.addEventListener('dblclick', (event) => {
      event.preventDefault();
      setZoom(zoom === minZoom ? 2 : minZoom, 0, 0);
    });

    lightbox.addEventListener('click', (event) => {
      if (event.target === lightbox) lightbox.close();
    });
    lightbox.addEventListener('keydown', (event) => {
      if (galleryItems.length > 1 && event.key === 'ArrowLeft') {
        event.preventDefault();
        showImage(activeImage - 1);
      } else if (galleryItems.length > 1 && event.key === 'ArrowRight') {
        event.preventDefault();
        showImage(activeImage + 1);
      } else if (event.key === '+' || event.key === '=') {
        event.preventDefault();
        setZoom(zoom * 1.25);
      } else if (event.key === '-') {
        event.preventDefault();
        setZoom(zoom / 1.25);
      } else if (event.key === '0') {
        event.preventDefault();
        setZoom(minZoom, 0, 0);
      }
    });

    stage.addEventListener('pointerdown', (event) => {
      if (event.target.closest('button')) return;
      pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
      stage.setPointerCapture(event.pointerId);
      if (pointers.size === 2) {
        const [first, second] = Array.from(pointers.values());
        gesture = {
          mode: 'pinch',
          distance: Math.hypot(second.x - first.x, second.y - first.y),
          centerX: (first.x + second.x) / 2,
          centerY: (first.y + second.y) / 2,
          zoom,
          offsetX,
          offsetY,
        };
      } else if (pointers.size === 1) {
        gesture = {
          mode: zoom > minZoom ? 'pan' : 'swipe',
          x: event.clientX,
          y: event.clientY,
          offsetX,
          offsetY,
        };
      }
    });
    stage.addEventListener('pointermove', (event) => {
      if (!pointers.has(event.pointerId)) return;
      pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
      if (pointers.size >= 2 && gesture && gesture.mode === 'pinch') {
        const [first, second] = Array.from(pointers.values());
        const distance = Math.hypot(second.x - first.x, second.y - first.y);
        const centerX = (first.x + second.x) / 2;
        const centerY = (first.y + second.y) / 2;
        const scale = gesture.distance ? distance / gesture.distance : 1;
        setZoom(
          gesture.zoom * scale,
          gesture.offsetX + centerX - gesture.centerX,
          gesture.offsetY + centerY - gesture.centerY,
        );
      } else if (pointers.size === 1 && gesture && gesture.mode === 'pan') {
        setZoom(
          zoom,
          gesture.offsetX + event.clientX - gesture.x,
          gesture.offsetY + event.clientY - gesture.y,
        );
      }
    });

    function finishPointer(event, cancelled = false) {
      const point = pointers.get(event.pointerId);
      if (point && gesture && gesture.mode === 'swipe' && !cancelled) {
        const deltaX = point.x - gesture.x;
        const deltaY = point.y - gesture.y;
        if (galleryItems.length > 1 && Math.abs(deltaX) > 50 && Math.abs(deltaX) > Math.abs(deltaY) * 1.2) {
          showImage(activeImage + (deltaX < 0 ? 1 : -1));
          return;
        }
      }
      pointers.delete(event.pointerId);
      if (pointers.size === 1) {
        const remaining = Array.from(pointers.values())[0];
        gesture = {
          mode: zoom > minZoom ? 'pan' : 'swipe',
          x: remaining.x,
          y: remaining.y,
          offsetX,
          offsetY,
        };
      } else if (pointers.size === 0) {
        gesture = null;
      }
    }

    stage.addEventListener('pointerup', (event) => finishPointer(event));
    stage.addEventListener('pointercancel', (event) => finishPointer(event, true));
    stage.addEventListener('lostpointercapture', (event) => finishPointer(event, true));
    lightbox.addEventListener('close', () => {
      pointers.clear();
      gesture = null;
      setZoom(minZoom, 0, 0);
    });
    renderZoom();
  }
})();
