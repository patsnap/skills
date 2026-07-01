# Company Mapping Reference

## 12 OLED Core Companies

| Chinese Name | English Name | Abbr | Color | HTML Filename | Logo BG |
|-------------|-------------|------|-------|--------------|---------|
| 三星显示 | Samsung Display | SDC | blue | samsung.html | bg-blue-600 |
| 乐金显示 | LG Display | LGD | red | lg.html | bg-red-600 |
| 京东方 | BOE Technology | BOE | emerald | boe.html | bg-emerald-600 |
| 华星光电 | TCL CSOT | CSOT | purple | tcl.html | bg-purple-600 |
| 维信诺 | Visionox | VIX | cyan | visionox.html | bg-cyan-600 |
| 天马微电子 | Tianma Micro-electronics | TM | indigo | tianma.html | bg-indigo-600 |
| 和辉光电 | EverDisplay | EDO | gray | ivo.html | bg-gray-600 |
| 夏普 | Sharp | SH | gray | sharp.html | bg-gray-600 |
| 日本显示器 | Japan Display Inc. | JDI | gray | jdi.html | bg-gray-600 |
| 龙腾光电 | InfoVision Optoelectronics | IVO | gray | leo.html | bg-gray-600 |
| 友达光电 | AU Optronics | AUO | gray | auo.html | bg-gray-600 |
| 群创光电 | Innolux | INX | gray | innolux.html | bg-gray-600 |

## JSON Filename to Company Name Mapping

```python
json_to_company = {
    'news_三星显示-1.json': '三星显示',
    'news_乐金显示-1.json': '乐金显示',
    'news_京东方-1.json': '京东方',
    'news_华星光电-1.json': '华星光电',
    'news_维信诺-1.json': '维信诺',
    'news_天马微电子-1.json': '天马微电子',
    'news_和辉光电-1.json': '和辉光电',
    'news_夏普-1.json': '夏普',
    'news_日本显示器-1.json': '日本显示器',
    'news_龙腾光电-1.json': '龙腾光电',
    'news_友达光电-1.json': '友达光电',
    'news_群创光电-1.json': '群创光电',
}
```

## HTML Page Name Mapping

```python
company_page_map = {
    '三星显示': 'samsung',
    '乐金显示': 'lg',
    '京东方': 'boe',
    '华星光电': 'tcl',
    '维信诺': 'visionox',
    '天马微电子': 'tianma',
    '和辉光电': 'ivo',
    '夏普': 'sharp',
    '日本显示器': 'jdi',
    '龙腾光电': 'leo',
    '友达光电': 'auo',
    '群创光电': 'innolux',
}
```

## Company Info Dictionary

```python
company_name_map = {
    '三星显示': {'en': 'Samsung Display', 'abbr': 'SDC', 'color': 'blue'},
    '乐金显示': {'en': 'LG Display', 'abbr': 'LGD', 'color': 'red'},
    '京东方': {'en': 'BOE Technology', 'abbr': 'BOE', 'color': 'emerald'},
    '华星光电': {'en': 'TCL CSOT', 'abbr': 'CSOT', 'color': 'purple'},
    '维信诺': {'en': 'Visionox', 'abbr': 'VIX', 'color': 'cyan'},
    '天马微电子': {'en': 'Tianma Micro-electronics', 'abbr': 'TM', 'color': 'indigo'},
    '和辉光电': {'en': 'EverDisplay', 'abbr': 'EDO', 'color': 'gray'},
    '夏普': {'en': 'Sharp', 'abbr': 'SH', 'color': 'gray'},
    '日本显示器': {'en': 'Japan Display Inc.', 'abbr': 'JDI', 'color': 'gray'},
    '龙腾光电': {'en': 'InfoVision Optoelectronics', 'abbr': 'IVO', 'color': 'gray'},
    '友达光电': {'en': 'AU Optronics', 'abbr': 'AUO', 'color': 'gray'},
    '群创光电': {'en': 'Innolux', 'abbr': 'INX', 'color': 'gray'},
}
```

## Company Card HTML Template

### With News
```html
<a href="{page}.html" class="company-card bg-white border border-gray-200 rounded-xl p-5 float-card">
    <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-{color}-600 rounded-lg flex items-center justify-center text-white font-bold">{abbr}</div>
            <div>
                <h3 class="font-medium text-gray-900">{name}</h3>
                <p class="text-xs text-gray-500">{en}</p>
            </div>
        </div>
        <span class="px-2 py-1 bg-red-100 text-red-700 text-xs rounded">{count}条新闻</span>
    </div>
    <p class="text-sm text-gray-600 mb-3">{summary}</p>
    <div class="flex flex-wrap gap-2">
        <span class="tech-badge px-2 py-1 text-xs rounded">{tag1}</span>
        <span class="tech-badge px-2 py-1 text-xs rounded">{tag2}</span>
    </div>
</a>
```

### Empty (No News)
```html
<div class="company-card bg-white border border-gray-200 rounded-xl p-5 opacity-60">
    <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gray-500 rounded-lg flex items-center justify-center text-white font-bold">{abbr}</div>
            <div>
                <h3 class="font-medium text-gray-900">{name}</h3>
                <p class="text-xs text-gray-500">{en}</p>
            </div>
        </div>
        <span class="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">无新闻</span>
    </div>
    <p class="text-sm text-gray-500">本周期内暂无相关新闻</p>
</div>
```
