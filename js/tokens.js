let allTokens = [];
let currentFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
  loadTokens();
  setupFilters();
});

function showLoading() {
  const tbody = document.getElementById('tokensTableBody');
  const emptyState = document.getElementById('emptyState');
  const table = document.getElementById('tokensTable');

  table.style.display = 'table';
  emptyState.style.display = 'none';

  tbody.innerHTML = `
    <tr>
      <td><div class="skeleton" style="width:100px;height:16px;"></div></td>
      <td><div class="skeleton" style="width:80px;height:16px;"></div></td>
      <td><div class="skeleton" style="width:100px;height:16px;"></div></td>
      <td><div class="skeleton" style="width:60px;height:24px;border-radius:20px;"></div></td>
      <td><div class="skeleton" style="width:60px;height:32px;border-radius:8px;"></div></td>
    </tr>
    <tr>
      <td><div class="skeleton" style="width:120px;height:16px;"></div></td>
      <td><div class="skeleton" style="width:90px;height:16px;"></div></td>
      <td><div class="skeleton" style="width:100px;height:16px;"></div></td>
      <td><div class="skeleton" style="width:60px;height:24px;border-radius:20px;"></div></td>
      <td><div class="skeleton" style="width:60px;height:32px;border-radius:8px;"></div></td>
    </tr>
    <tr>
      <td><div class="skeleton" style="width:110px;height:16px;"></div></td>
      <td><div class="skeleton" style="width:70px;height:16px;"></div></td>
      <td><div class="skeleton" style="width:100px;height:16px;"></div></td>
      <td><div class="skeleton" style="width:60px;height:24px;border-radius:20px;"></div></td>
      <td><div class="skeleton" style="width:60px;height:32px;border-radius:8px;"></div></td>
    </tr>
  `;
}

async function loadTokens() {
  showLoading();

  try {
    const response = await fetch('./data/tokens.json');
    const data = await response.json();
    allTokens = data.tokens || [];
    renderTable();
  } catch (error) {
    console.error('加载Token数据失败:', error);
    showEmptyState();
  }
}

function setupFilters() {
  const filterTabs = document.querySelectorAll('#filterTabs .filter-tab');
  filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      filterTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      currentFilter = tab.dataset.filter;
      renderTable();
    });
  });
}

function renderTable() {
  const tbody = document.getElementById('tokensTableBody');
  const emptyState = document.getElementById('emptyState');
  const table = document.getElementById('tokensTable');

  const filteredTokens = filterTokens(allTokens, currentFilter);

  if (filteredTokens.length === 0) {
    tbody.innerHTML = '';
    table.style.display = 'none';
    emptyState.style.display = 'block';
    return;
  }

  table.style.display = 'table';
  emptyState.style.display = 'none';

  tbody.innerHTML = filteredTokens.map(token => {
    const statusInfo = getStatusInfo(token.status);
    return `
      <tr>
        <td>${escapeHtml(token.platform)}</td>
        <td>${escapeHtml(token.tokenAmount)}</td>
        <td>${escapeHtml(token.validityPeriod)}</td>
        <td><span class="status-badge ${statusInfo.class}">${statusInfo.label}</span></td>
        <td>
          <a href="${escapeHtml(token.claimUrl)}" target="_blank" rel="noopener noreferrer"
             class="claim-btn ${token.status === 'expired' ? 'disabled' : ''}">
            ${token.status === 'expired' ? '已过期' : '领取'}
          </a>
        </td>
      </tr>
    `;
  }).join('');
}

function filterTokens(tokens, filter) {
  if (filter === 'all') {
    return tokens;
  }

  const now = new Date();
  const oneMonthLater = new Date();
  oneMonthLater.setMonth(oneMonthLater.getMonth() + 1);

  return tokens.filter(token => {
    const expiryDate = parseDate(token.validityPeriod);

    if (filter === 'expiring') {
      if (!expiryDate) return false;
      return expiryDate <= oneMonthLater && expiryDate >= now;
    }

    if (filter === 'longterm') {
      if (!expiryDate) return true;
      return expiryDate > oneMonthLater;
    }

    return true;
  });
}

function parseDate(dateStr) {
  if (!dateStr) return null;
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return null;
  return date;
}

function getStatusInfo(status) {
  const statusMap = {
    'active': { label: '可领取', class: 'status-active' },
    'expired': { label: '已领完', class: 'status-expired' },
    'limited': { label: '限时', class: 'status-limited' }
  };
  return statusMap[status] || { label: status, class: 'status-limited' };
}

function showEmptyState() {
  const tbody = document.getElementById('tokensTableBody');
  const emptyState = document.getElementById('emptyState');
  const table = document.getElementById('tokensTable');
  tbody.innerHTML = '';
  table.style.display = 'none';
  emptyState.style.display = 'block';
}

function escapeHtml(text) {
  if (typeof text !== 'string') return text;
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
