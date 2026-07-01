# HTML Templates Reference

## Shared CSS Styles

```html
<style>
    * { font-family: 'Inter', 'Microsoft YaHei Light', sans-serif; }
    body { background: #FFFFFF; color: #1F2937; font-weight: 300; }
    .hero-gradient { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%); }
    .float-card { transition: transform 0.3s ease, box-shadow 0.3s ease; }
    .float-card:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(37, 99, 235, 0.15); }
    .company-card { border-left: 4px solid #3b82f6; transition: all 0.3s ease; }
    .company-card:hover { border-left-color: #06b6d4; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); }
    .tech-badge { background: rgba(6, 182, 212, 0.1); color: #0891b2; border: 1px solid rgba(6, 182, 212, 0.3); }
    .data-highlight { color: #f59e0b; font-weight: 600; }
    .section-divider { background: linear-gradient(90deg, transparent, #e5e7eb, transparent); }
    .cta-gradient { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); }
    .tab-active { border-bottom: 3px solid #3b82f6; color: #3b82f6; }
    .journal-badge { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); color: #92400e; border: 1px solid #f59e0b; }
    .event-badge { background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); color: #1e40af; border: 1px solid #3b82f6; }
    .summary-card { transition: all 0.3s ease; cursor: pointer; }
    .summary-card:hover { transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
    .date-display { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); border-radius: 8px; padding: 10px 16px; font-size: 14px; color: white; }
    .patent-card { border-left: 4px solid #8b5cf6; transition: all 0.3s ease; }
    .patent-card:hover { border-left-color: #a78bfa; box-shadow: 0 10px 30px rgba(139, 92, 246, 0.15); }
</style>
```

Include in `<head>`:
```html
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<base target="_blank">
```

## index.html Section Templates

### 1. Hero Section
```html
<section class="hero-gradient relative overflow-hidden">
    <div class="absolute inset-0 opacity-10">
        <!-- Decorative SVG shapes -->
        <svg viewBox="0 0 1200 600" class="w-full h-full">
            <circle cx="200" cy="150" r="100" stroke="white" stroke-width="1" fill="none" opacity="0.5"/>
            <circle cx="1000" cy="450" r="150" stroke="white" stroke-width="0.5" fill="none" opacity="0.3"/>
            <rect x="500" y="200" width="200" height="120" stroke="white" stroke-width="1" fill="none" opacity="0.4" rx="10"/>
            <path d="M0,300 Q300,100 600,300 T1200,300" stroke="white" stroke-width="1.5" fill="none" opacity="0.6"/>
        </svg>
    </div>
    <div class="relative max-w-7xl mx-auto px-6 py-16">
        <!-- Title, date range, stat counters -->
    </div>
</section>
```

### 2. Navigation Tabs
```html
<section class="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-6">
        <div class="flex overflow-x-auto">
            <a href="#companies" class="px-6 py-4 text-sm font-medium text-gray-700 hover:text-blue-600 whitespace-nowrap tab-active">核心企业</a>
            <a href="#technologies" class="px-6 py-4 text-sm font-medium text-gray-700 hover:text-blue-600 whitespace-nowrap">技术标签</a>
            <a href="#events" class="px-6 py-4 text-sm font-medium text-gray-700 hover:text-blue-600 whitespace-nowrap">重大事件</a>
            <a href="#journals" class="px-6 py-4 text-sm font-medium text-gray-700 hover:text-blue-600 whitespace-nowrap">顶级期刊</a>
            <a href="#patents" class="px-6 py-4 text-sm font-medium text-gray-700 hover:text-blue-600 whitespace-nowrap">专利技术</a>
            <a href="#methodology" class="px-6 py-4 text-sm font-medium text-gray-700 hover:text-blue-600 whitespace-nowrap">数据来源</a>
        </div>
    </div>
</section>
```

### 3. AI Executive Summary
```html
<section class="max-w-7xl mx-auto px-6 py-12">
    <div class="bg-gradient-to-r from-amber-50 to-yellow-50 rounded-xl p-6 border-l-4 border-amber-500">
        <div class="flex items-center gap-3 mb-4">
            <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            <h3 class="text-lg font-medium text-gray-900">AI智能摘要：周期核心要点（点击卡片跳转）</h3>
        </div>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- 4 summary cards with .summary-card class -->
        </div>
    </div>
</section>
```

### 4. Event Card Template
```html
<div class="bg-white border border-gray-200 rounded-xl p-5 border-l-4 border-l-{color}-500">
    <div class="flex flex-col lg:flex-row lg:items-start gap-4">
        <div class="lg:w-3/4">
            <div class="flex items-center gap-2 mb-2">
                <span class="event-badge px-2 py-1 text-xs rounded">{category}</span>
                <span class="text-sm text-gray-500">{date}</span>
                <span class="text-sm text-gray-400">|</span>
                <span class="text-sm text-gray-500">{source}</span>
            </div>
            <h4 class="text-lg font-medium text-gray-900 mb-2">{title}</h4>
            <p class="text-gray-600 text-sm leading-relaxed mb-3">{content}</p>
        </div>
        <div class="lg:w-1/4 flex items-center justify-end">
            <a href="{url}" class="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors">阅读原文 →</a>
        </div>
    </div>
</div>
```

Event border colors: red, blue, purple, emerald, amber, cyan, pink

### 5. Patent Card Template
```html
<div class="patent-card bg-white border border-gray-200 rounded-xl p-5">
    <div class="flex items-center gap-2 mb-2">
        <span class="px-2 py-1 {status_class} text-xs rounded">{status}</span>
        <span class="text-sm text-gray-500">公开日：{pub_date}</span>
        <span class="text-sm text-gray-400">|</span>
        <span class="text-sm font-mono text-gray-500">{pub_no}</span>
    </div>
    <h4 class="text-lg font-medium text-gray-900 mb-2">{title}</h4>
    <p class="text-sm text-gray-500 mb-3">申请人：{applicant}</p>
    <div class="bg-violet-50 rounded-lg p-4">
        <p class="text-sm text-gray-600"><span class="font-medium text-violet-700">技术核心：</span>{tech_core}</p>
    </div>
</div>
```

### 6. Methodology Section
```html
<section id="methodology" class="max-w-7xl mx-auto px-6 py-12">
    <div class="bg-emerald-50 rounded-xl p-6 border border-emerald-200">
        <!-- Statistics grid (4 cols), data source list, filtering logic, disclaimer -->
    </div>
</section>
```

### 7. Footer + CTA
```html
<section class="cta-gradient py-16">
    <div class="max-w-4xl mx-auto px-6 text-center">
        <h2 class="text-2xl font-medium text-white mb-4">OLED技术情报门户</h2>
        <p class="text-white/80 mb-8">本报告基于公开新闻数据与专利信息整理，为产业决策与技术跟踪提供情报支撑</p>
        <div class="bg-white/20 backdrop-blur px-6 py-3 rounded-lg text-white text-sm inline-block">
            <span class="opacity-70">数据周期：</span><span>2026.3.18-3.27</span>
        </div>
    </div>
</section>

<footer class="bg-gray-900 text-gray-400 py-10">
    <div class="max-w-7xl mx-auto px-6 text-center">
        <p class="text-sm">本报告基于公开新闻数据与专利信息，仅供技术参考，不构成投资建议</p>
        <p class="text-xs mt-2">数据来源：用户提供JSON文件 + 公开网络搜索 + 专利数据Excel</p>
    </div>
</footer>
```

## Detail Page Templates

### Company Page Header
```html
<section class="hero-gradient relative overflow-hidden">
    <div class="relative max-w-7xl mx-auto px-6 py-12">
        <div class="flex items-center gap-4 mb-4">
            <a href="index.html" target="_self" class="text-white/70 hover:text-white flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
                </svg>
                返回首页
            </a>
        </div>
        <div class="flex items-center gap-4">
            <div class="w-16 h-16 bg-white/20 rounded-xl flex items-center justify-center">
                <span class="text-2xl font-bold text-white">{abbr}</span>
            </div>
            <div class="text-white">
                <h1 class="text-3xl font-medium">{company_name}</h1>
                <p class="text-white/70">{company_en}</p>
            </div>
        </div>
    </div>
</section>
```

### Tech Tag Page Header
Same structure but with cyan gradient:
```css
.hero-gradient { background: linear-gradient(135deg, #0891b2 0%, #06b6d4 50%, #22d3ee 100%); }
```

### Patent Page Header
Same structure but with violet gradient:
```css
.hero-gradient { background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 50%, #c4b5fd 100%); }
```

### News Item Template (Detail Pages)
```html
<div class="bg-white border border-gray-200 rounded-xl p-6 mb-4">
    <div class="flex items-center gap-2 mb-3">
        <span class="px-2 py-1 bg-{theme}-100 text-{theme}-700 text-xs rounded">{date}</span>
        <span class="text-sm text-gray-400">|</span>
        <span class="text-sm text-gray-500">{source}</span>
    </div>
    <h3 class="text-lg font-medium text-gray-900 mb-3">{title}</h3>
    <p class="text-gray-600 text-sm leading-relaxed mb-4">{content}</p>
    <a href="{url}" class="inline-flex items-center gap-2 px-4 py-2 bg-{theme}-600 text-white text-sm rounded-lg hover:bg-{theme}-700 transition-colors">
        阅读原文
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
        </svg>
    </a>
</div>
```

Theme colors: blue (company), cyan (tech), violet (patent)

## JavaScript

### Date Edit Function
```javascript
function editDate(type) {
    const currentValue = type === 'start' ? document.getElementById('startDateDisplay').value : document.getElementById('endDateDisplay').value;
    const newValue = prompt('请输入新的日期（格式：YYYY年M月D日）：', currentValue);
    if (newValue && newValue.match(/\d{4}年\d{1,2}月\d{1,2}日/)) {
        if (type === 'start') {
            document.getElementById('startDateDisplay').value = newValue;
        } else {
            document.getElementById('endDateDisplay').value = newValue;
        }
        alert('日期已更新，注意：当前为静态展示，数据内容不会随日期变化。');
    } else if (newValue) {
        alert('日期格式不正确，请使用"YYYY年M月D日"格式');
    }
}
```

### Smooth Scroll for Anchor Links
```javascript
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
```
