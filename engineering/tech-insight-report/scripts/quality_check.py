#!/usr/bin/env python3
"""
quality_check.py — 技术洞察报告自动化质检脚本
用法：python quality_check.py <report.html>
输出：5项检查结果，全部 ✅ 才可发布
"""
import sys
import re
from collections import Counter
from pathlib import Path


def check_html_structure(content: str) -> tuple[bool, str]:
    """CHECK-1：HTML结构完整性（章节锚点 + id唯一性）"""
    errors = []
    for i in range(10):
        if f'id="s{i}"' not in content:
            errors.append(f"缺少章节锚点 id=\"s{i}\"")
    ids = re.findall(r'id="([^"]+)"', content)
    dupes = {k: v for k, v in Counter(ids).items() if v > 1}
    if dupes:
        errors.append(f"重复ID: {dupes}")
    canvas_ids = re.findall(r'<canvas[^>]+id="([^"]+)"', content)
    canvas_dupes = {k: v for k, v in Counter(canvas_ids).items() if v > 1}
    if canvas_dupes:
        errors.append(f"重复canvas ID: {canvas_dupes}")
    if errors:
        return False, "；".join(errors)
    return True, f"锚点s0~s9全部存在，{len(ids)}个id全部唯一"


def check_version_number(content: str) -> tuple[bool, str]:
    """CHECK-2：版本号3处一致且无旧版残留"""
    versions = re.findall(r'V(\d+\.\d+)', content)
    if not versions:
        return False, "未找到任何版本号（格式应为 VX.X）"
    version_counter = Counter(versions)
    if len(version_counter) > 1:
        return False, f"存在多个版本号（旧版残留）: {dict(version_counter)}"
    version = versions[0]
    count = version_counter[version]
    if count < 3:
        return False, f"V{version} 仅出现 {count} 处，应在 title/meta/footer 共3处"
    return True, f"版本号 V{version} 共出现 {count} 处，唯一且≥3处 ✓"


def check_critical_sections(content: str) -> tuple[bool, str]:
    """CHECK-3：关键章节内容完整性（双语关键词，命中任一语言即通过）"""
    keywords = [
        ("决策建议", "Decision"),
        ("市场格局", "Market"),
        ("技术路线", "Technology"),
        ("竞争情报", "Competitive"),
        ("专利全景", "Patent"),
        ("标准法规", "Standard"),
        ("热点", "Hotspot"),
        ("规避建议", "Avoidance"),
        ("高风险", "High Risk"),
        ("离线", "Offline"),
    ]
    missing = [f"{zh}/{en}" for zh, en in keywords
               if zh not in content and en not in content]
    if missing:
        return False, f"缺少关键内容词: {missing}"
    return True, "10个关键词（双语）全部命中 ✓"


def check_legal_language(content: str) -> tuple[bool, str]:
    """CHECK-4：法律语气合规（禁用词零命中）"""
    forbidden = ["无侵权风险", "不会侵权", "已解决侵权", "无需担心侵权", "完全安全"]
    hits = []
    for word in forbidden:
        positions = [m.start() for m in re.finditer(re.escape(word), content)]
        if positions:
            lines_before = content[:positions[0]].count('\n') + 1
            hits.append(f'"{word}"（第{lines_before}行）')
    if hits:
        return False, f"发现禁用法律措辞: {'; '.join(hits)}"
    return True, "法律语气检查通过，禁用词零命中 ✓"


def check_version_in_footer(content: str) -> tuple[bool, str]:
    """CHECK-5：footer包含版本号和数据截止日期"""
    footer_match = re.search(r'<footer[^>]*>(.*?)</footer>', content, re.DOTALL)
    if not footer_match:
        return False, "未找到 <footer> 标签"
    footer_text = footer_match.group(1)
    errors = []
    if not re.search(r'V\d+\.\d+', footer_text):
        errors.append("footer缺少版本号")
    if not re.search(r'数据截止|截止日期|\d{4}年\d{1,2}月', footer_text):
        errors.append("footer缺少数据截止日期")
    if errors:
        return False, "；".join(errors)
    return True, "footer版本号和数据截止日期均存在 ✓"


def main():
    if len(sys.argv) < 2:
        print("用法：python quality_check.py <report.html>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"❌ 文件不存在：{path}")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    print(f"\n{'='*60}")
    print(f"  技术洞察报告质检报告")
    print(f"  文件：{path.name}  ({len(content):,} 字符)")
    print(f"{'='*60}\n")

    checks = [
        ("HTML结构完整性", check_html_structure),
        ("版本号一致性", check_version_number),
        ("关键章节完整性", check_critical_sections),
        ("法律语气合规", check_legal_language),
        ("Footer完整性", check_version_in_footer),
    ]

    passed = 0
    for name, fn in checks:
        ok, msg = fn(content)
        status = "✅" if ok else "❌"
        print(f"  {status} [{name}]")
        print(f"     {msg}\n")
        if ok:
            passed += 1

    print(f"{'='*60}")
    print(f"  结果：{passed}/{len(checks)} 项通过")
    if passed == len(checks):
        print("  🎉 全部通过，报告可以发布！")
    else:
        print(f"  ⚠️  {len(checks)-passed} 项未通过，请修复后重新运行")
    print(f"{'='*60}\n")

    sys.exit(0 if passed == len(checks) else 1)


if __name__ == "__main__":
    main()
