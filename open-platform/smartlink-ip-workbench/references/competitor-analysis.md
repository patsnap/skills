# Competitor Analysis Implementation Notes

## Data Contract

The page calls:

```js
fetch(`${ZHIHUIYA_MCP_PROXY}/api/competitor-patent-search`, {
  method: 'POST',
  headers: {'Content-Type':'application/json'},
  body: JSON.stringify({ assignees: names, jurisdiction: jurisdictions, topk: 50 })
})
```

Expected response:

```js
{
  success: true,
  market_scope: '全球智慧芽数据' | 'US' | 'EP' | 'WO',
  submitted_at: '...',
  companies: [{
    name,
    metrics: { total, design, invention, maxCited, ipcTop, active },
    trend: {'2024': 76, '2025': 66},
    patents: [{num, title, appDate, jurisdiction, cited}]
  }]
}
```

## Required UI Linkage

After successful fetch:

```js
currentCompetitorMcpData = data;
compChartsInited = false;
renderCompetitorMcpResults(data);
```

`renderCompetitorMcpResults(data)` should call:

```js
updateCompLiveTable(data);
initCompCharts(data);
renderCompOpportunityCards(data);
```

Market change should rerun analysis if data exists:

```js
function handleCompMarketChange(){
  if(currentCompetitorMcpData) runCompetitorAnalysis();
  else renderCompPendingTable();
}
```

## Radar Scoring

Normalize values across the current applicant set:

- total patents -> 专利武器库
- design patents -> 外观布局
- invention/utility patents -> 技术覆盖
- recent trend sum -> 申请活跃度
- weighted score -> 市场壁垒
- design ratio -> 平台适配

## Opportunity Cards

- Low coverage: company with lowest total.
- Design focus: highest design ratio.
- High risk: highest total or highest recent applications.

Do not leave static text unless the number comes from returned data.

## Proxy Notes

The local proxy may call:

- `search_patents_by_original_assignee`
- `search_patent_count`
- `search_patent_field`
