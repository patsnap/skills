# HTML报告结构规范

## 整体布局

```
┌─────────────────────────────────────────────┐
│  左侧导航栏（固定，220px）  │  主内容区域    │
│  ┌─────────────────────┐  │                │
│  │ 🔬 报告标题          │  │  模块内容       │
│  │ ─────────────────── │  │                │
│  │ 🏠 执行摘要          │  │                │
│  │ 📊 规模与趋势        │  │                │
│  │ 🧬 核心技术方向      │  │                │
│  │ 🦠 关键菌属图谱      │  │                │
│  │ 🏥 疾病关联研究      │  │                │
│  │ 🍽️ 食品干预         │  │                │
│  │ 🏢 主要申请人        │  │                │
│  │ 📄 代表性文献        │  │                │
│  │ 📅 研究时间线        │  │                │
│  │ 🤖 模型微调指引      │  │                │
│  │ 🚀 未来趋势          │  │                │
│  └─────────────────────┘  │                │
└─────────────────────────────────────────────┘
```

## CSS规范

### 配色方案（浅蓝-白色系）
```css
:root {
  --primary: #2563eb;       /* 主色调蓝 */
  --primary-light: #dbeafe; /* 浅蓝背景 */
  --accent: #0ea5e9;        /* 强调色 */
  --bg: #f8fafc;            /* 页面背景 */
  --sidebar-bg: #1e293b;    /* 导航栏深色背景 */
  --sidebar-text: #e2e8f0;  /* 导航栏文字 */
  --sidebar-active: #2563eb;/* 当前选中项 */
  --card-bg: #ffffff;       /* 卡片背景 */
  --text-main: #1e293b;     /* 主文字色 */
  --text-muted: #64748b;    /* 次要文字 */
  --border: #e2e8f0;        /* 边框色 */
  --success: #10b981;       /* 成功/正向 */
  --warning: #f59e0b;       /* 警告/中性 */
  --danger: #ef4444;        /* 危险/负向 */
}
```

### 导航栏样式
```css
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 220px;
  height: 100vh;
  background: var(--sidebar-bg);
  overflow-y: auto;
  z-index: 100;
  padding: 20px 0;
}

.sidebar-header {
  padding: 0 16px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 8px;
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  color: var(--sidebar-text);
  text-decoration: none;
  font-size: 13px;
  transition: background 0.2s;
}

.sidebar-nav a:hover,
.sidebar-nav a.active {
  background: var(--sidebar-active);
  border-radius: 6px;
  margin: 0 8px;
  padding: 10px 8px;
}
```

### 主内容区域
```css
.main-content {
  margin-left: 220px;
  padding: 32px;
  max-width: 1200px;
}
```

### 卡片组件
```css
.card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  margin-bottom: 24px;
  border: 1px solid var(--border);
}

.stat-card {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}

.stat-card .number {
  font-size: 2.5rem;
  font-weight: 700;
}
```

### 文献条目
```css
.paper-item {
  border-left: 3px solid var(--primary);
  padding: 12px 16px;
  margin-bottom: 12px;
  background: var(--primary-light);
  border-radius: 0 8px 8px 0;
}

.paper-item .title {
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 4px;
}

.paper-item .meta {
  font-size: 12px;
  color: var(--text-muted);
}

.tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  background: var(--primary-light);
  color: var(--primary);
  margin-right: 4px;
}
```

## HTML模块结构模板

### 模块1 — 执行摘要
```html
<section id="summary">
  <h2>🏠 执行摘要</h2>
  <div class="stat-grid">
    <div class="stat-card">
      <div class="number">57,341+</div>
      <div class="label">专利文献总量</div>
    </div>
    <!-- 更多统计卡 -->
  </div>
  <div class="card">
    <h3>报告结构导览</h3>
    <!-- 11个模块简介 -->
  </div>
</section>
```

### 模块8 — 代表性文献（带[S#]标注）
```html
<section id="literature">
  <h2>📄 代表性文献</h2>
  <div class="topic-group" id="topic-a">
    <h3>A. 个性化营养与菌群图谱</h3>
    <div class="paper-item">
      <div class="title">[S1] 专利标题...</div>
      <div class="meta">
        <span class="tag">专利</span>
        <span class="tag">A类</span>
        AU2020101019A4 · 2020
      </div>
    </div>
  </div>
</section>
```

## 响应式断点

```css
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s;
  }
  .sidebar.open {
    transform: translateX(0);
  }
  .main-content {
    margin-left: 0;
  }
}
```

## JavaScript交互规范

```javascript
// 导航栏滚动高亮
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.sidebar-nav a');

window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(section => {
    if (window.scrollY >= section.offsetTop - 100) {
      current = section.id;
    }
  });
  navLinks.forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === '#' + current);
  });
});
```
