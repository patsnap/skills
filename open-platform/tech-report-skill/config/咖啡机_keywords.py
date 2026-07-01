# 咖啡机技术关键词配置文件

# 检索字段
SEARCH_COLS = ["标题", "Patsnap专利标题", "技术问题", "技术手段", "技术功效"]

# 包含关键词（命中任意一个即判定为高相关）
INCLUDE_KEYWORDS = [
    # 1. 研磨精度与均匀度技术
    "研磨精度", "研磨均匀", "磨豆机", "咖啡研磨", "研磨颗粒", "粉末均匀",
    "锥刀", "平刀", "鬼齿", "刀盘", "研磨刀", "磨盘",
    "grinding precision", "grinder", "coffee grinder", "burr grinder",
    "grinding uniformity", "particle size", "grinding consistency",
    "conical burr", "flat burr", "grinding blade",

    # 2. 加热温控技术
    "加热温控", "温度控制", "恒温", "PID温控", "热稳定", "温度稳定",
    "加热块", "锅炉", "热交换", "预热", "保温",
    "heating control", "temperature control", "thermostat", "PID control",
    "thermal stability", "heating block", "boiler", "heat exchanger",
    "preheating", "temperature stability",

    # 3. 高压压力动态控制技术
    "压力控制", "萃取压力", "预浸泡", "变压萃取", "压力曲线",
    "泵压", "水泵", "压力传感", "动态压力",
    "pressure control", "extraction pressure", "pre-infusion",
    "pressure profiling", "pressure curve", "pump pressure",
    "water pump", "pressure sensor", "dynamic pressure",

    # 4. 冲煮头均匀布水萃取技术
    "冲煮头", "布水", "萃取均匀", "淋浴网", "分水网", "出水孔",
    "萃取", "咖啡萃取", "均匀萃取", "水流分布",
    "brew head", "brewing head", "shower screen", "water distribution",
    "extraction uniformity", "brewing uniformity", "water flow",
    "coffee extraction", "uniform extraction",

    # 5. 蒸汽奶泡绵密技术
    "蒸汽", "奶泡", "打奶", "奶泡绵密", "微泡", "奶泡质地",
    "蒸汽棒", "蒸汽喷嘴", "奶泡系统", "自动打奶",
    "steam", "milk foam", "milk froth", "microfoam", "milk texture",
    "steam wand", "steam nozzle", "frothing", "milk frothing",
    "automatic milk frother", "cappuccino",

    # 6. 智能电控与水路闭环技术
    "智能控制", "电控", "闭环控制", "传感器", "自动化",
    "物联网", "APP控制", "远程控制", "智能咖啡机",
    "水路控制", "流量控制", "水位检测",
    "intelligent control", "electronic control", "closed-loop control",
    "sensor", "automation", "IoT", "smart coffee machine",
    "app control", "remote control", "water flow control",
    "flow control", "water level detection",

    # 通用咖啡机相关词
    "咖啡机", "浓缩咖啡", "意式咖啡", "全自动咖啡机", "半自动咖啡机",
    "coffee machine", "espresso machine", "coffee maker",
    "automatic coffee machine", "semi-automatic coffee machine",
]

# 排除关键词（命中则降级，即使命中包含词也不标引）
EXCLUDE_KEYWORDS = [
    # 排除非咖啡机相关的饮料设备
    "茶饮机", "果汁机", "豆浆机", "榨汁机",
    "tea machine", "juice machine", "juicer",

    # 排除咖啡种植、加工相关
    "咖啡种植", "咖啡豆加工", "咖啡烘焙", "咖啡豆包装",
    "coffee plantation", "coffee processing", "coffee roasting",

    # 排除纯包装、物流相关
    "咖啡包装", "咖啡配送", "咖啡物流",
    "coffee packaging", "coffee delivery",
]

# 公司简称映射
COMPANY_SHORT = {
    '德隆吉器具有限公司': '德隆',
    '雀巢产品有限公司': '雀巢',
    '美的集团股份有限公司': '美的',
    '小熊电器股份有限公司': '小熊',
    '九阳股份有限公司': '九阳',
    '飞利浦': '飞利浦',
    'PHILIPS': '飞利浦',
    'NESTEC': '雀巢',
    'NESTLE': '雀巢',
    'DE LONGHI': '德隆',
    'DELONGHI': '德隆',
    'MIDEA': '美的',
}
