# HTML报告骨架模板

> **使用说明**：本文件为固定的HTML报告框架模板。生成报告时，按以下步骤执行：
> 1. 复制本模板为报告文件
> 2. 将模板中所有 `{{变量名}}` 占位符替换为实际数据
> 3. 将各小节内容填入 `<!-- SECTION_N: -->` 和 `<!-- /SECTION_N -->` 之间的区域
> 4. 执行20项检查清单验证

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{{company_cn}} — 企业战略专利分析报告</title>
  <style>
    /* === 强制配色（不可更改） === */
    :root { --blue: #0a3dff; --green: #0fcc7a; --gray: #D9D9D9; --yellow: #fff9e6; }
    body { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif; font-size: 14px; line-height: 1.6; color: #1a1a1a; background: #f5f6f8; margin: 0; padding: 0; }
    .main-content { max-width: 1100px; margin: 0 auto; padding: 24px 32px; }
    .section-title { font-size: 18px; font-weight: 700; color: #1a1a1a; padding: 12px 16px; border-left: 4px solid #0a3dff; margin: 32px 0 0px; }
    .section-subtitle { display: block; font-size: 13px; color: #666; margin: 4px 0 16px 16px; background: #f8f9fa; }
    .chart-box { width: 100%; box-sizing: border-box; background: #fff; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); margin: 16px 0; }
    .chart-box img { max-width: 100%; height: auto; }
    table { width: 100%; border-collapse: collapse; }
    th { background: #0a3dff; color: #fff; padding: 10px 12px; text-align: left; font-size: 13px; font-weight: 600; }
    td { padding: 10px 12px; border-bottom: 1px solid #f0f0f0; font-size: 13px; }
    tr:nth-child(even) { background: #fafbfc; }
    tr:hover { background: #f0f3ff; }
    .conclusion-box { background: #fff9e6; border-radius: 6px; padding: 14px 16px; margin: 16px 0; }
    .conclusion-box ol { margin: 8px 0 0 0; padding-left: 18px; }
    .conclusion-box li { margin-bottom: 6px; color: #333; font-size: 13px; }
    .source-hint { color: #999; font-size: 12px; margin-top: 8px; padding-top: 6px; border-top: 1px dashed #e0e0e0; }

    /* === 封面页 === */
    .hero-header { background: #0a3dff; padding: 40px 32px 24px; text-align: center; color: #fff; }
    .hero-header .company-en { font-size: 11px; font-weight: 500; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 12px; }
    .hero-header .company-cn { font-size: 32px; font-weight: 900; margin-bottom: 8px; word-break: break-all; }
    .hero-header .hero-subtitle { font-size: 28px; font-weight: 700; margin-bottom: 24px; }
    .hero-header .meta-bar { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }
    .hero-header .meta-pill { display: inline-block; padding: 6px 16px; border-radius: 20px; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); font-size: 12px; color: rgba(255,255,255,0.9); }
    .hero-header .hero-hint { font-size: 12px; color: rgba(255,255,255,0.85); line-height: 1.6; max-width: 800px; margin: 0 auto; }

    /* === 页签导航 === */
    .tab-nav { position: sticky; top: 0; z-index: 1000; background: #fff; border-bottom: 1px solid #e0e0e0; display: flex; justify-content: center; gap: 4px; padding: 0 16px; }
    .tab-nav-item { padding: 12px 20px; font-size: 13px; color: #666; cursor: pointer; border: none; background: none; border-bottom: 2px solid transparent; transition: all 0.2s; font-weight: 500; white-space: nowrap; }
    .tab-nav-item:hover { color: #0a3dff; background: #f0f3ff; }
    .tab-nav-item.active { color: #0a3dff; border-bottom-color: #0a3dff; font-weight: 600; }
    .tab-content { display: none; }

    /* === KPI === */
    .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0; }
    .kpi-grid.patent-stats .kpi-card:nth-last-child(1),
    .kpi-grid.patent-stats .kpi-card:nth-last-child(2) { grid-column: span 2; }
    .kpi-card { background: #fff; border-radius: 8px; padding: 14px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    .kpi-label { font-size: 11px; color: #999; margin-bottom: 6px; }
    .kpi-value { font-size: 16px; font-weight: 700; color: #1a1a1a; }
    .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0; }
    .kpi-row .kpi-big { background: #fff; border-radius: 8px; padding: 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    .kpi-row .kpi-big .num { font-size: 28px; font-weight: 700; }
    .kpi-row .kpi-big .label { font-size: 12px; color: #999; margin-top: 4px; }

    /* === 增长曲线卡片 === */
    .curve-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 16px 0; }
    .curve-card { background: #fff; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border-top: 3px solid; }
    .curve-card.blue { border-top-color: #0a3dff; }
    .curve-card.green { border-top-color: #0fcc7a; }
    .curve-card.yellow { border-top-color: #ffaa00; }

    /* === 三梯队卡片 === */
    .tier-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 16px 0; }
    .tier-card { background: #fff; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    .tier-card.positive { border-top: 3px solid #0a3dff; }
    .tier-card.accent { border-top: 3px solid #0fcc7a; }
    .tier-card.graybox { border-top: 3px solid #ffaa00; }

    /* === 三级缺口卡片 === */
    .gap-cards { margin: 16px 0; }
    .gap-card { background: #fff; padding: 16px; border-radius: 8px; margin: 12px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    .gap-card.urgent { border-top: 3px solid #e74c3c; }
    .gap-card.important { border-top: 3px solid #ffaa00; }
    .gap-card.opportunity { border-top: 3px solid #0a3dff; }

    /* === 进度条 === */
    .cover-bar { width: 100%; height: 8px; background: #eee; border-radius: 4px; overflow: hidden; }
    .cover-fill { height: 100%; border-radius: 4px; }

    /* === 时间线 === */
    .timeline { position: relative; padding-left: 24px; }
    .timeline::before { content: ''; position: absolute; left: 7px; top: 0; bottom: 0; width: 2px; background: #0a3dff; }
    .timeline-item { position: relative; margin-bottom: 20px; }
    .timeline-item::before { content: ''; position: absolute; left: -21px; top: 4px; width: 14px; height: 14px; border-radius: 50%; background: #0a3dff; }
    .timeline-item:last-child::before { background: #0fcc7a; }

    /* === SWOT === */
    .swot-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 16px 0; }
    .swot-card { background: #fff; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }

    /* === 三栏建议 === */
    .three-col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin: 16px 0; }

    /* === 双栏 === */
    .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }

    /* === 技术前瞻双栏 === */
    .trend-col-grow { background: #fff; border-left: 4px solid #0fcc7a; padding: 16px; border-radius: 0 8px 8px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    .trend-col-decline { background: #fff; border-left: 4px solid #e74c3c; padding: 16px; border-radius: 0 8px 8px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }

    /* === 专利运营/产品链/产业链 侧边线卡片 === */
    .side-green { background: #fff; border-left: 3px solid #0fcc7a; padding: 12px 16px; border-radius: 0 6px 6px 0; margin: 12px 0; }
    .side-blue { background: #fff; border-left: 3px solid #0a3dff; padding: 12px 16px; border-radius: 0 6px 6px 0; margin: 12px 0; }

    /* === 报告综述 === */
    .report-review { background: #d6e0ff; border-radius: 8px; padding: 20px; margin: 16px 0; }

    /* === 风险评分仪表盘 === */
    .score-gauge { background: #fff; border-radius: 8px; padding: 20px; margin: 16px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    .score-bar { width: 100%; height: 8px; background: #eee; border-radius: 4px; overflow: hidden; }
    .score-fill { height: 100%; border-radius: 4px; }

    /* === 双栏待办 === */
    .action-ip { background: linear-gradient(135deg, rgba(10,61,255,0.10) 0%, rgba(255,255,255,0) 100%); border-radius: 8px; padding: 16px; border-left: 4px solid #0a3dff; }
    .action-rd { background: linear-gradient(135deg, rgba(15,204,122,0.10) 0%, rgba(255,255,255,0) 100%); border-radius: 8px; padding: 16px; border-left: 4px solid #0fcc7a; }

    /* === Badge === */
    .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }
    .badge-green { background: #e6f9f0; color: #0fcc7a; }
    .badge-blue { background: #e6eeff; color: #0a3dff; }
    .badge-yellow { background: #fff5e6; color: #ffaa00; }
    .badge-red { background: #ffe6e6; color: #e74c3c; }

    /* === 产品系列卡片 === */
    .product-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; margin: 16px 0; }
    .product-card { background: #fff; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }

    /* === 策略标签 === */
    .strategy-strengthen { color: #0fcc7a; }
    .strategy-layout { color: #0a3dff; }
    .strategy-catchup { color: #ffaa00; }

    /* === 【新增】价值分布热力图 - 星级表格（第八节） === */
    .heatmap-star-table { width: 100%; border-collapse: collapse; margin: 16px 0; }
    .heatmap-star-table th { background: #0a3dff; color: #fff; padding: 12px 16px; text-align: left; font-size: 13px; }
    .heatmap-star-table td { padding: 12px 16px; border-bottom: 1px solid #f0f0f0; font-size: 13px; vertical-align: middle; }
    .heatmap-star-table tr:nth-child(even) { background: #fafbfc; }
    .star-blue { color: #0a3dff; font-size: 16px; letter-spacing: 2px; }
    .star-gray { color: #D9D9D9; font-size: 16px; letter-spacing: 2px; }

    /* === 【新增】三级缺口卡片 - 带圆点标题（第十节） === */
    .gap-title { font-size: 15px; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
    .dot-red { width: 12px; height: 12px; background: #e74c3c; border-radius: 50%; display: inline-block; flex-shrink: 0; }
    .dot-yellow { width: 12px; height: 12px; background: #ffaa00; border-radius: 50%; display: inline-block; flex-shrink: 0; }
    .dot-blue { width: 12px; height: 12px; background: #0a3dff; border-radius: 50%; display: inline-block; flex-shrink: 0; }
    .gap-item { margin: 12px 0; padding: 10px 0; border-bottom: 1px dashed #f0f0f0; }
    .gap-item:last-child { border-bottom: none; }
    .gap-item strong { color: #333; }

    /* === 【新增】风险评分仪表盘 - 渐变条+指示器（第十三节） === */
    .score-bar-gradient { width: 100%; height: 16px; background: linear-gradient(to right, #e74c3c 0%, #e74c3c 25%, #ffaa00 50%, #0fcc7a 75%, #0fcc7a 100%); border-radius: 8px; position: relative; margin: 16px 0; }
    .score-indicator { width: 24px; height: 24px; border: 4px solid #333; border-radius: 50%; background: #fff; position: absolute; top: -6px; transform: translateX(-50%); box-shadow: 0 2px 4px rgba(0,0,0,0.3); z-index: 10; }
    .score-section-header { background: #0a3dff; color: #fff; padding: 12px 16px; font-weight: 700; font-size: 14px; border-radius: 6px 6px 0 0; }
    .score-section-body { border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 6px 6px; padding: 12px 16px; }
    .score-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 13px; }
    .score-row:last-child { border-bottom: none; }
    .score-val-red { color: #e74c3c; font-weight: 700; }
    .score-val-green { color: #0fcc7a; font-weight: 700; }
    .score-val-yellow { color: #ffaa00; font-weight: 700; }
    .score-total-row { background: #0a3dff; color: #fff; font-weight: 700; padding: 10px 16px; border-radius: 0 0 6px 6px; display: flex; justify-content: space-between; }

    /* === 【新增】海外布局建议版块（第十三节） === */
    .overseas-advice { background: #f0f3ff; border-radius: 8px; padding: 20px; margin: 16px 0; border-left: 4px solid #0a3dff; }
    .overseas-advice h4 { color: #0a3dff; margin: 0 0 12px 0; font-size: 15px; }

    /* === 【新增】发明人排行双Y轴图容器 === */
    .chart-inventor-dual { width: 100%; box-sizing: border-box; background: #fff; border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); margin: 16px 0; }
    .chart-inventor-dual img { max-width: 100%; height: auto; }
  </style>
</head>
<body>

<!-- ==================== 封面页 ==================== -->
<div class="hero-header">
  <div class="company-en">{{company_en}}</div>
  <div class="company-cn">{{company_cn}}</div>
  <div class="hero-subtitle">&#9679; 企业战略专利分析报告</div>
  <div class="meta-bar">
    <span class="meta-pill">报告日期：{{report_date}}</span>
    <span class="meta-pill">数据来源：{{data_source}}</span>
    <span class="meta-pill">分析范围：企业全球专利</span>
    <span class="meta-pill">分析工具：Eureka AI平台</span>
  </div>
  <div class="hero-hint">建议：人工提供企业产品立项书、研发计划、出口市场清单等信息，可显著提升报告针对性和实用性。本报告基于{{data_source_hint}}，全量专利以平台导出为准。</div>
</div>

<!-- ==================== 页签导航 ==================== -->
<nav class="tab-nav">
  <button class="tab-nav-item active" data-tab="tab-overview" onclick="switchTab('tab-overview')">企业概览</button>
  <button class="tab-nav-item" data-tab="tab-business" onclick="switchTab('tab-business')">业务与技术</button>
  <button class="tab-nav-item" data-tab="tab-assets" onclick="switchTab('tab-assets')">资产与价值</button>
  <button class="tab-nav-item" data-tab="tab-mapping" onclick="switchTab('tab-mapping')">映射与缺口</button>
  <button class="tab-nav-item" data-tab="tab-team" onclick="switchTab('tab-team')">团队与海外</button>
  <button class="tab-nav-item" data-tab="tab-strategy" onclick="switchTab('tab-strategy')">战略与优化</button>
  <button class="tab-nav-item" data-tab="tab-action" onclick="switchTab('tab-action')">行动建议</button>
</nav>

<!-- ==================== 页签1：企业概览 ==================== -->
<div id="tab-overview" class="tab-content">
  <div class="main-content">

<!-- SECTION_1: 企业全景概述与核心KPI -->
<!-- 填充规范见 section_specs.md #第一节 -->
<!-- /SECTION_1 -->

<!-- SECTION_2: 企业基本信息与名称变体检索清单 -->
<!-- 填充规范见 section_specs.md #第二节 -->
<!-- /SECTION_2 -->

  </div>
</div>

<!-- ==================== 页签2：业务与技术 ==================== -->
<div id="tab-business" class="tab-content" style="display:none">
  <div class="main-content">

<!-- SECTION_3: 企业业务与营收曲线分析 -->
<!-- 填充规范见 section_specs.md #第三节 -->
<!-- /SECTION_3 -->

<!-- SECTION_4: 技术演进路径与竞争情报 -->
<!-- 填充规范见 section_specs.md #第四节 -->
<!-- /SECTION_4 -->

<!-- SECTION_5: 产业技术链梯队分析 -->
<!-- 填充规范见 section_specs.md #第五节 -->
<!-- /SECTION_5 -->

<!-- SECTION_6: 产品技术分类 -->
<!-- 填充规范见 section_specs.md #第六节 -->
<!-- /SECTION_6 -->

  </div>
</div>

<!-- ==================== 页签3：资产与价值 ==================== -->
<div id="tab-assets" class="tab-content" style="display:none">
  <div class="main-content">

<!-- SECTION_7: 专利组合全景分析 -->
<!-- 填充规范见 section_specs.md #第七节 -->
<!-- /SECTION_7 -->

<!-- SECTION_8: 专利价值分层与代表性专利 -->
<!-- 填充规范见 section_specs.md #第八节 -->
<!-- /SECTION_8 -->

  </div>
</div>

<!-- ==================== 页签4：映射与缺口 ==================== -->
<div id="tab-mapping" class="tab-content" style="display:none">
  <div class="main-content">

<!-- SECTION_9: 专利与营收曲线匹配分析 -->
<!-- 填充规范见 section_specs.md #第九节 -->
<!-- /SECTION_9 -->

<!-- SECTION_10: 专利布局缺口分析 -->
<!-- 填充规范见 section_specs.md #第十节 -->
<!-- /SECTION_10 -->

  </div>
</div>

<!-- ==================== 页签5：团队与海外 ==================== -->
<div id="tab-team" class="tab-content" style="display:none">
  <div class="main-content">

<!-- SECTION_11: 核心发明人与研发团队分析 -->
<!-- 填充规范见 section_specs.md #第十一节 -->
<!-- /SECTION_11 -->

<!-- SECTION_12: 近期技术方向前瞻 -->
<!-- 填充规范见 section_specs.md #第十二节 -->
<!-- /SECTION_12 -->

<!-- SECTION_13: 海外专利与抗风险能力评估 -->
<!-- 填充规范见 section_specs.md #第十三节 -->
<!-- /SECTION_13 -->

  </div>
</div>

<!-- ==================== 页签6：战略与优化 ==================== -->
<div id="tab-strategy" class="tab-content" style="display:none">
  <div class="main-content">

<!-- SECTION_14: 降本优化 -->
<!-- 填充规范见 section_specs.md #第十四节 -->
<!-- /SECTION_14 -->

<!-- SECTION_15: 近期新产品专利布局策略 -->
<!-- 填充规范见 section_specs.md #第十五节 -->
<!-- /SECTION_15 -->

<!-- SECTION_16: SWOT分析与专利运营建议 -->
<!-- 填充规范见 section_specs.md #第十六节 -->
<!-- /SECTION_16 -->

<!-- SECTION_17: 产品链与产业链发展策略 -->
<!-- 填充规范见 section_specs.md #第十七节 -->
<!-- /SECTION_17 -->

<!-- SECTION_18: 分阶段专利补全计划 -->
<!-- 填充规范见 section_specs.md #第十八节 -->
<!-- /SECTION_18 -->

<!-- SECTION_19: 平台使用场景建议 -->
<!-- 填充规范见 section_specs.md #第十九节 -->
<!-- /SECTION_19 -->

  </div>
</div>

<!-- ==================== 页签7：行动建议 ==================== -->
<div id="tab-action" class="tab-content" style="display:none">
  <div class="main-content">

<!-- SECTION_20: 知识产权行动建议汇总 -->
<!-- 填充规范见 section_specs.md #第二十节 -->
<!-- /SECTION_20 -->

<!-- SECTION_21: 报告综述（第二十节子元素，不单独编号） -->
<!-- 填充规范见 section_specs.md #报告综述 -->
<!-- /SECTION_21 -->

  </div>
</div>

<script>
function switchTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
  document.querySelectorAll('.tab-nav-item').forEach(el => el.classList.remove('active'));
  document.getElementById(tabId).style.display = 'block';
  document.querySelector('[data-tab="' + tabId + '"]').classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
switchTab('tab-overview');
</script>
</body>
</html>
```

**模板变量说明**：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `{{company_en}}` | 英文公司名 | SHANGHAI KINETIC MEDICAL CO., LTD. |
| `{{company_cn}}` | 中文公司名 | 上海凯利泰医疗科技股份有限公司 |
| `{{report_date}}` | 报告日期 | 2025年05月26日 |
| `{{data_source}}` | 数据来源 | 用户提供专利清单 / PatSnap智慧芽 |
| `{{data_source_hint}}` | 数据来源提示 | PatSnap样本数据 / 用户提供清单 |
