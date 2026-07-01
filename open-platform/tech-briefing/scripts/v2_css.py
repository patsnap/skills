# -*- coding: utf-8 -*-
"""技术简报 V2 报告样式。build_report_v2.py 会引用 CSS 变量。"""

CSS = r"""
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
               "Microsoft YaHei", sans-serif;
  background: #fafafa; color: #1a1a1a; line-height: 1.7;
  padding: 40px 320px 40px 60px;
}
a { color: #1b5cd8; }

/* 报告标题 */
.report-header {
  text-align: center; margin-bottom: 48px; padding-bottom: 24px;
  border-bottom: 1px solid #eee;
}
.report-title { font-size: 32px; font-weight: 600; margin-bottom: 12px; }
.report-badge {
  display: inline-block; padding: 4px 12px; background: #e6f0ff;
  color: #1b5cd8; border-radius: 12px; font-size: 13px;
}

/* 段落 */
section { margin-bottom: 48px; scroll-margin-top: 24px; }
h2 {
  font-size: 22px; border-left: 4px solid #1b5cd8;
  padding-left: 12px; margin-bottom: 20px;
}
h3 { font-size: 18px; margin: 24px 0 12px; color: #333; }
p.empty { color: #999; padding: 16px; background: #fafafa; border-radius: 6px; }

/* 右侧导航 */
.nav-panel {
  position: fixed; right: 24px; top: 40px; width: 240px;
  background: #fff; border: 1px solid #eee; border-radius: 8px;
  padding: 16px; max-height: calc(100vh - 80px); overflow-y: auto;
  font-size: 14px;
}
.nav-panel a {
  display: block; padding: 6px 10px; color: #555;
  text-decoration: none; border-radius: 4px;
}
.nav-panel a:hover { background: #f0f5ff; color: #1b5cd8; }
.nav-panel a.sub { padding-left: 20px; font-size: 13px; color: #888; }

/* 词云 */
.word-cloud {
  display: flex; flex-wrap: wrap; gap: 12px 18px; padding: 20px;
  background: #f7f9fc; border-radius: 8px; align-items: baseline;
}
.word-cloud span { cursor: help; transition: opacity 0.15s; }
.word-cloud span:hover { opacity: 0.65; }

/* 柱状图 */
.bar-chart {
  display: flex; align-items: flex-end; gap: 16px;
  height: 220px; padding: 16px 0;
}
.bar { flex: 1; display: flex; flex-direction: column; align-items: center; }
.bar .fill {
  width: 100%;
  background: linear-gradient(to top, #1b5cd8, #6a9eff);
  border-radius: 4px 4px 0 0; min-height: 4px;
}
.bar .label { margin-top: 8px; font-size: 13px; color: #555; }
.bar .count { font-size: 12px; color: #888; margin-bottom: 4px; }

/* 趋势 SVG */
.trend-svg {
  width: 100%; height: 260px; background: #fff;
  border: 1px solid #eef; border-radius: 8px; padding: 10px;
  margin-bottom: 16px;
}

/* 专利手风琴 */
.accordion-group {
  margin-bottom: 16px; border: 1px solid #e5e9f0;
  border-radius: 8px; overflow: hidden;
}
.accordion-header {
  background: linear-gradient(to right, #1b5cd8, #3f7de0);
  color: white; padding: 14px 18px; cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
  user-select: none;
}
.accordion-header .caret { transition: transform 0.2s; }
.accordion-header[aria-expanded="true"] .caret { transform: rotate(90deg); }
.accordion-body { padding: 16px 18px; display: none; background: #fff; }
.accordion-body.open { display: block; }

/* 专利卡片 */
.patent-card {
  padding: 14px; border: 1px solid #eef; border-radius: 6px;
  margin-bottom: 12px; background: #fdfdff;
}
.patent-card .pn {
  color: #1b5cd8; text-decoration: none; font-weight: 500;
  margin-right: 8px;
}
.patent-card .pn:hover { text-decoration: underline; }
.patent-card .meta { font-size: 13px; color: #888; margin: 6px 0 10px; }

/* 标签 */
.tag {
  display: inline-block; padding: 2px 8px; border-radius: 4px;
  font-size: 12px; margin-right: 6px; vertical-align: middle;
}
.tag.problem { background: #fde8e8; color: #c23434; }
.tag.approach { background: #e7f4e7; color: #2d8b3b; }
.tag.effect { background: #fff3e0; color: #d07b1b; }
.tag.status-valid { background: #e7f4e7; color: #2d8b3b; }
.tag.status-pending { background: #fff3e0; color: #d07b1b; }
.tag.status-expired { background: #fde8e8; color: #c23434; }

/* 三要素 */
.tech-field { margin: 6px 0; font-size: 14px; }

/* 新闻卡片 */
.news-card {
  padding: 14px 16px; border: 1px solid #eee;
  border-radius: 6px; margin-bottom: 10px;
}
.news-card a { color: #1a1a1a; text-decoration: none; font-weight: 500; }
.news-card a:hover { color: #1b5cd8; }
.news-card .desc { font-size: 14px; color: #555; margin-top: 6px; }
.news-card .source { font-size: 12px; color: #999; margin-top: 4px; }

/* 文献 */
.lit-item {
  padding: 12px 0; border-bottom: 1px dashed #eee;
}
.lit-item:last-child { border-bottom: 0; }
.lit-item a { text-decoration: none; font-weight: 500; }
.lit-item a:hover { text-decoration: underline; }
.lit-item .meta { font-size: 13px; color: #888; margin: 4px 0; }

/* 子技术 */
.subtech {
  margin-bottom: 10px; border: 1px solid #eef; border-radius: 6px;
  overflow: hidden;
}
.subtech-header {
  padding: 12px 16px; cursor: pointer;
  display: flex; justify-content: space-between;
  background: #f7f9fc; user-select: none;
}
.subtech-header:hover { background: #eef3fa; }
.subtech-body { display: none; padding: 12px 16px; background: #fff; }
.subtech-body.open { display: block; }

/* 响应式 */
@media (max-width: 1080px) {
  body { padding: 24px; }
  .nav-panel { display: none; }
}
"""
