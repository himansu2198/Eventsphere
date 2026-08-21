// ================================
// Toast Notifications
// ================================
function showToast(message, type = 'success') {
  let stack = document.querySelector('.toast-stack');
  if (!stack) {
    stack = document.createElement('div');
    stack.className = 'toast-stack';
    document.body.appendChild(stack);
  }

  const icons = { success: 'bi-check-circle-fill', error: 'bi-x-circle-fill', warning: 'bi-exclamation-triangle-fill' };
  const toast = document.createElement('div');
  toast.className = `app-toast toast-${type}`;
  toast.innerHTML = `<i class="bi ${icons[type] || icons.success}"></i><span>${message}</span>`;
  stack.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(30px)';
    toast.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
    setTimeout(() => toast.remove(), 200);
  }, 4000);
}

// Auto-convert Django messages (.alert elements) into toasts on page load
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.alert').forEach(alertEl => {
    const text = alertEl.textContent.trim();
    if (!text) return;
    let type = 'success';
    if (alertEl.classList.contains('alert-danger')) type = 'error';
    if (alertEl.classList.contains('alert-warning')) type = 'warning';
    showToast(text, type);
    alertEl.style.display = 'none';
  });
});

// ================================
// Form: submit-loading state + duplicate submission prevention
// ================================
function attachFormLoadingState(formEl, loadingText = 'Saving...') {
  if (!formEl) return;
  formEl.addEventListener('submit', function (e) {
    const submitBtn = formEl.querySelector('button[type="submit"]');
    if (!submitBtn) return;
    if (submitBtn.dataset.submitting === 'true') {
      e.preventDefault();
      return;
    }
    submitBtn.dataset.submitting = 'true';
    submitBtn.dataset.originalText = submitBtn.innerHTML;
    submitBtn.classList.add('btn-submit-loading');
    submitBtn.innerHTML = `<span class="btn-spinner"></span>${loadingText}`;
  });
}

// ================================
// Table: search + sort + pagination
// ================================
function initDataTable(tableId, options = {}) {
  const table = document.getElementById(tableId);
  if (!table) return;

  const perPage = options.perPage || 10;
  const searchInputId = options.searchInputId;
  const tbody = table.querySelector('tbody');
  const allRows = Array.from(tbody.querySelectorAll('tr'));
  let currentPage = 1;
  let sortColumn = -1;
  let sortAsc = true;

  function getFilteredRows() {
    const q = searchInputId
      ? (document.getElementById(searchInputId)?.value || '').toLowerCase().trim()
      : '';
    if (!q) return allRows;
    return allRows.filter(row => row.textContent.toLowerCase().includes(q));
  }

  function renderTable() {
    let rows = getFilteredRows();

    if (sortColumn >= 0) {
      rows = rows.slice().sort((a, b) => {
        const aText = a.children[sortColumn]?.textContent.trim().toLowerCase() || '';
        const bText = b.children[sortColumn]?.textContent.trim().toLowerCase() || '';
        return sortAsc ? aText.localeCompare(bText) : bText.localeCompare(aText);
      });
    }

    const totalPages = Math.max(1, Math.ceil(rows.length / perPage));
    if (currentPage > totalPages) currentPage = totalPages;

    allRows.forEach(row => row.style.display = 'none');
    const start = (currentPage - 1) * perPage;
    rows.slice(start, start + perPage).forEach(row => row.style.display = '');

    renderPagination(rows.length, totalPages);
  }

  function renderPagination(totalRows, totalPages) {
    let paginationEl = table.parentElement.querySelector('.table-pagination');
    if (!paginationEl) {
      paginationEl = document.createElement('div');
      paginationEl.className = 'table-pagination';
      table.parentElement.after(paginationEl);
    }

    const start = totalRows === 0 ? 0 : (currentPage - 1) * perPage + 1;
    const end = Math.min(currentPage * perPage, totalRows);

    let buttonsHtml = '';
    for (let p = 1; p <= totalPages; p++) {
      buttonsHtml += `<button data-page="${p}" class="${p === currentPage ? 'active-page' : ''}">${p}</button>`;
    }

    paginationEl.innerHTML = `
      <span>Showing ${start}-${end} of ${totalRows}</span>
      <div class="pagination-buttons">
        <button data-page="prev" ${currentPage === 1 ? 'disabled' : ''}>‹</button>
        ${buttonsHtml}
        <button data-page="next" ${currentPage === totalPages ? 'disabled' : ''}>›</button>
      </div>
    `;

    paginationEl.querySelectorAll('button').forEach(btn => {
      btn.addEventListener('click', () => {
        if (btn.dataset.page === 'prev') currentPage = Math.max(1, currentPage - 1);
        else if (btn.dataset.page === 'next') currentPage = Math.min(totalPages, currentPage + 1);
        else currentPage = parseInt(btn.dataset.page, 10);
        renderTable();
      });
    });
  }

  if (searchInputId) {
    const searchInput = document.getElementById(searchInputId);
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        currentPage = 1;
        renderTable();
      });
    }
  }

  table.querySelectorAll('thead th').forEach((th, index) => {
    th.style.cursor = 'pointer';
    if (!th.querySelector('.sort-icon')) {
      th.innerHTML += ' <i class="bi bi-arrow-down-up sort-icon"></i>';
    }
    th.addEventListener('click', () => {
      if (sortColumn === index) {
        sortAsc = !sortAsc;
      } else {
        sortColumn = index;
        sortAsc = true;
      }
      table.querySelectorAll('thead th').forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
      th.classList.add(sortAsc ? 'sorted-asc' : 'sorted-desc');
      renderTable();
    });
  });

  renderTable();
}