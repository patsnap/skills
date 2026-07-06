# 专利报告规格

## 链接规则

使用前端可接收 MCP 返回实体 ID 的实体详情 URL 模式。

重要：不要将 MCP 实体 UUID 放入 `*-list?query_id=...` 路由。这些列表路由需要前端搜索/列表 query ID，而不是实体 UUID，否则会生成不可用页面或 404。Patent Analytics 是例外：`patentId=<patent_id>` 直接接受 MCP 专利 UUID。

| 实体 | URL 模式 |
| --- | --- |
| 药物 | `https://synapse.zhihuiya.com/drug/<drug_id>` |
| 药物交易 | 优先使用 `ls_drug_deal_search` / `ls_drug_deal_fetch` 返回的 `url`；如果没有可用来源 URL，不要编造列表 URL。 |
| 新闻 | 当 MCP 返回 Synapse 新闻 URL 时使用 `https://synapse.zhihuiya.com/news-detail/<news_uuid>`；否则使用返回的来源 URL。 |
| 临床试验 | `https://synapse.zhihuiya.com/clinical-progress-detail/<clinical_trial_id>` |
| 临床结果 | `https://synapse.zhihuiya.com/clinical-result-detail/<ct_result_id>` |
| 转化医学 | 优先使用 `ls_translational_medicine_search` / fetch 返回的 `url`；许多记录会解析到文献详情或来源 URL。 |
| 文献 | `https://synapse.zhihuiya.com/literature-detail/<paper_id>` |
| 专利 | `https://analytics.zhihuiya.com/patent-view/abst?patentId=<patent_id>` |

永远不要将 PN、NCT 号、标题、公司名或显示名称放入 `query_id` 或 `patentId`。

## V6 HTML 风格

使用以下约定：

- `html lang="zh-CN" data-theme="light"`。
- Sticky `.topbar`，包含紧凑 `.nav` 锚点和主题切换。
- `header#overview`，然后交替使用 `section` 和 `section.s-band`。
- `.wrap` 最大宽度约 1440px。
- `.grid.g5/.g4/.g3/.g2` 搭配 `.metric` 卡片。
- `.callout` 变体：default、`.amber`、`.red`、`.green`、`.orange`、`.gray`、`.violet`。
- 表格放在 `<div class="tw"><table>...</table></div>` 中。
- 来源链接使用 `.zchip`。
- 序列使用 `.seq`。
- 附图引用使用 `.iref`。

保持报告的分析性和信息密度。不要使用 landing-page hero 布局。

## 推荐章节

1. 概览/header，包含核心论点和指标。
2. 专利核心信息：PN、标题、申请人、申请/优先权/公开日期、法律状态提示、IPC/CPC、权利要求。
3. 靶点或技术背景。
4. 权利要求/序列/scaffold/payload 分析。
5. 实验数据：亲和力、DAR/SEC、IC50、TGI、安全性、实施例。
6. 管线和临床格局。
7. 临床结果/读出。
8. 专利格局和 FTO 风险。
9. 文献/转化证据。
10. BD 交易和新闻。
11. 专利附图索引。
12. 来源/查询溯源和链接审计说明。

## 可悬浮附图引用

在证据出现的位置使用内联链接：

```html
<a class="iref"
   href="assets/<project>/<image>.png"
   data-img="assets/<project>/<image>.png"
   data-cap="I100160 · HT55 D35 TGI 表"
   target="_blank">图 I100160</a>
```

添加 CSS：

```css
.iref{display:inline-flex;align-items:center;gap:2px;padding:1px 6px;border-radius:8px;border:1px dashed var(--amber);font-size:10px;color:var(--amber);background:var(--amber-bg);text-decoration:none;white-space:nowrap;margin:1px;vertical-align:middle}
.iref:hover,.iref:focus{background:var(--amber);color:#fff;text-decoration:none;outline:none}
#img-float{display:none;position:fixed;z-index:9999;pointer-events:none;width:420px;max-width:min(420px,92vw);background:var(--bg);border:1px solid var(--line);border-radius:10px;box-shadow:0 10px 40px rgba(0,0,0,.28);overflow:hidden}
#img-float img{display:block;width:100%;max-height:62vh;object-fit:contain;background:#fff}
#img-float .fcap{padding:6px 9px;font-size:10.5px;color:var(--ink2);border-top:1px solid var(--line);background:var(--bg2)}
```

在 `<body>` 末尾附近添加一次 JS：

```html
<script>
(function(){
  const float=document.createElement("div");
  float.id="img-float";
  float.innerHTML='<img alt=""><div class="fcap"></div>';
  document.body.appendChild(float);
  const img=float.querySelector("img"), cap=float.querySelector(".fcap");
  function positionFloat(e){
    const pad=14, off=16, w=window.innerWidth, h=window.innerHeight;
    const fw=float.offsetWidth||420, fh=float.offsetHeight||300;
    let x=e.clientX+off, y=e.clientY-fh/2;
    if(x+fw+pad>w)x=e.clientX-fw-off;
    if(y+fh+pad>h)y=h-fh-pad;
    if(y<pad)y=pad;
    if(x<pad)x=pad;
    float.style.left=x+"px";
    float.style.top=y+"px";
  }
  document.querySelectorAll(".iref").forEach(ref=>{
    ref.addEventListener("mouseenter",e=>{
      img.src=ref.dataset.img||ref.href;
      cap.textContent=ref.dataset.cap||ref.textContent.trim();
      float.style.display="block";
      positionFloat(e);
    });
    ref.addEventListener("mousemove",positionFloat);
    ref.addEventListener("mouseleave",()=>{float.style.display="none";});
  });
})();
</script>
```

## 校验命令

从仓库根目录执行：

```bash
python3 -m html.parser reports/<new-report>.html
rg -n "patentId=(WO|US|CN|EP)|query_id=(WO|US|CN|EP|NCT)|patent-view/abst\?patentId=[A-Z]" reports/<new-report>.html
rg -o 'data-img="[^"]+"|<img src="[^"]+"' reports/<new-report>.html
```

对于本地图片，确认引用文件存在于 `reports/assets/<project>/` 下。
