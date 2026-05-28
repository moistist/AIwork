// AI新闻页面 JavaScript
let newsData = { news: [] };

// 页面加载时获取数据
document.addEventListener('DOMContentLoaded', () => {
  loadNewsData();
});

// 加载新闻数据
async function loadNewsData() {
  try {
    const response = await fetch('./data/news.json');
    if (!response.ok) throw new Error('Failed to load news data');
    newsData = await response.json();
    renderNews();
  } catch (error) {
    console.error('Error loading news:', error);
    showEmptyState();
  }
}

// 渲染新闻列表
function renderNews() {
  const newsGrid = document.getElementById('newsGrid');
  const emptyState = document.getElementById('emptyState');

  if (!newsData.news || newsData.news.length === 0) {
    showEmptyState();
    return;
  }

  emptyState.style.display = 'none';
  newsGrid.style.display = 'grid';

  newsGrid.innerHTML = newsData.news.map(news => `
    <div class="news-card">
      <div class="news-card-content">
        <div class="news-meta">
          <span class="news-source">${escapeHtml(news.source)}</span>
          <span class="news-date">${formatDate(news.publishedAt)}</span>
        </div>
        <h3 class="news-title">${escapeHtml(news.title)}</h3>
        <p class="news-summary">${escapeHtml(news.summary)}</p>
        <div class="news-tags">
          ${news.tags.map(tag => `<span class="news-tag">${escapeHtml(tag)}</span>`).join('')}
        </div>
        <a href="${escapeHtml(news.url)}" target="_blank" rel="noopener noreferrer" class="news-link">
          阅读原文 →
        </a>
      </div>
    </div>
  `).join('');
}

// 显示空状态
function showEmptyState() {
  const newsGrid = document.getElementById('newsGrid');
  const emptyState = document.getElementById('emptyState');
  
  newsGrid.style.display = 'none';
  emptyState.style.display = 'block';
}

// 格式化日期
function formatDate(dateStr) {
  const date = new Date(dateStr);
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleDateString('zh-CN', options);
}

// 转义HTML
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
