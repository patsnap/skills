# Technology Tags Reference

## 16 Technology Tags

| # | Chinese Name | English Name | HTML File | Keywords for Matching |
|---|-------------|-------------|-----------|----------------------|
| 1 | 叠层/串联OLED | Tandem OLED | tech-tandem.html | Tandem, 叠层, 串联, Penta, 五层, Primary RGB |
| 2 | 量子点OLED | QD-OLED | tech-qdoled.html | QD-OLED, QuantumBlack, 量子点, Quantum Dot |
| 3 | 白光OLED | WOLED | tech-w-oled.html | WOLED, 白光, White OLED |
| 4 | 无FMM | ViP/eLEAP/FPM | tech-fmm.html | FMM, eLEAP, ViP, 无FMM, 金属掩模 |
| 5 | LTPO/LTPS+Oxide | 低温多晶硅+氧化物 | tech-ltpo.html | LTPO, LTPS, Oxide, 氧化物 |
| 6 | 高迁移率氧化物 | HMO/Oxide | tech-oxide.html | HMO, 高迁移率, Oxide |
| 7 | 无偏光片 | Pol-less/COE | tech-pol-less.html | Pol-less, 偏光片, COE, Color on Encapsulation |
| 8 | 自主发光材料 | TADF/PSF/磷光 | tech-materials.html | TADF, 磷光, Phosphorescent, 发光材料, Material, UDC, Lordin |
| 9 | 柔性OLED | Flexible OLED | tech-flexible.html | Flexible, 柔性, 显示器, Monitor, 屏幕 |
| 10 | 折叠屏 | Foldable Display | tech-foldable.html | Foldable, 折叠, 折痕, Creaseless, Fold |
| 11 | 可拉伸显示 | Stretchable Display | tech-stretchable.html | Stretchable, 拉伸, 可拉伸 |
| 12 | 车载显示 | Automotive Display | tech-automotive.html | Automotive, 车载, P2P, Pillar, 汽车 |
| 13 | 微透镜阵列 | MLA | tech-mla.html | MLA, 微透镜, Micro Lens |
| 14 | 印刷OLED | IJP | tech-ijp.html | 印刷, IJP, Inkjet, 喷墨 |
| 15 | 屏下摄像头 | UDC/FDC | tech-udc.html | UDC, FDC, 屏下, Under Display |
| 16 | 8.6代/8代OLED | G8.x/G8 | tech-g8.html | 8.6代, G8, Gen 8, 高世代 |

## Tech Tag Classification Algorithm

```python
tech_keywords = {
    'tech-tandem': ['Tandem', '叠层', '串联', 'Penta', '五层', 'Primary RGB'],
    'tech-qdoled': ['QD-OLED', 'QuantumBlack', '量子点', 'Quantum Dot'],
    'tech-w-oled': ['WOLED', '白光', 'White OLED'],
    'tech-fmm': ['FMM', 'eLEAP', 'ViP', '无FMM', '金属掩模', '掩模'],
    'tech-ltpo': ['LTPO', 'LTPS', 'Oxide', '氧化物', '低温多晶'],
    'tech-oxide': ['HMO', '高迁移率', 'Oxide'],
    'tech-pol-less': ['Pol-less', '偏光片', 'COE', 'Color on Encapsulation'],
    'tech-materials': ['TADF', '磷光', 'Phosphorescent', '发光材料', 'Material', 
                       'UDC', 'Lordin', '发光层', 'EML', 'Host', 'Dopant'],
    'tech-flexible': ['Flexible', '柔性', '显示器', 'Monitor', '屏幕', 'Display'],
    'tech-foldable': ['Foldable', '折叠', '折痕', 'Creaseless', 'Fold', '可折叠'],
    'tech-stretchable': ['Stretchable', '拉伸', '可拉伸'],
    'tech-automotive': ['Automotive', '车载', 'P2P', 'Pillar', '汽车', 'Vehicle'],
    'tech-mla': ['MLA', '微透镜', 'Micro Lens', 'Lens Array'],
    'tech-ijp': ['印刷', 'IJP', 'Inkjet', '喷墨', '打印'],
    'tech-udc': ['UDC', 'FDC', '屏下', 'Under Display', '屏下摄像'],
    'tech-g8': ['8.6代', 'G8', 'Gen 8', '高世代', '8.5代', '8代'],
}

def classify_news_to_tech(news_item):
    """Classify a news item to technology tags based on keyword matching."""
    text = (news_item.get('title', '') + ' ' + news_item.get('content', '')).lower()
    matched_tags = []
    for tag_id, keywords in tech_keywords.items():
        for kw in keywords:
            if kw.lower() in text:
                matched_tags.append(tag_id)
                break
    return matched_tags
```

## Tech Tag Card HTML Template

### With News
```html
<a href="{tag_file}.html" class="float-card bg-gradient-to-br from-{color}-50 to-white p-4 rounded-xl border border-{color}-100">
    <div class="flex items-center justify-between mb-2">
        <span class="px-2 py-1 bg-{color}-100 text-{color}-700 text-xs rounded">热门</span>
        <span class="text-xs text-gray-400">{count}条新闻</span>
    </div>
    <h3 class="font-medium text-gray-900 mb-1">{name_cn}</h3>
    <p class="text-xs text-gray-500 mb-2">{name_en}</p>
    <p class="text-sm text-gray-600">{summary}</p>
</a>
```

### Empty (No News)
```html
<div class="float-card bg-gradient-to-br from-gray-50 to-white p-4 rounded-xl border border-gray-100 opacity-60">
    <div class="flex items-center justify-between mb-2">
        <span class="text-xs text-gray-400">无新闻</span>
    </div>
    <h3 class="font-medium text-gray-900 mb-1">{name_cn}</h3>
    <p class="text-xs text-gray-500 mb-2">{name_en}</p>
    <p class="text-sm text-gray-500">本周期内暂无相关新闻</p>
</div>
```

## Color Rotation for Tech Cards

```python
tech_colors = ['blue', 'purple', 'emerald', 'rose', 'cyan', 'amber', 
               'pink', 'indigo', 'teal', 'orange', 'violet', 'lime']
# Assign: color = tech_colors[index % len(tech_colors)]
```

## Tech Page Name Mapping

```python
tech_page_map = {
    '叠层/串联OLED': ('tech-tandem', 'Tandem OLED'),
    '量子点OLED': ('tech-qdoled', 'QD-OLED'),
    '白光OLED': ('tech-w-oled', 'WOLED'),
    '无FMM': ('tech-fmm', 'ViP/eLEAP/FPM'),
    'LTPO/LTPS+Oxide': ('tech-ltpo', '低温多晶硅+氧化物'),
    '高迁移率氧化物': ('tech-oxide', 'HMO/Oxide'),
    '无偏光片': ('tech-pol-less', 'Pol-less/COE'),
    '自主发光材料': ('tech-materials', 'TADF/PSF/磷光'),
    '柔性OLED': ('tech-flexible', 'Flexible OLED'),
    '折叠屏': ('tech-foldable', 'Foldable Display'),
    '可拉伸显示': ('tech-stretchable', 'Stretchable Display'),
    '车载显示': ('tech-automotive', 'Automotive Display'),
    '微透镜阵列': ('tech-mla', 'MLA'),
    '印刷OLED': ('tech-ijp', 'IJP'),
    '屏下摄像头': ('tech-udc', 'UDC/FDC'),
    '8.6代/8代OLED': ('tech-g8', 'G8.x/G8'),
}
```
