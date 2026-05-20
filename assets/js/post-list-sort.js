(function () {
  const STORAGE_PREFIX = "postSort:";

  function sortList(ul, key, order) {
    const items = Array.from(ul.querySelectorAll(":scope > li"));
    const mult = order === "desc" ? -1 : 1;
    const attr = key === "semester" ? "semester" : "date";

    items.sort((a, b) => {
      const av = Number(a.dataset[attr] || 0);
      const bv = Number(b.dataset[attr] || 0);
      return (av - bv) * mult;
    });

    items.forEach((li) => ul.appendChild(li));
  }

  function storageKey(container) {
    return STORAGE_PREFIX + (container.dataset.sortStorageKey || window.location.pathname);
  }

  function updateButtons(controls, key, order) {
    controls.querySelectorAll("button[data-sort-key]").forEach((btn) => {
      const active =
        btn.dataset.sortKey === key && btn.dataset.sortOrder === order;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  function initContainer(container) {
    const ul = container.querySelector(".post-list");
    const controls = container.querySelector(".post-list-sort-controls");
    if (!ul || !controls) return;

    const defaultKey = container.dataset.sortDefaultKey || "date";
    const defaultOrder = container.dataset.sortDefault || "asc";
    let activeKey = defaultKey;
    let activeOrder = defaultOrder;

    const saved = localStorage.getItem(storageKey(container));
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        activeKey = parsed.key || activeKey;
        activeOrder = parsed.order || activeOrder;
      } catch (_) {
        /* ignore invalid storage */
      }
    }

    sortList(ul, activeKey, activeOrder);
    updateButtons(controls, activeKey, activeOrder);

    controls.addEventListener("click", (event) => {
      const btn = event.target.closest("button[data-sort-key]");
      if (!btn) return;

      const sortKey = btn.dataset.sortKey;
      const sortOrder = btn.dataset.sortOrder;
      sortList(ul, sortKey, sortOrder);
      updateButtons(controls, sortKey, sortOrder);
      localStorage.setItem(
        storageKey(container),
        JSON.stringify({ key: sortKey, order: sortOrder })
      );
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".post-list-sortable").forEach(initContainer);
  });
})();
