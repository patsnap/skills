#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纳恩博专利态势官 · main.py
自动计算上一标准自然周（周一~周日），所有检索严格锁定该窗口。
"""
import os
from datetime import date, timedelta

# ── 自动计算上一完整自然周 ─────────────────────────────────────────────────────
# 无论今天是周几，都取"上一个完整自然周（周一~周日）"
# 例：今天 2026-05-25（周一），上周 = 2026-05-18（周一）~ 2026-05-24（周日）
today = date.today()
# today.weekday()：周一=0, 周日=6
# 上周一 = 今天 - 今天是本周第几天(0-indexed) - 7天
last_monday = today - timedelta(days=today.weekday() + 7)
last_sunday  = last_monday + timedelta(days=6)

WEEK_START   = last_monday.strftime("%Y-%m-%d")   # 例 "2026-05-18"
WEEK_END     = last_sunday.strftime("%Y-%m-%d")    # 例 "2026-05-24"
DATE_FROM    = int(last_monday.strftime("%Y%m%d")) # 例 20260518，用于 PatSnap filter
DATE_TO      = int(last_sunday.strftime("%Y%m%d")) # 例 20260524
ISO_WEEK     = last_monday.isocalendar()[1]         # ISO 周次，例 21
REPORT_WEEK  = f"W{ISO_WEEK:02d}"                  # 例 "W21"
GEN_DATE     = today.strftime("%Y-%m-%d")

print(f"[纳恩博专利态势官] 监控窗口：{WEEK_START} ~ {WEEK_END}（{REPORT_WEEK}）")
print(f"[纳恩博专利态势官] PatSnap 过滤参数：date_from={DATE_FROM}, date_to={DATE_TO}")
print(f"[纳恩博专利态势官] 生成日期：{GEN_DATE}")

# ── PatSnap 检索参数模板（供调用方使用）───────────────────────────────────────
# 所有竞对专利检索均应传入以下 date_filter，确保只检索自然周窗口内公开的专利
DATE_FILTER = {
    "date_from": DATE_FROM,
    "date_to":   DATE_TO,
    "date_type": "publication",
}

# ── 输出配置 ──────────────────────────────────────────────────────────────────
OUT_DIR      = os.environ.get("EUREKA_PYTHON_OUTPUT_DIR", ".")
OUT_FILENAME = f"ninebot_weekly_{REPORT_WEEK}_{today.strftime('%Y%m%d')}.html"
OUT_PATH     = os.path.join(OUT_DIR, OUT_FILENAME)

if __name__ == "__main__":
    print(f"[纳恩博专利态势官] 输出路径：{OUT_PATH}")
    print("[纳恩博专利态势官] 本脚本为入口模块，完整报告生成逻辑由 Eureka 技能框架驱动。")
    print("[纳恩博专利态势官] 使用方式：在 Eureka 中说 '运行态势周报' 即可自动执行完整六模块报告。")
