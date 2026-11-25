import json
from pathlib import Path

from common import require, source_ref


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_THEME = "blue"
THEMES = {
    "red": {"name": "华为红", "use": "公司技术简报与重点进展", "aliases": ["华为红"], "profile": "reference-report"},
    "blue": {"name": "科技蓝", "use": "技术研究与公司情报", "aliases": ["科技蓝", "蓝色"], "profile": "reference-report"},
    "green": {"name": "生态绿", "use": "产业生态与长期跟踪", "aliases": ["生态绿"], "profile": "reference-report"},
    "violet": {"name": "砚紫", "use": "专题研究与个人阅读", "aliases": ["砚紫"], "profile": "reference-report"},
    "amber": {"name": "石墨金", "use": "公司布局与管理层阅读", "aliases": ["石墨金"], "profile": "reference-report"},
}


def resolve_theme(value: str | None = None) -> str:
    if value is None:
        return DEFAULT_THEME
    require(isinstance(value, str) and bool(value.strip()), "报告色系名称不能为空")
    name = value.strip().casefold()
    matches = [key for key, item in THEMES.items()
               if name in {key, *(alias.casefold() for alias in item["aliases"])}]
    require(len(matches) == 1, "无法识别报告色系，请运行 scripts/report_themes.py 查看可用名称：" + value)
    return matches[0]


def theme_path(value: str | None = None) -> Path:
    key = resolve_theme(value)
    path = ROOT / "assets/themes" / (key + ".css")
    require(path.is_file(), "缺少报告配色文件：" + str(path))
    return path


def theme_css(value: str | None = None) -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in theme_files(value))


def theme_files(value: str | None = None) -> list[Path]:
    key = resolve_theme(value)
    paths = [theme_path(key)]
    if THEMES[key].get("profile") == "reference-report":
        paths.append(ROOT / "assets/themes/reference-report.css")
    for path in paths:
        require(path.is_file(), "缺少报告配色文件：" + str(path))
    return paths


def theme_info(value: str | None = None) -> dict:
    key = resolve_theme(value)
    paths = theme_files(key)
    return {"id": key, "name": THEMES[key]["name"], "source": source_ref(paths[0]),
            **({"shared_source": source_ref(paths[1])} if len(paths) > 1 else {})}


if __name__ == "__main__":
    print(json.dumps({"default": DEFAULT_THEME, "themes": [{"id": key, **item} for key, item in THEMES.items()]},
                     ensure_ascii=False, indent=2))
