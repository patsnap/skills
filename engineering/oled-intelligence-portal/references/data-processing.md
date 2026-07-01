# Data Processing Reference

## JSON News File Parsing

### File Naming Convention
Input files follow the pattern:
- `news_{company_name}-1.json` for company-specific news
- `技术方向_news-1.json` for technology-direction news
- `重大事件-1.json` for major industry events

### JSON Format
Each file contains multiple JSON objects concatenated together (not a valid JSON array). Each object has:

```json
{
  "company": "company_name",
  "uuid": "unique_id",
  "title": "News Title",
  "mid": "message_id",
  "content": "Full content text...",
  "web_url": "https://example.com/article",
  "pic_urls": [],
  "publisher": {
    "platform": "media_platform",
    "site_name": "Website Name",
    "id": "site|id",
    "name": "Publisher Name",
    "entity": "Entity Name"
  },
  "ctime": 1772159313,
  "url": "https://example.com/article",
  "images": []
}
```

### Parsing Algorithm

```python
import json
from datetime import datetime

def parse_json_file(filepath):
    """Parse multi-object JSON file, return list of normalized records."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    records = []
    decoder = json.JSONDecoder()
    idx = 0
    
    while idx < len(content):
        try:
            # Skip whitespace
            while idx < len(content) and content[idx] in ' \t\n\r':
                idx += 1
            if idx >= len(content):
                break
            
            obj, end_idx = decoder.raw_decode(content, idx)
            
            if isinstance(obj, dict) and 'title' in obj:
                # Convert timestamp to date string
                ctime = obj.get('ctime', '')
                if ctime and isinstance(ctime, (int, float)):
                    obj['date_str'] = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d')
                else:
                    obj['date_str'] = 'N/A'
                
                # Extract human-readable source name
                pub = obj.get('publisher', {})
                if isinstance(pub, dict):
                    obj['source_name'] = pub.get('name', pub.get('site_name', pub.get('platform', '未知')))
                else:
                    obj['source_name'] = str(pub) if pub else '未知来源'
                
                records.append(obj)
            
            idx += end_idx
        except json.JSONDecodeError:
            idx += 1  # Skip problematic character
    
    return records
```

### Data Organization

After parsing all files, organize into:

```python
company_news = {
    '三星显示': [record1, record2, ...],
    '乐金显示': [...],
    '京东方': [...],
    '华星光电': [...],
    '维信诺': [...],
    '天马微电子': [...],
    '和辉光电': [...],
    '夏普': [...],
    '日本显示器': [...],
    '龙腾光电': [...],
    '友达光电': [...],
    '群创光电': [...],
}

tech_news = [record1, record2, ...]  # from 技术方向_news
event_news = [record1, record2, ...]  # from 重大事件
```

### Empty File Handling
Some JSON files may be empty (e.g., `news_天马微电子-1.json`). Handle gracefully with 0 records.

## Patent Excel Processing

### Excel Columns to Extract

| Excel Column | Field Name | Description |
|-------------|-----------|-------------|
| 公开(公告)号 | pub_no | Patent publication number |
| 标题 | title | Patent title in Chinese |
| 法律状态/事件 | status | Legal status (公开/实质审查/PCT未进入指定国/etc.) |
| [标]当前申请(专利权)人 | applicant | Patent applicant/assignee |
| 公开(公告)日 | pub_date | Publication date (YYYY-MM-DD) |
| Patsnap专利标题 / 技术功效 | tech_core | Technical core description |

### Reading Method

Use `mshtools-read_file` tool to read the Excel file. The tool converts Excel to markdown table format. Parse the markdown table to extract patent records.

### Patent Record Structure

```python
patent = {
    'pub_no': 'CN121751951A',
    'title': '一种OLED显示面板发光层的制造方法及其应用',
    'status': '公开',
    'applicant': '台州光电产业创新中心',
    'pub_date': '2026-03-27',
    'tech_core': '采用光刻、干法刻蚀等高精度图形化技术...'
}
```

### Status Badge Colors

| Status | CSS Class |
|--------|----------|
| 公开 | bg-green-100 text-green-700 |
| 实质审查 | bg-amber-100 text-amber-700 |
| PCT未进入指定国 | bg-gray-100 text-gray-700 |
| PCT进入指定国 | bg-blue-100 text-blue-700 |
| - (dash) | bg-gray-100 text-gray-500 |

## Supplemental News via Web Search

When user requests more content, search for additional OLED news within the target date range.

### Search Strategy

1. **Search queries** (use `mshtools-web_search`):
   - `OLED AMOLED news March 2026`
   - `Samsung Display OLED 2026`
   - `LG Display OLED 2026`
   - `京东方 OLED 2026年3月`
   - `TCL华星 OLED 2026年3月`
   - `OLED market 2026`
   - `QD-OLED news 2026`
   - `foldable OLED 2026`
   - `OLED patent 2026`

2. **Extract from search results**: title, date, source, URL, content snippet

3. **Normalize format** to match JSON records:
   ```python
   supplemental_record = {
       'title': result_title,
       'content': result_snippet,
       'date': result_date,        # e.g. '2026-03-26'
       'date_str': result_date,    # same as date
       'source': result_source,    # e.g. 'Notebookcheck'
       'source_name': result_source,
       'url': result_url,
       'web_url': result_url,
   }
   ```

4. **Merge with JSON data** by company/tech category for display.

### Data Statistics for Methodology Section

Report actual counts:
```python
total_json_news = sum(len(v) for v in company_news.values()) + len(tech_news) + len(event_news)
total_supplemental = sum(len(v) for v in supplemental_news.values())
total_patents = len(patents)
total_companies = len([c for c in company_news if len(company_news[c]) > 0])
```
