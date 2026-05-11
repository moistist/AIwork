document.addEventListener('DOMContentLoaded', () => {
  initStarfield();
  loadTools();
});

function initStarfield() {
  const canvas = document.getElementById('starfield');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height;
  let stars = [];
  let nebulas = [];

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    initStars();
    initNebulas();
  }

  function initStars() {
    stars = [];
    const count = Math.floor((width * height) / 4000);
    for (let i = 0; i < count; i++) {
      stars.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 1.5 + 0.3,
        alpha: Math.random(),
        speed: Math.random() * 0.02 + 0.005,
        twinkleSpeed: Math.random() * 0.03 + 0.01,
        twinkleDir: 1
      });
    }
  }

  function initNebulas() {
    nebulas = [];
    const count = 4;
    for (let i = 0; i < count; i++) {
      nebulas.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 200 + 150,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        hue: Math.random() > 0.5 ? 40 : 45,
        alpha: 0.03 + Math.random() * 0.04
      });
    }
  }

  function drawNebula(n) {
    const gradient = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.radius);
    gradient.addColorStop(0, `hsla(${n.hue}, 70%, 50%, ${n.alpha})`);
    gradient.addColorStop(0.5, `hsla(${n.hue}, 60%, 40%, ${n.alpha * 0.5})`);
    gradient.addColorStop(1, 'hsla(0, 0%, 0%, 0)');
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
    ctx.fill();
  }

  function drawStar(s) {
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(255, 220, 120, ${s.alpha})`;
    ctx.fill();

    if (s.radius > 1) {
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.radius * 3, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 200, 80, ${s.alpha * 0.15})`;
      ctx.fill();
    }
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    for (const n of nebulas) {
      n.x += n.vx;
      n.y += n.vy;

      if (n.x < -n.radius) n.x = width + n.radius;
      if (n.x > width + n.radius) n.x = -n.radius;
      if (n.y < -n.radius) n.y = height + n.radius;
      if (n.y > height + n.radius) n.y = -n.radius;

      drawNebula(n);
    }

    for (const s of stars) {
      s.alpha += s.twinkleSpeed * s.twinkleDir;
      if (s.alpha >= 1 || s.alpha <= 0.2) {
        s.twinkleDir *= -1;
      }
      s.alpha = Math.max(0.1, Math.min(1, s.alpha));

      s.y -= s.speed;
      if (s.y < 0) {
        s.y = height;
        s.x = Math.random() * width;
      }

      drawStar(s);
    }

    requestAnimationFrame(animate);
  }

  resize();
  window.addEventListener('resize', resize);
  animate();
}

function createSkeletonCards(count) {
  return Array.from({ length: count }, () => `
    <div class="skeleton-card">
      <div class="skeleton skeleton-icon"></div>
      <div class="skeleton skeleton-title"></div>
      <div class="skeleton skeleton-text"></div>
      <div class="skeleton skeleton-text short"></div>
    </div>
  `).join('');
}

async function loadTools() {
  const container = document.getElementById('tools-preview');
  if (!container) return;

  container.innerHTML = createSkeletonCards(6);

  try {
    const response = await fetch('./data/tools.json');
    const data = await response.json();
    const popularTools = data.tools.filter(t => t.popular).slice(0, 6);

    container.innerHTML = popularTools.map((tool, index) => `
      <div class="tool-card scroll-reveal" style="transition-delay: ${index * 0.1}s">
        <div class="tool-icon">${tool.icon || tool.name.charAt(0)}</div>
        <h3 class="tool-name">${tool.name}</h3>
        <p class="tool-desc">${tool.description}</p>
        <span class="tool-tag">${tool.category}</span>
      </div>
    `).join('');

    initScrollReveal();
  } catch (err) {
    container.innerHTML = '<p style="text-align:center;color:var(--color-text-muted)">加载工具数据失败</p>';
    console.error('Failed to load tools:', err);
  }
}

function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  document.querySelectorAll('.scroll-reveal').forEach(el => {
    observer.observe(el);
  });
}
