document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const filterTabs = document.getElementById('filterTabs');
  const toolsList = document.getElementById('toolsList');
  const emptyState = document.getElementById('emptyState');

  let allTools = [];
  let currentCategory = '全部';
  let currentSearch = '';

  const categoryIcons = {
    '聊天': '💬',
    '图像': '🎨',
    '代码': '💻',
    '写作': '📝',
    '音频': '🎵',
    '视频': '🎬'
  };

  function showLoading() {
    toolsList.innerHTML = `
      <div class="tool-item skeleton-item">
        <div class="tool-item-header">
          <div class="skeleton" style="width:48px;height:48px;border-radius:50%;flex-shrink:0;"></div>
          <div style="flex:1;min-width:0;">
            <div class="skeleton" style="width:120px;height:18px;margin-bottom:8px;"></div>
            <div class="skeleton" style="width:80%;height:14px;"></div>
          </div>
        </div>
      </div>
      <div class="tool-item skeleton-item">
        <div class="tool-item-header">
          <div class="skeleton" style="width:48px;height:48px;border-radius:50%;flex-shrink:0;"></div>
          <div style="flex:1;min-width:0;">
            <div class="skeleton" style="width:100px;height:18px;margin-bottom:8px;"></div>
            <div class="skeleton" style="width:60%;height:14px;"></div>
          </div>
        </div>
      </div>
      <div class="tool-item skeleton-item">
        <div class="tool-item-header">
          <div class="skeleton" style="width:48px;height:48px;border-radius:50%;flex-shrink:0;"></div>
          <div style="flex:1;min-width:0;">
            <div class="skeleton" style="width:140px;height:18px;margin-bottom:8px;"></div>
            <div class="skeleton" style="width:70%;height:14px;"></div>
          </div>
        </div>
      </div>
    `;
    emptyState.style.display = 'none';
  }

  async function loadTools() {
    showLoading();

    try {
      const response = await fetch('./data/tools.json');
      const data = await response.json();
      allTools = data.tools || [];
      renderTools();
    } catch (error) {
      console.error('加载工具数据失败:', error);
      toolsList.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">⚠️</div>
          <h3>加载失败</h3>
          <p>无法加载工具数据，请稍后重试</p>
        </div>
      `;
    }
  }

  function getToolIcon(tool) {
    if (tool.icon) return tool.icon;
    return categoryIcons[tool.category] || tool.name.charAt(0).toUpperCase();
  }

  function filterTools() {
    return allTools.filter(tool => {
      const matchCategory = currentCategory === '全部' || tool.category === currentCategory;
      const searchLower = currentSearch.toLowerCase();
      const matchSearch = !currentSearch ||
        tool.name.toLowerCase().includes(searchLower) ||
        tool.description.toLowerCase().includes(searchLower) ||
        (tool.tags && tool.tags.some(tag => tag.toLowerCase().includes(searchLower)));
      return matchCategory && matchSearch;
    });
  }

  function renderTools() {
    const filtered = filterTools();

    if (filtered.length === 0) {
      toolsList.style.display = 'none';
      emptyState.style.display = 'block';
      return;
    }

    toolsList.style.display = 'block';
    emptyState.style.display = 'none';

    toolsList.innerHTML = filtered.map(tool => `
      <div class="tool-item" data-id="${tool.id}">
        <div class="tool-item-header">
          <div class="tool-icon-wrap">${getToolIcon(tool)}</div>
          <div class="tool-info">
            <div class="tool-name">${escapeHtml(tool.name)}</div>
            <div class="tool-desc">${escapeHtml(tool.description)}</div>
            <span class="tool-category-tag">${escapeHtml(tool.category)}</span>
          </div>
          <div class="tool-meta">
            <span class="tool-pricing">${escapeHtml(tool.pricing || '未知')}</span>
            <span class="tool-arrow">▼</span>
          </div>
        </div>
        <div class="tool-details">
          <div class="tool-details-inner">
            <div class="detail-section">
              <div class="detail-label">功能特点</div>
              <div class="detail-features">
                ${(tool.features || []).map(f => `<span class="detail-feature">${escapeHtml(f)}</span>`).join('')}
              </div>
            </div>
            <div class="detail-section">
              <div class="detail-label">官网链接</div>
              <a href="${escapeHtml(tool.url || '#')}" target="_blank" rel="noopener noreferrer" class="detail-link" onclick="event.stopPropagation();">
                ${escapeHtml(tool.url || '#')}
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
            <div class="detail-section">
              <div class="detail-label">价格</div>
              <span style="color: var(--color-text); font-size: 0.95rem;">${escapeHtml(tool.pricing || '未知')}</span>
            </div>
            <div class="detail-section">
              <div class="detail-label">标签</div>
              <div class="detail-tags">
                ${(tool.tags || []).map(tag => `<span class="detail-tag">${escapeHtml(tag)}</span>`).join('')}
              </div>
            </div>
          </div>
        </div>
      </div>
    `).join('');

    document.querySelectorAll('.tool-item').forEach(item => {
      item.addEventListener('click', () => {
        const isExpanded = item.classList.contains('expanded');
        document.querySelectorAll('.tool-item.expanded').forEach(expanded => {
          if (expanded !== item) expanded.classList.remove('expanded');
        });
        item.classList.toggle('expanded', !isExpanded);
      });
    });
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  searchInput.addEventListener('input', (e) => {
    currentSearch = e.target.value.trim();
    renderTools();
  });

  filterTabs.addEventListener('click', (e) => {
    if (e.target.classList.contains('filter-tab')) {
      filterTabs.querySelectorAll('.filter-tab').forEach(tab => tab.classList.remove('active'));
      e.target.classList.add('active');
      currentCategory = e.target.dataset.category;
      renderTools();
    }
  });

  loadTools();
});
