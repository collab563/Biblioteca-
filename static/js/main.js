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
})();
