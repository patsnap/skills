"""
保标API (gov-bid.com) 完整对接模块
基于官方接口文档 http://faq.zhvac.com/web/#/57
生产环境: https://gate.gov-bid.com
认证方式: 每个请求URL带参数 key=<your_key>
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

# ─────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────
BASE_URL = "https://gate.gov-bid.com/outer-gateway/bid"
API_KEY  = "c25c774b2b1d4e15adfd0a1ebded3adb"
TIMEOUT  = 15  # 秒
USER_ID  = 88  # 文档固定值


def _url(path: str) -> str:
    """拼接完整请求URL（含key参数）"""
    return f"{BASE_URL}/{path}?key={API_KEY}"


def _post_json(path: str, payload: dict) -> dict:
    """通用 POST application/json 请求"""
    resp = requests.post(_url(path), json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _post_form(path: str, data: dict) -> dict:
    """通用 POST multipart/form-data 请求"""
    resp = requests.post(_url(path), data=data, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


# ─────────────────────────────────────────────
# 接口3：招标采购信息搜索（新版）
# 文档页 page_id=445
# ─────────────────────────────────────────────
def search_projects(
    keyword: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page_id: int = 1,
    page_number: int = 20,
    search_type: int = 1,
    area_province_codes: Optional[List[str]] = None,
    exclude_kw: Optional[str] = None,
    include_kw: Optional[str] = None,
    project_class_ids: Optional[str] = None,
    purchase_type_ids: Optional[str] = None,
    project_money_min: Optional[int] = None,
    project_money_max: Optional[int] = None,
) -> dict:
    """
    招标采购信息高级搜索
    
    参数说明：
    - keyword: 搜索关键词（多词"同时出现"用空格，"或关系"用竖线|分隔，总长≤300字）
    - start_date: 发布开始日期 yyyy-MM-dd（必填，默认近30天）
    - end_date: 发布结束日期 yyyy-MM-dd（必填，与start_date间隔≤1年）
    - page_id: 页码（从1开始）
    - page_number: 每页条数（最大50；传0仅返回total）
    - search_type: 1=智能模糊搜索，2=精确搜索，3=高级搜索（单关键词精确）
    - area_province_codes: 省份code列表，["0"]表示全国，省份code参见Area.csv
    - project_class_ids: 14个子分类ID，逗号分隔（见枚举值-码表）
    - purchase_type_ids: 采购分类 0=其他,1=服务类,2=工程类,3=货物类，逗号分隔
    
    返回: 原始API响应，data.data为项目列表，data.total为总数
    """
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    payload: Dict[str, Any] = {
        "keyword": keyword,
        "excludeKW": exclude_kw,
        "inCludeKW": include_kw,
        "sourceType": "0",
        "searchMode": 1,
        "areaCode": {
            "ProviceCodeList": area_province_codes or ["0"],
            "CityCodeList": [],
            "CuntyCodeList": [],
        },
        "industryCode": {
            "FirstCodeList": ["0"],
            "SecondCodeList": [],
            "ThirdCodeList": [],
        },
        "startDate": start_date,
        "endDate": end_date,
        "userId": USER_ID,
        "pageId": page_id,
        "pageNumber": page_number,
        "searchType": search_type,
    }
    if project_class_ids:
        payload["projectClassID"] = project_class_ids
    if purchase_type_ids:
        payload["purchaseTypeID"] = purchase_type_ids
    if project_money_min is not None:
        payload["projectMoneyMin"] = project_money_min
    if project_money_max is not None:
        payload["projectMoneyMax"] = project_money_max

    return _post_json("searchProjectApi", payload)


# ─────────────────────────────────────────────
# 接口4：项目结构化数据获取（含源网址）
# 文档页 page_id=446
# ─────────────────────────────────────────────
def get_project_structure(project_id: int, publish_time: str) -> dict:
    """
    获取项目结构化字段详情（含预算金额、中标金额、甲方、乙方、代理机构、合同信息等）
    
    参数：
    - project_id: 项目ID（来自search_projects返回的data.id）
    - publish_time: 项目发布时间（来自data.publishTime）
    
    返回: data字段含 projectName, projectID, budgetMoney, bidMoney, 
          partyAInfo, partyBInfo, agencyInfo, bidCompany, sbkjBidUrl, collectUrl 等
    """
    return _post_form("getZTBStructreDetail", {
        "id": project_id,
        "publishTime": publish_time,
    })


# ─────────────────────────────────────────────
# 接口5：项目完整正文获取（不含结构化数据）
# 文档页 page_id=447
# ─────────────────────────────────────────────
def get_project_detail(project_id: int, publish_time: str) -> dict:
    """
    获取项目完整正文内容（含基础信息、关联附件等，不含结构化数据）
    
    参数：
    - project_id: 项目ID
    - publish_time: 项目发布时间
    
    返回: data含 id, title, content(HTML), newsTypeID, areaName 等
    """
    return _post_form("getZTBProjectDetail", {
        "id": project_id,
        "publishTime": publish_time,
    })


# ─────────────────────────────────────────────
# 接口6：项目附件列表获取
# 文档页 page_id=448
# ─────────────────────────────────────────────
def get_project_files(project_id: int, publish_time: str) -> dict:
    """
    获取项目关联的所有附件信息（含下载地址、文件类型、文件状态等）
    
    参数：
    - project_id: 项目ID
    - publish_time: 项目发布时间
    
    返回: data为附件数组，每项含 name, url, suffix, size, state 等
    注意: state=0未下载，1下载正常，2下载失败，3超过20M，4文件损坏，5URL失效
    """
    return _post_form("getZTBProjectFiles", {
        "projectId": project_id,
        "publishTime": publish_time,
    })


# ─────────────────────────────────────────────
# 接口7：招标信息搜索（AI专用版）
# 文档页 page_id=449
# ─────────────────────────────────────────────
def search_projects_for_ai(
    keyword: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page_id: int = 1,
    page_number: int = 20,
    class_name: Optional[str] = None,
    area_name: Optional[str] = None,
    search_field: str = "全部",
) -> dict:
    """
    专为AI模型设计的招标投标数据搜索接口（简化参数版）
    
    参数：
    - keyword: 关键词（多词"或关系"用竖线|分隔）
    - start_date: 发布开始日期 yyyy-MM-dd（必填）
    - end_date: 发布结束日期 yyyy-MM-dd（必填）
    - class_name: 项目分类（"全部信息","招标信息","中标信息","合同信息","采购意向","拍租信息"，逗号分隔）
    - area_name: 归属地区名称（如"武汉"）
    - search_field: 搜索字段（"标题","内容","全部"）
    - page_number: 每页条数（最大100）
    
    返回: data.data 为项目列表，含 id, title, publishTime, areaName, 
          projectMoney, projectClass, partAInfo, partBInfo, agencyInfo 等
    """
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    payload: Dict[str, Any] = {
        "keyword": keyword,
        "startDate": start_date,
        "endDate": end_date,
        "pageId": page_id,
        "pageNumber": page_number,
        "searchField": search_field,
    }
    if class_name:
        payload["className"] = class_name
    if area_name:
        payload["areaName"] = area_name

    return _post_json("SearchProjectForAI", payload)


# ─────────────────────────────────────────────
# 接口8：合同数据搜索列表
# 文档页 page_id=450
# ─────────────────────────────────────────────
def search_contracts(
    keyword: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page_id: int = 1,
    page_number: int = 20,
    search_type: int = 1,
    area_province_codes: Optional[List[str]] = None,
    contract_end_min: Optional[str] = None,
    contract_end_max: Optional[str] = None,
) -> dict:
    """
    项目合同数据搜索（返回合同金额、甲方、乙方、合同到期时间、项目周期等）
    
    参数：
    - keyword: 搜索关键词
    - start_date/end_date: 发布日期范围（必填）
    - contract_end_min/max: 合同截止日期范围（格式 yyyy-MM-dd）
    - page_number: 每页条数（最大100）
    
    返回: data.data 含合同核心字段
    """
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload: Dict[str, Any] = {
        "keyword": keyword,
        "sourceType": None,
        "searchMode": 1,
        "areaCode": {
            "proviceCodeList": area_province_codes or ["0"],
            "cityCodeList": [],
            "countyCodeList": [],
        },
        "industryCode": {
            "firstCodeList": ["0"],
            "secondCodeList": [],
            "thirdCodeList": [],
        },
        "startDate": start_date,
        "endDate": end_date,
        "userID": USER_ID,
        "pageID": page_id,
        "pageNumber": page_number,
        "searchType": search_type,
        "keyWordType": -100,
        "purchaseTypeID": "-100",
    }
    if contract_end_min:
        payload["contractEndMin"] = contract_end_min
    if contract_end_max:
        payload["contractEndMax"] = contract_end_max

    return _post_json("searchProjectContactApi", payload)


# ─────────────────────────────────────────────
# 接口9：AI搜索条件重写（异步轮询）
# 文档页 page_id=451
# ─────────────────────────────────────────────
def ai_search_rewrite(user_query: str) -> dict:
    """
    提交AI搜索请求，返回 requestKey 供后续轮询查询结果。
    如果缓存命中，直接返回 status=completed 的完整结果。
    
    参数：
    - user_query: 用户自然语言搜索文本（如"军队采购网 病床 北京"）
    
    返回: data 含 requestKey, status(processing/completed/failed),
          searchCondition(关键词重写结果), industryCodes, areaCode
    """
    return _post_json("aiSearchSubmitPolling", {"userQuery": user_query})


# ─────────────────────────────────────────────
# 接口10：AI行业搜索
# 文档页 page_id=452
# ─────────────────────────────────────────────
def ai_industry_reasoning(keyword: str) -> dict:
    """
    根据行业短语，调用AI推理接口获取相关行业标签信息（国家统计局行业码）
    
    参数：
    - keyword: 行业关键词短语（如"教育"、"空调"）
    
    返回: data 为行业码数组，每项含 firstCodeList, secondCodeList, thirdCodeList, 
          fullTitle(如"教育-教育-高等教育"), minTitle
    """
    return _post_json("industryReasoning", {"keyword": keyword})


# ─────────────────────────────────────────────
# 便捷方法：面向技术转移场景的招标搜索
# ─────────────────────────────────────────────
def search_tender_for_tech_transfer(
    tech_keywords: str,
    days_back: int = 90,
    top_n: int = 20,
) -> List[Dict]:
    """
    技术转移场景专用：搜索近N天内与技术关键词相关的招标信息
    
    参数：
    - tech_keywords: 技术关键词（多词OR关系用|分隔，如"固态电池|储能|新能源"）
    - days_back: 回溯天数（默认90天）
    - top_n: 返回条数（最大50）
    
    返回: 简化后的企业列表，每项含 title, partAName, partBName, 
          projectMoney, publishTime, areaName, projectClass
    """
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    result = search_projects_for_ai(
        keyword=tech_keywords,
        start_date=start_date,
        end_date=end_date,
        page_id=1,
        page_number=min(top_n, 50),
        class_name="招标信息,中标信息",
        search_field="标题",
    )

    projects = []
    if result.get("code") == 200:
        data = result.get("data", {})
        items = data.get("data", []) if isinstance(data, dict) else []
        for item in items:
            part_a = [p.get("name", "") for p in item.get("partAInfo", [])]
            part_b = [p.get("name", "") for p in item.get("partBInfo", [])]
            projects.append({
                "id": item.get("id"),
                "title": item.get("title", ""),
                "partAName": part_a,
                "partBName": part_b,
                "projectMoney": item.get("projectMoney"),
                "publishTime": item.get("publishTime"),
                "areaName": item.get("areaName"),
                "projectClass": item.get("projectClass"),
            })
    return projects


# ─────────────────────────────────────────────
# 主程序（测试用）
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=== 测试：招标搜索接口 ===")
    result = search_projects_for_ai(
        keyword="固态电池|储能",
        start_date="2025-01-01",
        end_date="2026-04-22",
        page_number=5,
    )
    print(f"状态码: {result.get('code')}")
    data = result.get("data", {})
    if isinstance(data, dict):
        print(f"总条数: {data.get('total', 0)}")
        items = data.get("data", [])
        for item in items[:3]:
            print(f"  [{item.get('newsTypeName')}] {item.get('title', '')[:50]}")
            print(f"    发布: {item.get('publishTime')} | 金额: {item.get('projectMoney')}")

    print("\n=== 测试：技术转移便捷搜索 ===")
    companies = search_tender_for_tech_transfer("人工智能|机器学习", days_back=60, top_n=5)
    for c in companies:
        print(f"  甲方: {c['partAName']} | 项目: {c['title'][:40]}")
