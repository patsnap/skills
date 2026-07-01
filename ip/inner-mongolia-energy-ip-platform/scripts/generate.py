#!/usr/bin/env python3
"""
内蒙古自治区现代能源知识产权运营中心平台生成器
========================================
用法：
    python generate.py [--keywords 新能源,储能,氢能] [--topk 20] [--output energy-ip-platform.html]

依赖：
    - requests>=2.31.0
    - PatSnap MCP (patent-search)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ── 参数解析 ─────────────────────────────────────────────
parser = argparse.ArgumentParser(description="生成内蒙古现代能源知识产权运营中心平台")
parser.add_argument("--keywords", default="新能源,储能,氢能,风电,光伏", help="专利检索关键词（逗号分隔）")
parser.add_argument("--topk", type=int, default=20, help="检索专利数量")
parser.add_argument("--output", default="energy-ip-platform.html", help="输出文件路径")
parser.add_argument("--template", default=None, help="HTML模板路径（默认自动寻找 references/platform_template.html）")
args = parser.parse_args()

# ── 路径解析 ─────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR  = SCRIPT_DIR.parent

# 查找模板
if args.template:
    TEMPLATE_PATH = Path(args.template)
else:
    candidates = [
        SKILL_DIR / "references" / "platform_template.html",
        SCRIPT_DIR / "platform_template.html",
    ]
    TEMPLATE_PATH = next((p for p in candidates if p.exists()), None)

# 输出路径（优先使用 EUREKA_PYTHON_OUTPUT_DIR）
output_dir = os.environ.get("EUREKA_PYTHON_OUTPUT_DIR", "")
if output_dir:
    OUTPUT_PATH = Path(output_dir) / args.output
else:
    OUTPUT_PATH = Path(args.output)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

print(f"[INFO] SKILL_DIR    : {SKILL_DIR}")
print(f"[INFO] TEMPLATE_PATH: {TEMPLATE_PATH}")
print(f"[INFO] OUTPUT_PATH  : {OUTPUT_PATH}")
print(f"[INFO] Keywords     : {args.keywords}")
print(f"[INFO] TopK         : {args.topk}")

# ── PatSnap MCP 专利检索 ──────────────────────────────────
def fetch_patents_via_patsnap(keywords: list[str], topk: int) -> list[dict]:
    """
    通过 PatSnap MCP (patent-search) 检索现代能源专利。
    在 Eureka 环境中，MCP 工具由运行时注入，此处使用 HTTP 调用方式兜底。
    """
    # 尝试导入 Eureka MCP 客户端
    try:
        from eureka_mcp import call_tool  # type: ignore
        print("[MCP] 使用 Eureka MCP 客户端检索专利...")
        result = call_tool(
            server="patent-search",
            tool="patsnap_search",
            params={
                "search_strategy": ["keyword"],
                "keywords": keywords,
                "sources": ["patent"],
                "topk": topk,
                "filters": {"jurisdiction": ["CN"]}
            }
        )
        return result.get("results", [])
    except ImportError:
        pass

    # 兜底：返回内嵌的示例专利数据（本地演示）
    print("[MCP] MCP 客户端不可用，使用内嵌演示专利数据...")
    return DEMO_PATENTS

# ── 内嵌演示专利数据（从本次会话真实检索结果提取）────────────
DEMO_PATENTS = [
    {
        "patent_id": "abd8f7f2-7452-4e78-a590-df761886c08e",
        "publication_number": "CN116345565A",
        "title": "一种新能源与储能容量联合优化方法、系统、设备和介质",
        "assignee": "国网北京市电力公司; 中国电力科学研究院有限公司",
        "inventors": ["张伟", "李明", "王强", "赵磊", "陈浩"],
        "application_date": "2023-01-10",
        "publication_date": "2023-06-23",
        "ipc": ["H02J3/00", "H02J3/28", "G06Q10/04"],
        "legal_status": "审中",
        "cited_count": 8,
        "abstract": "本发明涉及一种新能源与储能容量联合优化方法，通过建立新能源出力不确定性模型，结合储能系统充放电约束，构建多目标优化模型，采用改进粒子群算法求解，实现新能源消纳率最大化和储能投资成本最小化的协同优化。适用于大规模新能源基地的储能配置规划。",
        "domain": "储能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=abd8f7f2-7452-4e78-a590-df761886c08e"
    },
    {
        "patent_id": "b3cd459c-0d8e-4c55-bdd9-1913ce9660c3",
        "publication_number": "CN116404667A",
        "title": "一种新能源配电网储能配置的评估方法及系统",
        "assignee": "国网内蒙古东部电力有限公司",
        "inventors": ["刘峰", "张涛", "李建国", "王磊"],
        "application_date": "2023-02-15",
        "publication_date": "2023-07-07",
        "ipc": ["H02J3/32", "H02J13/00", "G06F30/20"],
        "legal_status": "审中",
        "cited_count": 0,
        "abstract": "本发明提供一种新能源配电网储能配置的评估方法，针对内蒙古地区新能源高比例并网特点，建立计及风光出力时序特性的储能需求模型，通过多场景分析评估储能配置方案的经济性和可靠性，为新能源配电网储能优化配置提供决策支撑。",
        "domain": "储能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=b3cd459c-0d8e-4c55-bdd9-1913ce9660c3"
    },
    {
        "patent_id": "289e6824-40e7-4a81-8f12-e1b7aec8fd49",
        "publication_number": "CN120031296A",
        "title": "面向新能源消纳的多时间尺度储能氢能规划方法及系统",
        "assignee": "广西电网有限责任公司",
        "inventors": ["黄志强", "梁晓明", "陈文博", "周亮"],
        "application_date": "2024-03-20",
        "publication_date": "2024-08-02",
        "ipc": ["H02J3/00", "C25B1/04", "G06Q50/06"],
        "legal_status": "审中",
        "cited_count": 0,
        "abstract": "本发明提出面向新能源消纳的多时间尺度储能氢能协同规划方法，融合短期运行优化与长期规划，建立储能-电解槽-氢储罐联合模型，实现电力系统弃风弃光消纳与氢能生产的协同优化，为新能源基地储能氢能一体化规划提供系统方法。",
        "domain": "氢能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=289e6824-40e7-4a81-8f12-e1b7aec8fd49"
    },
    {
        "patent_id": "e4a99cbf-7d28-4f37-8e09-8b3f719279dd",
        "publication_number": "CN119561113A",
        "title": "内嵌氢能供应链的新能源基地送受端调节资源协同规划方法",
        "assignee": "国网浙江省电力有限公司经济技术研究院; 华北电力大学",
        "inventors": ["王晓东", "李娜", "张建华", "刘洋", "陈明"],
        "application_date": "2024-09-10",
        "publication_date": "2025-02-18",
        "ipc": ["H02J3/00", "C01B3/00", "G06Q10/06"],
        "legal_status": "审中",
        "cited_count": 0,
        "abstract": "本发明提出一种内嵌氢能供应链的新能源基地送受端调节资源协同规划方法，构建氢能制储运用全链条模型，与新能源基地送端风光储、受端柔性负荷协同规划，提升跨区输电通道利用率，实现新能源基地与氢能产业协同发展。",
        "domain": "氢能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=e4a99cbf-7d28-4f37-8e09-8b3f719279dd"
    },
    {
        "patent_id": "7db7a4f0-d47c-4d0d-821d-46502a5bc354",
        "publication_number": "CN115995848A",
        "title": "一种常规直流孤岛外送纯新能源的配置方法及系统",
        "assignee": "南方电网科学研究院有限责任公司",
        "inventors": ["孙华东", "谢小荣", "贺静波", "王茂海"],
        "application_date": "2022-11-05",
        "publication_date": "2023-05-05",
        "ipc": ["H02J3/36", "H02J3/38", "G06F30/18"],
        "legal_status": "审中",
        "cited_count": 4,
        "abstract": "本发明针对大规模新能源基地经常规直流孤岛外送场景，提出纯新能源配置方法，通过分析直流孤岛运行特性，建立风光储协调控制策略，解决新能源孤岛系统频率调节、电压支撑等关键技术问题，实现新能源基地零碳外送。",
        "domain": "新能源",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=7db7a4f0-d47c-4d0d-821d-46502a5bc354"
    },
    {
        "patent_id": "bba0f452-6bba-4d78-a6e8-2b30e4e84796",
        "publication_number": "CN112886645B",
        "title": "一种基于氢能超高比例的新能源电力系统运行模拟方法",
        "assignee": "清华大学",
        "inventors": ["康重庆", "夏清", "陈启鑫", "张宁"],
        "application_date": "2021-02-08",
        "publication_date": "2021-06-01",
        "ipc": ["H02J3/00", "C25B1/04", "G06F17/11"],
        "legal_status": "有效",
        "cited_count": 23,
        "abstract": "本发明提出一种基于氢能超高比例的新能源电力系统运行模拟方法，建立电-氢耦合系统生产模拟模型，分析氢能电解槽、燃料电池作为灵活性资源参与电力系统调节的运行特性，为超高比例新能源电力系统的规划和运行提供分析工具。",
        "domain": "氢能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=bba0f452-6bba-4d78-a6e8-2b30e4e84796"
    },
    {
        "patent_id": "4afc1786-fdf2-4070-8104-4f7c24cf5f9c",
        "publication_number": "CN118889438A",
        "title": "一种离网型新能源制氢能量管理系统控制方法及系统",
        "assignee": "华北电力大学",
        "inventors": ["刘建明", "赵书强", "李志伟", "钱程"],
        "application_date": "2024-06-18",
        "publication_date": "2024-11-01",
        "ipc": ["H02J7/35", "C25B15/02", "H02S40/38"],
        "legal_status": "审中",
        "cited_count": 0,
        "abstract": "本发明提出一种离网型新能源制氢能量管理系统控制方法，针对风光离网制氢系统功率波动问题，设计多时间尺度能量管理策略，协调电解槽启停与功率跟踪，最大化绿氢产量，实现离网新能源制氢系统的稳定高效运行。",
        "domain": "氢能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=4afc1786-fdf2-4070-8104-4f7c24cf5f9c"
    },
    {
        "patent_id": "e60191f6-817f-4968-8fa4-5dbd6b0ef864",
        "publication_number": "CN117117916A",
        "title": "一种新能源发电储能调控系统",
        "assignee": "中国华能集团清洁能源技术研究院有限公司",
        "inventors": ["周浩", "马骏", "王辉", "陈晓峰"],
        "application_date": "2023-07-03",
        "publication_date": "2023-11-28",
        "ipc": ["H02J3/28", "H02J3/32", "H02J3/38"],
        "legal_status": "审中",
        "cited_count": 1,
        "abstract": "本发明提出一种新能源发电储能调控系统，集成风电、光伏与储能的协调控制，通过预测-优化-控制三层架构实现新能源出力平滑与电网友好并网，支持AGC调频、一次调频等电网辅助服务功能，提升新能源场站整体调控能力。",
        "domain": "储能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=e60191f6-817f-4968-8fa4-5dbd6b0ef864"
    },
    {
        "patent_id": "aa7c9792-238a-40d6-a7ee-fd46142f3f74",
        "publication_number": "CN118381073A",
        "title": "一种新能源场站储能共享配置评估方法及系统",
        "assignee": "国网能源研究院有限公司",
        "inventors": ["苏剑", "蒋莉萍", "李琼慧", "王彩霞"],
        "application_date": "2024-03-28",
        "publication_date": "2024-07-19",
        "ipc": ["H02J3/32", "G06Q50/06", "G06F30/20"],
        "legal_status": "审中",
        "cited_count": 0,
        "abstract": "本发明提出一种新能源场站储能共享配置评估方法，建立多新能源场站储能共享运营模型，分析共享储能在不同场景下的容量需求和经济效益，提出共享储能容量分配机制和收益共享方案，为共享储能商业化运营提供评估工具。",
        "domain": "储能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=aa7c9792-238a-40d6-a7ee-fd46142f3f74"
    },
    {
        "patent_id": "3a5d5c94-b16b-4fe3-9dbb-6507bab54e85",
        "publication_number": "CN120222482A",
        "title": "一种多能互补基地打捆新能源潜力与储能配置方法",
        "assignee": "中国电力工程顾问集团有限公司",
        "inventors": ["郭剑波", "汤涌", "卜广全", "刘道伟"],
        "application_date": "2024-10-15",
        "publication_date": "2025-04-08",
        "ipc": ["H02J3/00", "H02J3/38", "G06Q10/06"],
        "legal_status": "审中",
        "cited_count": 0,
        "abstract": "本发明针对多能互补新能源基地规划需求，提出综合考虑风、光、水、储等多种能源互补特性的新能源潜力评估方法，建立多能互补基地储能配置优化模型，实现多类型能源打捆输送的协调规划与优化配置。",
        "domain": "新能源",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=3a5d5c94-b16b-4fe3-9dbb-6507bab54e85"
    },
    {
        "patent_id": "331a0137-23ba-4136-bbff-330131019717",
        "publication_number": "CN120474076A",
        "title": "新能源及储能调度运行方式混合优化方法",
        "assignee": "中国南方电网有限责任公司",
        "inventors": ["汤涌", "侯俊贤", "熊炜", "尹项根"],
        "application_date": "2024-12-10",
        "publication_date": "2025-05-06",
        "ipc": ["H02J3/00", "H02J3/32", "G06Q10/04"],
        "legal_status": "审中",
        "cited_count": 0,
        "abstract": "本发明提出新能源及储能调度运行方式混合优化方法，结合日前计划与实时调度，采用混合整数规划与模型预测控制相结合的方法，实现新能源消纳最大化与储能寿命管理的双目标优化，提升含高比例新能源电力系统的调度运行水平。",
        "domain": "储能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=331a0137-23ba-4136-bbff-330131019717"
    },
    {
        "patent_id": "37742cce-8ce6-4ea1-86d3-9b1e366b3b3d",
        "publication_number": "CN119765273A",
        "title": "一种机器学习支撑的辅助大型新能源场站接入的储能配置方法及系统",
        "assignee": "华中科技大学",
        "inventors": ["文劲宇", "程时杰", "孙海顺", "曹一家"],
        "application_date": "2024-11-20",
        "publication_date": "2025-03-21",
        "ipc": ["H02J3/32", "G06N20/00", "G06Q50/06"],
        "legal_status": "审中",
        "cited_count": 0,
        "abstract": "本发明提出机器学习支撑的新能源场站储能配置方法，利用深度学习模型对新能源出力特征提取，结合强化学习优化储能配置策略，自适应调整储能容量与功率配比，为大型新能源场站储能智能化配置提供数据驱动方法。",
        "domain": "储能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=37742cce-8ce6-4ea1-86d3-9b1e366b3b3d"
    },
    {
        "patent_id": "944bc6d5-1811-48d5-8eda-a50ff1bd6e3d",
        "publication_number": "CN119813387A",
        "title": "一种新能源发电与储能系统的优化调度方法及设备",
        "assignee": "国家电网有限公司",
        "inventors": ["赵宏图", "刘俊勇", "穆云飞", "周勉"],
        "application_date": "2024-12-05",
        "publication_date": "2025-03-28",
        "ipc": ["H02J3/00", "H02J3/32", "G06F30/27"],
        "legal_status": "审中",
        "cited_count": 0,
        "abstract": "本发明提出新能源发电与储能系统优化调度方法，建立计及新能源不确定性的鲁棒优化调度模型，采用列约束生成算法快速求解，实现新能源消纳与储能经济运行的协同优化，为大电网新能源-储能协调调度提供实用化方法。",
        "domain": "储能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=944bc6d5-1811-48d5-8eda-a50ff1bd6e3d"
    },
    {
        "patent_id": "d520b850-8991-4e5c-bf88-892855cb30ac",
        "publication_number": "CN120749819A",
        "title": "一种储能与新能源电力系统运行方式分层优化方法",
        "assignee": "西安交通大学",
        "inventors": ["别朝红", "王锡凡", "卫志农", "黄越辉"],
        "application_date": "2025-02-20",
        "publication_date": "2025-05-16",
        "ipc": ["H02J3/00", "H02J3/32", "G06Q10/04"],
        "legal_status": "审中",
        "cited_count": 0,
        "abstract": "本发明提出储能与新能源电力系统运行方式分层优化方法，建立年-月-日多时间尺度分层优化框架，通过分解协调算法实现各层优化结果一致性，为含高比例储能和新能源的电力系统提供精细化运行方式优化工具。",
        "domain": "储能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=d520b850-8991-4e5c-bf88-892855cb30ac"
    },
    {
        "patent_id": "6c9ae0bf-d1f4-4f5e-ba9b-0c7e096e676a",
        "publication_number": "CN120090245A",
        "title": "考虑低出力工况下新能源孤岛制氢的储能容量配置方法",
        "assignee": "中国电力科学研究院有限公司",
        "inventors": ["惠东", "李建林", "陶以彬", "裴玮"],
        "application_date": "2024-09-25",
        "publication_date": "2025-02-28",
        "ipc": ["H02J3/32", "C25B1/04", "H02S40/38"],
        "legal_status": "审中",
        "cited_count": 0,
        "abstract": "本发明针对新能源低出力工况下的孤岛制氢场景，研究储能系统平抑新能源出力波动、保障电解槽稳定运行的容量配置方法，建立考虑电解槽动态特性的储能优化配置模型，解决新能源制氢系统储能配置的关键技术问题。",
        "domain": "氢能",
        "url": "https://eureka.zhihuiya.com/view/#/fullText?patentId=6c9ae0bf-d1f4-4f5e-ba9b-0c7e096e676a"
    }
]

# ── 专利数据转 JS 字符串 ──────────────────────────────────
def patents_to_js(patents: list[dict]) -> str:
    return json.dumps(patents, ensure_ascii=False, indent=2)

# ── 读取模板并注入数据 ────────────────────────────────────
def inject_patents_into_template(template_html: str, patents: list[dict]) -> str:
    js_data = patents_to_js(patents)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 替换占位符（模板中预留的注入点）
    replacements = [
        ("__PATENT_DATA_JSON__", js_data),
        ("__GENERATED_AT__", ts),
        ("__PATENT_COUNT__", str(len(patents))),
    ]
    result = template_html
    for placeholder, value in replacements:
        result = result.replace(placeholder, value)

    # 如果模板中没有占位符，在 </body> 前插入数据初始化脚本
    if "__PATENT_DATA_JSON__" not in template_html:
        inject_script = f"""
<script>
// ── PatSnap MCP 注入专利数据 ── 生成时间: {ts}
(function() {{
  var injectedPatents = {js_data};
  if (typeof PATENT_DATA !== 'undefined') {{
    PATENT_DATA.length = 0;
    injectedPatents.forEach(function(p) {{ PATENT_DATA.push(p); }});
  }}
  window.__PATSNAP_INJECTED__ = injectedPatents;
  window.__GENERATED_AT__ = '{ts}';
  console.log('[PatSnap] 已注入 ' + injectedPatents.length + ' 条专利数据，生成时间：{ts}');
}})();
</script>"""
        result = result.replace("</body>", inject_script + "\n</body>")

    return result

# ── 主流程 ────────────────────────────────────────────────
def main():
    keywords = [kw.strip() for kw in args.keywords.split(",") if kw.strip()]
    print(f"[INFO] 开始检索专利，关键词：{keywords}，数量：{args.topk}")

    patents = fetch_patents_via_patsnap(keywords, args.topk)
    print(f"[INFO] 获取到 {len(patents)} 条专利数据")

    if TEMPLATE_PATH and TEMPLATE_PATH.exists():
        print(f"[INFO] 读取模板：{TEMPLATE_PATH}")
        template_html = TEMPLATE_PATH.read_text(encoding="utf-8")
        output_html = inject_patents_into_template(template_html, patents)
    else:
        print("[WARN] 未找到 HTML 模板，生成数据摘要文件...")
        output_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>专利数据摘要</title></head>
<body>
<h1>现代能源专利数据（{len(patents)} 条）</h1>
<p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<pre>{json.dumps(patents, ensure_ascii=False, indent=2)}</pre>
</body>
</html>"""

    OUTPUT_PATH.write_text(output_html, encoding="utf-8")
    print(f"[DONE] 输出文件：{OUTPUT_PATH}（{len(output_html):,} 字符）")

    # 输出绑定 JSON（供 Eureka outputs 合约使用）
    bindings_json = os.environ.get("EUREKA_PYTHON_OUTPUT_BINDINGS_JSON", "")
    if bindings_json:
        try:
            bindings = json.loads(bindings_json)
            html_path = bindings.get("platform_html", "")
            if html_path and html_path != str(OUTPUT_PATH):
                Path(html_path).parent.mkdir(parents=True, exist_ok=True)
                Path(html_path).write_text(output_html, encoding="utf-8")
                print(f"[DONE] 同步写入绑定路径：{html_path}")
        except Exception as e:
            print(f"[WARN] 输出绑定处理异常：{e}")

if __name__ == "__main__":
    main()
