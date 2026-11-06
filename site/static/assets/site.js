/* YuHan Articles · Progressive enhancements only.
 * Navigation and reading work without JavaScript.
 */
(() => {
  "use strict";

  const root = document.documentElement;
  const toggle = document.getElementById("theme-toggle");
  const storageKey = "yuhan-theme";

  const readPreference = () => {
    try { return localStorage.getItem(storageKey); } catch (_) { return null; }
  };
  const savePreference = (value) => {
    try { localStorage.setItem(storageKey, value); } catch (_) { /* private mode */ }
  };
  const updateThemeLabel = () => {
    if (!toggle) return;
    const theme = root.dataset.theme;
    const mode = theme === "dark" ? "深色" : theme === "light" ? "浅色" : "跟随系统";
    toggle.setAttribute("aria-label", "当前：" + mode + "。切换明暗主题");
    toggle.title = "当前：" + mode + "。切换明暗主题";
  };

  if (toggle) {
    updateThemeLabel();
    toggle.addEventListener("click", () => {
      const stored = readPreference();
      const active = root.dataset.theme === "dark" ? "dark" :
        root.dataset.theme === "light" ? "light" :
        (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      const next = (stored === "dark" || stored === "light") ? (stored === "dark" ? "light" : "dark") : (active === "dark" ? "light" : "dark");
      root.dataset.theme = next;
      savePreference(next);
      updateThemeLabel();
    });
  }

  const search = document.getElementById("archive-search");
  const cards = Array.from(document.querySelectorAll(".archive-item[data-search]"));
  const filters = Array.from(document.querySelectorAll("[data-filter]"));
  const count = document.getElementById("results-count");
  const empty = document.getElementById("no-results");
  let activeCategory = "all";

  const normalize = (text) => String(text || "").trim().toLocaleLowerCase("zh-CN").normalize("NFKC");
  const refresh = () => {
    const needle = normalize(search && search.value);
    let visible = 0;
    for (const card of cards) {
      const matchesCategory = activeCategory === "all" || card.dataset.category === activeCategory;
      const matchesTerm = !needle || normalize(card.dataset.search).includes(needle);
      const show = matchesCategory && matchesTerm;
      card.hidden = !show;
      if (show) visible++;
    }
    if (empty) empty.hidden = visible !== 0;
    if (count) count.textContent = "共 " + visible + " 篇文章";
  };

  if (search) search.addEventListener("input", refresh);
  for (const filter of filters) {
    filter.addEventListener("click", () => {
      activeCategory = filter.dataset.filter || "all";
      for (const button of filters) {
        const selected = button === filter;
        button.classList.toggle("is-active", selected);
        button.setAttribute("aria-pressed", String(selected));
      }
      refresh();
    });
  }

  const progress = document.getElementById("reading-progress");
  const body = document.getElementById("article-body");
  if (progress && body) {
    let scheduled = false;
    const recalc = () => {
      scheduled = false;
      const top = body.getBoundingClientRect().top + window.scrollY;
      const total = Math.max(1, body.offsetHeight - window.innerHeight * .35);
      const percent = Math.max(0, Math.min(100, (window.scrollY - top) / total * 100));
      progress.style.width = percent.toFixed(1) + "%";
    };
    const request = () => {
      if (!scheduled) {
        scheduled = true;
        window.requestAnimationFrame(recalc);
      }
    };
    window.addEventListener("scroll", request, { passive: true });
    window.addEventListener("resize", request, { passive: true });
    recalc();
  }
})();
