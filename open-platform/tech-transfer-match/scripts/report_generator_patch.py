
# ─────────────────────────────────────────────
# 桌面保存工具函数（每次生成报告自动调用）
# 追加至 report_generator.py 末尾
# ─────────────────────────────────────────────

import os
import shutil
from pathlib import Path


def save_report_to_desktop(html_content: str, filename: str) -> dict:
    """
    将 HTML 报告同时保存到：
      1. ~/Desktop/<filename>（用户桌面，主要目标）
      2. 当前工作目录 reports/<filename>（备份）

    参数:
      html_content: 完整 HTML 字符串
      filename: 文件名，如 tech_transfer_report_20260422.html

    返回:
      {
        "desktop_path": str,
        "backup_path": str,
        "success": bool,
        "message": str
      }
    """
    result = {
        "desktop_path": "",
        "backup_path": "",
        "success": False,
        "message": ""
    }

    # ── 1. 写入桌面 ──
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        desktop = Path.home() / "桌面"  # 中文系统备用

    if desktop.exists():
        desktop_file = desktop / filename
        desktop_file.write_text(html_content, encoding="utf-8")
        result["desktop_path"] = str(desktop_file)
        result["success"] = True
        result["message"] = f"✅ 报告已保存到桌面：{desktop_file}"
    else:
        result["message"] = "⚠️ 未找到桌面目录（Desktop / 桌面）"

    # ── 2. 同时写入备份目录（session reports/）──
    try:
        backup_dir = Path(os.environ.get("EUREKA_SESSION_DIR", str(Path.home()))) / "reports"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / filename
        backup_file.write_text(html_content, encoding="utf-8")
        result["backup_path"] = str(backup_file)
    except Exception as e:
        result["backup_path"] = f"备份失败: {e}"

    return result


def save_and_announce(html_content: str, topic: str, date_str: str = None) -> str:
    """
    一步完成：保存报告到桌面 + 返回用户可见提示字符串

    参数:
      html_content: 完整 HTML 字符串
      topic: 技术主题（用于生成文件名）
      date_str: 日期字符串，默认今天 YYYYMMDD

    返回: 用户可见的路径提示 Markdown 字符串
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")

    # 清理文件名特殊字符，取前30字符
    safe_topic = "".join(c for c in topic if c.isalnum() or c in "-_")[:30]
    if not safe_topic:
        safe_topic = "report"
    filename = f"tech_transfer_{safe_topic}_{date_str}.html"

    res = save_report_to_desktop(html_content, filename)

    lines = [
        f"📄 **文件名**：`{filename}`",
    ]
    if res["desktop_path"]:
        lines.append(f"🖥️ **桌面路径**：`{res['desktop_path']}`")
    if res["backup_path"] and not res["backup_path"].startswith("备份失败"):
        lines.append(f"📁 **备份路径**：`{res['backup_path']}`")
    lines.append(res["message"])
    return "\n".join(lines)
