# BIPV 技术关键词配置文件

# 检索字段
SEARCH_COLS = ["标题", "Patsnap专利标题", "技术问题", "技术手段", "技术功效"]

# 包含关键词（命中任意一个即判定为高相关）
INCLUDE_KEYWORDS = [
    # 1. 曲面光伏瓦（绝对核心）
    "曲面光伏", "光伏瓦", "曲面瓦", "光伏屋面瓦", "XBC", "多曲面",
    "弧形光伏", "仿古光伏", "光伏陶瓦", "光伏沥青瓦", "晶硅光伏瓦",
    "curved solar tile", "curved photovoltaic", "solar roof tile",
    "solar shingles", "solar clay tile", "multi-curved photovoltaic",

    # 2. 户用坡屋顶 BIPV
    "坡屋顶光伏", "斜屋面光伏", "坡屋面光伏", "户用BIPV", "户用光伏屋顶",
    "屋顶建材光伏", "光伏一体化屋顶", "防水光伏屋面",
    "pitched roof photovoltaic", "sloped roof BIPV", "residential BIPV",

    # 3. 光储一体化
    "光储一体", "BIPV储能", "户用光储", "家庭储能光伏", "离网光伏储能",
    "光伏家储", "智能能源管理",
    "solar storage integration", "BIPV energy storage",
    "off-grid solar storage", "home energy storage",

    # 4. DIY 轻量化组件
    "DIY光伏", "即插即用光伏", "阳台光伏", "便携光伏", "轻量化光伏",
    "小型BIPV", "balcony solar", "plug-and-play solar", "portable solar",

    # 5. 玻璃深加工与封装油墨
    "超白钢化玻璃", "哑光光伏玻璃", "曲面封装", "超薄电池片",
    "光伏封装油墨", "封装油墨", "曲面玻璃光伏",
    "ultra-white tempered glass", "matte photovoltaic glass",
    "curved encapsulation", "ultra-thin solar cell", "PV encapsulation ink",
]

# 排除关键词（命中则降级，即使命中包含词也不标引）
EXCLUDE_KEYWORDS = [
    "光伏幕墙", "光伏外立面", "光伏外墙", "建筑幕墙",
    "solar facade", "PV curtain wall", "photovoltaic facade",
    "厂房光伏", "商业建筑BIPV", "大型公共建筑",
    "平屋顶光伏", "flat roof PV",
    "光伏逆变器", "PV inverter", "solar inverter", "微型逆变器",
]

# 公司简称映射
COMPANY_SHORT = {
    '特斯拉公司(美国)': '特斯拉',
    'AUTARQ GMBH': 'AUTARQ',
    '隆基绿能科技股份有限公司': '隆基绿能',
    '正泰新能科技股份有限公司': '正泰新能',
    '天合富家能源股份有限公司': '天合富家',
    '合肥国轩高科动力能源有限公司': '国轩高科',
    '浙江金贝能源科技有限公司': '金贝能源',
    '东方日升绿电(浙江)建材有限公司': '东方日升',
}
