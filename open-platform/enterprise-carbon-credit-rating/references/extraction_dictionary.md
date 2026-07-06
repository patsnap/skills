# Extraction Dictionary

Use this file as the internal extraction target. Do not force the user to fill a fixed template.

## Extraction Process

1. Extract values from all supplied materials.
2. Preserve source hints: filename, section/table name, page number when available, and original label.
3. Normalize synonyms to the canonical field names below.
4. Show a confirmation table to the user.
5. Ask for missing required identity fields before scoring.

## Field Status Values

- `已采集`: provided by customer or extracted from materials.
- `已核证`: backed by third-party verification, official platform, audited report, or similar.
- `默认参数`: supplied by industry defaults.
- `用户确认`: user approved the value.
- `未采集数据`: missing and not estimated.
- `不适用`: not applicable to this industry or enterprise.
- `异常待核`: inconsistent or unsupported value requiring confirmation.

## Cannot Remain Missing

These fields must be present before scoring or report generation:

| Canonical field | Chinese label | Common aliases |
|---|---|---|
| `company_name` | 企业名称 | 公司名称、受评企业、企业全称 |
| `unified_credit_code` | 统一社会信用代码 | 统一信用代码、社会信用代码 |
| `industry` | 所属行业 | 行业、行业类型、所属领域 |
| `rating_period` | 评价周期 | 评级周期、评估周期、报告期、评价期间 |

If any of these are missing, ask the user to provide them. Do not proceed to scoring.

## Key Required Rating Fields

If these remain missing and the user chooses `保持缺失`, output `不评级`.

| Canonical field | Chinese label | Common aliases | Why key |
|---|---|---|---|
| `serious_dishonesty_flag` | 是否纳入严重失信主体名单 | 严重失信、失信名单 | one-vote termination |
| `verified_emission_qty` | 经核查碳排放量 | 碳排放量、核查排放量、排放总量 | S and W calculation |
| `enterprise_carbon_intensity` | 企业碳排放强度 | 碳强度、排放强度、单位产值排放 | W calculation |
| `industry_carbon_intensity` | 行业碳排放强度基准值 | 行业基准、行业排放强度 | W denominator |
| `carbon_behavior_total_count` | 碳行为总次数 | 行为总次数、交易/履约/核查总次数 | V denominator |
| `major_environment_penalty` | 重大环境处罚 | 重大环保处罚、重大环境违法 | no-rating trigger |
| `major_bank_bad_record` | 重大银行不良记录 | 银行不良、金融不良记录 | no-rating trigger |
| `carbon_data_fraud` | 碳数据造假 | 数据造假、虚报、篡改 | no-rating trigger |

## Industry Classification

Infer the industry class from explicit labels first, then from enterprise description.

| Industry class | Typical aliases |
|---|---|
| 污水处理行业特例 | 污水处理、城镇污水、工业污水、园区污水、水务运营、污水厂 |
| 高碳排放强度、高转型压力 | 火电、钢铁、水泥、电解铝、煤化工、石油炼制 |
| 中碳排放强度、中等转型压力 | 一般制造、建筑、交通运输、部分化工 |
| 低碳排放强度、低转型压力 | 信息技术、金融、商业服务、教育、医疗 |
| 资源依赖型、生态敏感行业 | 林业、矿业、生态旅游、农业、环境治理 |
| 创新驱动型、绿色技术行业 | 新能源设备、新能源汽车、节能环保、新材料 |

When industry is inferred, show it to the user with the matched aliases and default parameters.

## Enterprise Basic Credit Fields

| Canonical field | Chinese label | Common aliases |
|---|---|---|
| `registration_integrity` | 企业登记信息完整性、准确性 | 登记信息、工商信息、营业执照 |
| `paid_in_capital_ratio` | 股东实缴比例 | 实缴比例、出资比例 |
| `management_credit_record` | 管理层信用记录 | 高管信用、主要管理人员信用 |
| `admin_penalty_records_3y` | 近3年行政监管记录 | 行政处罚、行政监管、行政许可 |
| `civil_litigation_3y` | 近3年民事诉讼记录 | 诉讼记录、司法案件 |
| `enforcement_records` | 被执行记录 | 执行记录、被执行人 |
| `current_ratio` | 流动比率 | current ratio |
| `quick_ratio` | 速动比率 | quick ratio |
| `asset_liability_ratio` | 资产负债率 | 负债率 |
| `roe` | 净资产收益率 | ROE |
| `main_business_margin` | 主营业务利润率 | 营业利润率 |
| `resource_consumption_volatility` | 关键资源消耗波动率 | 水电气波动、资源用量波动 |
| `tax_credit_level` | 纳税信用等级 | 税务评级 |
| `housing_fund_ratio` | 公积金缴纳人数占比 | 公积金比例 |
| `rd_revenue_ratio` | 研发投入占营业收入比例 | 研发投入占比 |
| `patent_count` | 专利数量 | 发明专利、实用新型、外观专利 |
| `registered_trademark_count` | 注册商标数量 | 商标数量 |
| `qualification_awards` | 资质与荣誉数量及级别 | 资质证书、荣誉奖励 |

## Carbon Account Fields

| Canonical field | Chinese label | Common aliases |
|---|---|---|
| `carbon_allowance_qty` | 碳配额量 | 配额、碳配额 |
| `carbon_price` | 碳交易价格 | 碳价、碳市场价格 |
| `ccer_qty` | CCER数量 | 国家核证自愿减排量 |
| `ccer_price` | CCER交易价格 | CCER价格 |
| `verified_carbon_sink_qty` | 经核证碳汇量 | 碳汇量、核证碳汇 |
| `green_certificate_qty` | 绿证/绿电持有量 | 绿证、绿色电力证书、绿电 |
| `power_emission_factor` | 电力排放因子 | 电网排放因子、电力因子 |
| `enterprise_output_value` | 企业产量值或产值 | 产量、产值、营业收入 |
| `industry_carbon_account_value` | 行业碳账户价值 | 行业碳账户值 |
| `industry_output_value` | 行业产量值或产值 | 行业产值、行业产量 |
| `data_error_count` | 核查数据有误次数 | 数据错误次数、核查错误 |
| `purchase_data_false_count` | 购买数据虚报次数 | 虚报次数、购买数据虚报 |
| `green_certificate_delay_count` | 绿证交易未及时履约次数 | 绿证履约延迟 |
| `carbon_trade_delay_count` | 碳交易未及时履约次数 | 碳交易履约延迟 |

## Green Transition Fields

| Canonical field | Chinese label | Common aliases |
|---|---|---|
| `voluntary_project_investment_ratio` | 自愿减排项目投资占比 | 减排项目投资、项目投资占比 |
| `renewable_project_ratio` | 可再生能源项目占比 | 可再生项目比例 |
| `ccus_sink_project_ratio` | CCUS/碳汇项目占比 | CCUS占比、碳汇项目占比 |
| `project_standard_level` | 项目采用标准级别 | VCS、GS、CCER、绿证、项目标准 |
| `risk_coverage_count` | 项目风险应对覆盖类别数 | 风险应对、风险管理 |
| `annual_reduction_target_achievement` | 年度减排量目标达成率 | 减排目标完成率 |
| `reduction_to_emission_ratio` | 减排量占企业碳排放总量比例 | 减排占比 |
| `transition_capex_ratio` | 绿色转型投资占总资本支出比例 | 转型投资占比 |
| `environment_credit_rating` | 企业环境信用评价 | 环保绿牌、蓝牌、黄牌、红牌 |
| `tech_upgrade_investment_ratio` | 技改降碳投资占比 | 技改投资、设备更新投资 |
| `carbon_intensity_decline_yoy` | 万元产值二氧化碳排放量下降率 | 碳强度下降率 |

## Wastewater-Specific Risk Fields

These are model suggestions and should be disclosed as risk prompts, not main-score fields by default:

- `ton_water_energy_consumption`: 吨水综合能耗
- `ton_water_carbon_emission`: 吨水碳排放
- `cod_reduction_carbon_intensity`: 单位COD削减碳排放
- `ammonia_reduction_carbon_intensity`: 单位氨氮削减碳排放
- `sludge_disposal_compliance_rate`: 污泥处置合规率
- `reclaimed_water_reuse_rate`: 再生水利用率
- `biogas_heat_recovery_rate`: 沼气/余热回收率
- `effluent_compliance_rate`: 出水达标率
