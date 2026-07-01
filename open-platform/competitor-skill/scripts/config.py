import os
from pathlib import Path
from dotenv import load_dotenv

# 优先加载本目录的 .env，其次加载 patsnap_skill 的 .env（共享凭证）
_here = Path(__file__).parent
for _env in [_here / ".env", _here.parent / ".env", Path.home() / "Documents" / "patsnap_skill" / ".env", Path.home() / "Documents" / "patsnap_skill" / "scripts" / ".env"]:
    if _env.exists():
        load_dotenv(_env)
        break

PATSNAP_BASE_URL = os.getenv("PATSNAP_BASE_URL", "https://connect.zhihuiya.com")
PATSNAP_API_KEY = os.getenv("PATSNAP_API_KEY", "")  # 从 scripts/.env 读取，首次使用需配置
LITERATURE_API_KEY = os.getenv("LITERATURE_API_KEY", PATSNAP_API_KEY)
ARK_API_KEY = os.getenv("ARK_API_KEY", "")
ARK_BASE_URL = os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
ARK_MODEL = os.getenv("ARK_MODEL", "doubao-seed-2-0-pro-260215")
