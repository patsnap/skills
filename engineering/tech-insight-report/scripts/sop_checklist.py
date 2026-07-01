#!/usr/bin/env python3
"""
sop_checklist.py — 技术洞察报告SOP阶段检查清单
用法：python sop_checklist.py [phase]
      phase: 0|1|2|3|4|5|all（默认all）
输出：当前阶段的交互式检查清单
"""
import sys

PHASES = {
    0: {
        "name": "Phase 0：开写前强制预检",
        "items": [
            "【铁律确认】默读章节结构铁律：§0→§9顺序固定，禁止调整/删减/新增，风格对照骨架模板",
            "建立跨章节数据同步表（见SKILL.md CHECK-5模板）",
            "PatSnap MCP初步IPC扫描，确认技术边界",
            "搭建10章HTML骨架（§0~§9），运行 quality_check.py 验证结构",
            "六维信源采集计划列表已制定（专利/论文/市场/新闻/政策/标准）",
            "预计引用专利列表已通过CHECK-2表格逐一核实",
            "CHECK-6法律语气禁用词列表已准备好（对照表见SKILL.md）",
        ]
    },
    1: {
        "name": "Phase 1：全信源数据采集",
        "items": [
            "专利数据：§4全量检索已按6.3五步法执行，每个IPC分类的matched_total已记录（⚠️禁止仅用topk样本）",
            "专利数据：高风险候选池已建立（被引>20的有效专利）",
            "专利数据：近24个月申请趋势已分析",
            "每条专利：CHECK-2核实表格6列全部填满",
            "市场数据：至少2家独立机构数据，来源标注完整",
            "科技新闻：每家重点企业近12个月动态已采集",
            "政策法规：现行标准条款和空白已标注",
            "近期T0/T1动态：每章节独立执行检索",
        ]
    },
    2: {
        "name": "Phase 2：行业链分析",
        "items": [
            "行业价值链（上游→中游→下游）已绘制",
            "上游：关键材料/零部件供应商已列出+近期动态",
            "中游：主要Tier1市占率+核心专利布局已列出",
            "下游：OEM采购策略+终端场景已分析",
            "上下游技术联动影响已分析",
            "下游需求变化反推技术方向已完成",
        ]
    },
    3: {
        "name": "Phase 3：HTML报告编写",
        "items": [
            "CSS变量体系（暗色科技风）已定义完整",
            "图表CSS四件套已写入（ipc-bar-row/bg/fill/label）",
            "每张Chart.js图表有配套<details>离线降级表",
            "CDN失效时降级表自动展开逻辑已写入",
            "所有导航链接为相对锚点（#s0~#s9），无file:///路径",
            "版本号已写入3处（title/meta/footer）",
            "竞争情报表每行列数已验证与表头一致",
            "§8规避建议语气已软化，免责声明存在",
            "§0决策建议最后写，引用§4最终风险等级",
            "移动端宽表格有滑动提示",
            "回顶按钮已添加（position:fixed右下角）",
        ]
    },
    4: {
        "name": "Phase 4：自动化质检",
        "items": [
            "运行 quality_check.py，5项全部 ✅",
            "图表JS data与离线降级表数值完全一致",
            "图表图例已显示（plugins.legend.display: true）",
            "行业链上下游企业均已列入§3",
            "§0风险等级与§4风险清单完全对应（6条逻辑链）",
            "16项视觉完整性清单已逐项打勾（见SKILL.md第15章）",
        ]
    },
    5: {
        "name": "Phase 5：发布前终审",
        "items": [
            "全文逐章通读完成（非只看修改段落）",
            "移动端兼容检查完成",
            "离线可用性检查完成（CDN降级表可自动展开）",
            "8维度质量评估打分（评分标准见第11章）：___/40分（≥36分合格发布，≥39分为首次目标）",
            "版本号已归档，文件名含版本号",
            "footer数据截止日期已更新",
        ]
    }
}


def print_checklist(phase_num: int):
    phase = PHASES[phase_num]
    print(f"\n{'='*60}")
    print(f"  {phase['name']}")
    print(f"{'='*60}")
    for i, item in enumerate(phase['items'], 1):
        print(f"  □ {i:2d}. {item}")
    print()


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"

    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║       技术洞察报告 SOP 检查清单                          ║")
    print("║       tech-insight-report Skill                          ║")
    print("╚══════════════════════════════════════════════════════════╝")

    if arg == "all":
        for phase_num in sorted(PHASES.keys()):
            print_checklist(phase_num)
    elif arg.isdigit() and int(arg) in PHASES:
        print_checklist(int(arg))
    else:
        print(f"\n用法：python sop_checklist.py [0|1|2|3|4|5|all]")
        print("  0 = Phase 0 开写前强制预检")
        print("  1 = Phase 1 全信源数据采集")
        print("  2 = Phase 2 行业链分析")
        print("  3 = Phase 3 HTML报告编写")
        print("  4 = Phase 4 自动化质检")
        print("  5 = Phase 5 发布前终审")
        print("  all = 全部阶段\n")
        sys.exit(1)

    print("提示：运行 quality_check.py <report.html> 执行自动化质检")
    print()


if __name__ == "__main__":
    main()
