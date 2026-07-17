---
name: cn-biopharma-patent-drafting
description: "辅助生物医药发明查新、权利要求设计和申请草拟。适用于：基于发明交底、结构或序列材料开展查新、权利要求设计和CNIPA申请文本初稿撰写；用于代理师复核前的草稿准备。"
---

# CNIPA 专利撰写

使用本技能将用户提供的技术材料转化为 CNIPA 风格申请的专利撰写文件。所有能力声明均须以 `references/source-map.md` 为依据；在提及具体 API 端点或 MCP 工具前，先阅读该文件。

## 不可妥协的要求

- 将用户文件和陈述作为主要来源。不得编造技术特征、实施例、效果、附图或实验数据。
- 如来源缺失或不清晰，应标记为缺失，并询问具体缺失项或明确说明假设。
- 在输出中引用来源：用户文件名、可用时的段落/页码引用、API/工具输出，以及用于能力映射的本地源文件。
- 不得声称 OCR、AI32 或 AI37 能够执行来源映射未支持的功能。
- 不得在对话或交付物中暴露凭据。演示时使用环境变量、MCP 配置或用户本地提供的密钥文件中的已配置凭据；不得编造凭据。
- **免责声明**：所有 AI 生成的专利文件均为草稿。提交 CNIPA 前，必须由合格的中国专利律师或专利代理师复核。AI 不能替代关于可专利性、权利要求范围或审查策略的专业法律判断。

## 本地 API 封装器：调用规则

AI60 云端 OCR、AI32（技术交底书）和 AI37（CNIPA 说明书）均为**本地 API 封装器**，并非 MCP 工具。

- 通过 **Bash 工具**，使用第一层表格和 `references/source-map.md` 中所示的精确 CLI 命令调用。
- 不得通过 ToolSearch 检索它们，它们不会出现在 MCP 工具列表中。
- 不得通过 DeferExecuteTool 调用它们，它们不是 MCP 工具。
- 调用前始终确认封装器文件存在于 `$USERPROFILE/.workbuddy/api-wrappers/{ai60,ai32,ai37}/`。
- **AI60 云端 OCR**：PatSnap 的云端 OCR 服务（`https://connect.zhihuiya.com`）。需要 API 密钥（`--api-key` 或 `AI_API_KEY` 环境变量）。文件模式（`--file PATH`）需要具有上传权限的 API 密钥；URL 模式（`--document URL`）可使用标准 AI60 权限。
- **AI32/AI37**：可通过 `--api-key` CLI 参数或 `AI_API_KEY` 环境变量传入凭据。如两者均不可用，跳过该步骤，并将输出明确标记为**“编排层草稿，不是 API 生成结果”**。

## CNIPA 可专利性预检查

在新颖性评估（步骤 3）之后、权利要求撰写（步骤 5）之前，依据以下 CNIPA 法律基础核验发明：

| 检查项 | 法律基础 | 常见问题 | 处理方式 |
|-------|------------|--------------|--------|
| 新颖性 | 专利法第22条第2款 | 现有技术已公开该发明 | 由步骤 3 的新颖性评估覆盖 |
| 创造性 | 专利法第22条第3款 | 相较现有技术，发明显而易见 | 由步骤 3 的新颖性评估覆盖 |
| 实用性 | 专利法第22条第4款 | 发明不能在产业中制造或使用 | 标记风险并请用户确认实际实施可能性 |
| 客体适格性 | 专利法第25条 | 发现、算法、商业方法、疾病诊断/治疗方法 | 如发明纯属计算/算法且无技术效果，标记风险。方法权利要求应写入具体技术实现步骤。对于疾病治疗方法，应改写为“用于制备……药物的物质/组合物”（制药用途权利要求） |
| 充分公开 | 专利法第26条第3款 | 说明书不足以使本领域技术人员实施发明 | 核验说明书中每个权利要求要素至少具有一个可实施实施例。标记缺少实施细节的权利要求要素。 |
| 权利要求支持 | 专利法第26条第4款 | 权利要求范围宽于说明书支持范围 | 对化合物权利要求，确保马库什范围有覆盖所请求范围的代表性实施例支持。对序列权利要求，确保同一性百分比阈值有覆盖该范围的功能数据支持。 |

如任何检查未通过，记录风险并在继续前询问用户。

## 工作流程

1. 对输入进行分类。
   - 口述想法：要求提供 ASR 转写文本、笔记或用户说明。
   - 草图/图像/扫描版 PDF：如图像中嵌有文字，**先通过 Bash 运行 AI60 云端 OCR**。
     ```bash
     # 在本地文件上运行 OCR（输出 Markdown）：
     python "$USERPROFILE/.workbuddy/api-wrappers/ai60/cli.py" smart_doc --file /path/to/document.pdf [-o output.md]
     # 或使用 URL 模式（无需上传权限）：
     python "$USERPROFILE/.workbuddy/api-wrappers/ai60/cli.py" smart_doc --document "https://..." [-o output.md]
     ```
     **说明**：AI60 是 PatSnap 的云端 OCR 服务（通过 `--api-key` 或 `AI_API_KEY` 环境变量提供 API 密钥）。文件模式需要具有上传权限的 API 密钥；URL 模式可使用标准 AI60 权限。如服务不可用，对于原生 PDF 回退使用 Read 工具。
   - 简短交底：直接解析文本。
   - 既有草稿：除非需要撰写改进，否则保留用户原有表述。

2. 规范化为 `tech_solution`。
   - 根据用户材料生成忠实的技术方案文本。
   - 将不确定性单独保留为 `open_questions`；不得静默填补缺口。

3. **撰写前新颖性评估（必需，不得跳过）**。

   本步骤在任何权利要求撰写或 AI32/AI37 生成**之前**执行。目标是判断发明是否具有合理的新颖性/创造性前景，并为权利要求范围提供依据。并行运行**所有适用通道**：

   **通道 A：通用文本新颖性检索**（始终运行）
   - **默认方式（一键式）**：将 `tech_solution` 文本提交给 `novelty_lite_submit`，然后轮询 `novelty_lite_get` 直至完成。该方式自动运行 summary → feature_extract → keywords_extract → search → feature_comparison → report_generate。
   - **手动方式（需要细粒度检查时）**：`novelty_feature_extract` → `novelty_keywords_extract` → `novelty_lite_search` → `patsnap_search`（补充）→ `novelty_feature_comparison` → `novelty_summary` → `novelty_lite_report_generate`。完整工具链见“工具架构”。
   - 选择**一种**方式。同一 `tech_solution` 不得同时运行两种方式。
   **通道 D：药物情报背景**（当发明涉及生物医药药物、靶点、疾病或临床应用时运行）
   - 使用 `ls_ner_nor_normalize` 规范化药物/靶点/疾病名称，然后使用 `ls_drug_search`（竞品药物）、`ls_clinical_trial_search`（临床背景）、`ls_drug_deal_search`（商业格局）、`ls_epidemiology_vector_search`（疾病患病率）、`ls_organization_pipeline_fetch`（竞争对手管线）。详见“工具架构 → 第二层”。
   - **需要通道 D 的原因**：通道 A 仅按文本和关键词检索，无法发现仅在药物数据库中按药物名称、靶点或疾病适应症索引的药物特异性现有技术。药物情报数据为确定合适的权利要求范围和说明书细节层级提供关键背景。

   **通道 B：化学结构新颖性检索**（当发明涉及小分子化合物、药物组合物或化学骨架时运行）
   - 如用户提供 SMILES、化合物名称或结构图片，提取 SMILES 表示。
   - 运行 `ls_structure_search`（SIM，阈值 >= 0.7）调研现有技术化合物格局。
   - 使用申请人的核心骨架运行 `ls_structure_search`（EXT，子结构模式），检查该骨架本身是否已在现有技术中公开。
   - 使用 `ls_patent_structure_fetch` 从最相关的现有技术专利中提取化合物。
   - 使用 `ls_chemical_mcs_analyze` 识别申请人化合物与现有技术之间的共有骨架。
   - 对相关现有技术专利使用 `ls_sar_submit` + `ls_sar_fetch`，理解 SAR 趋势。
   - 对申请人的先导化合物使用 `ls_admet_predict`，获取支持创造性的辅助数据。
   - **需要通道 B 的原因**：通用新颖性 MCP（通道 A）不能按结构匹配化合物。仅凭通道 A 会遗漏文本看似不同、但结构相同或近似相同的化合物。

   **通道 C：生物序列新颖性检索**（当发明涉及蛋白质、核酸、抗体或修饰序列时运行）
   - 如用户提供序列，识别 sequence_type（NUCLEOTIDE 或 PROTEIN）。
   - 运行 `ls_sequence_search_submit`（database=ALLPATENT）核查序列现有技术。使用 `ls_sequence_search_check_status` 轮询直至 SUCCESS，然后通过 `ls_sequence_search_get_results` 获取结果。
   - 使用 `ls_sequence_alignment`（PSA）将申请人序列与最接近的现有技术命中进行比对。
   - 对于抗体发明，使用 `ls_antibody_antigen_search`（target_name = 抗原）调研抗体现有技术。
   - 对于修饰序列，使用 `ls_modification_search_submit` 核查修饰序列现有技术。
   - 使用 `ls_patent_sequence_fetch` 从引用的现有技术专利中提取序列。
   - **需要通道 C 的原因**：通用新颖性 MCP（通道 A）不能按同一性/覆盖度匹配序列。与现有序列仅相差一个氨基酸、但同一性达到 95% 的序列，仅用通道 A 的文本检索无法发现。

   **新颖性评估决策**：
   - **GREEN**：所有适用通道均未发现接近的现有技术 → 可有信心地进入步骤 4，权利要求范围可以更宽。
   - **YELLOW**：发现接近的现有技术，但已识别区别特征 → 进入步骤 4，但应围绕区别特征撰写更窄的权利要求。记录现有技术和区别分析。
   - **RED**：发明看似已被现有技术公开或相对于现有技术显而易见 → **停止并告知用户**。展示现有技术发现，说明新颖性/创造性风险，并询问是否：
     - (a) 修改技术方案以引入区别特征；
     - (b) 撰写限于区别特征的窄权利要求；
     - (c) 依用户明确指示继续（记录风险）。

   **步骤 3 的输出**：新颖性评估备忘录，包含：
   - 已运行的通道和已使用工具（附检索参数和结果数量）；
   - 每个通道的主要现有技术命中（视情况提供专利号、化合物 InChIKey 或序列 ID）；
   - 已识别的区别特征；
   - 风险等级（GREEN / YELLOW / RED）和建议的权利要求范围；
   - 可能截断结果的 API 限制或分页上限。

4. 生成或补全技术交底书。
   - 使用 **Bash：AI32 封装器** 从 `tech_solution` 生成技术交底书：
     ```bash
     node "$USERPROFILE/.workbuddy/api-wrappers/ai32/cli.mjs" create_and_wait --tech_solution "..." --output disclosure.docx
     ```
   - 如 AI32 封装器或凭据不可用，在编排层生成交底书，并标记为**“编排层草稿，不是 AI32 结果”**。
   - AI32 不是初始权利要求生成器；它提供结构化技术交底书内容。

5. 在编排层创建初始权利要求文本。
   - 根据已核验的技术交底书起草初始独立权利要求和从属权利要求框架。
   - **权利要求范围必须以新颖性评估（步骤 3）为依据**。如为 YELLOW，围绕区别特征起草更窄的权利要求。如发明涉及化合物，根据 MCS 分析考虑马库什权利要求与特定化合物权利要求。
   - 记录支撑每项权利要求要素的交底书事实。

6. 仅在 `claim` 和 `disclosure` 输入均已具备后，通过 **Bash 运行 AI37 CNIPA 撰写**。
   ```bash
   python "$USERPROFILE/.workbuddy/api-wrappers/ai37/cli.py" run_full_flow --claim "..." --disclosure "..." [--title "发明名称"] [--api-key SK]
   ```
   - **`--title` 限制**：必须不超过 50 个字符。如省略或过长，CLI 自动截断为 47 个字符加“...”。
   - 如 AI37 封装器或 `AI_API_KEY` 不可用，在编排层生成说明书，并标记为**“编排层草稿，不是 AI37 结果”**。

7. 生成交付物。
   - 说明书草稿、权利要求书草稿、摘要草稿，以及附图/图示说明。
   - 必须将**新颖性评估备忘录**（来自步骤 3）作为附录纳入。
   - 包含来源附录，将每项主要技术特征映射至用户输入或 API 输出。
   - 对于 Word/PDF 输出，使用 Documents/PDF 技能并对生成文件进行视觉核验。

## CNIPA 说明书结构（必需）

每份 CNIPA 说明书草稿必须按以下顺序包含这些章节：

1. **技术领域**：用一句话说明发明所属技术领域。
2. **背景技术**：描述本发明所要解决的现有技术及其不足。不得在此处写入申请人自身未公开的既有工作。
3. **发明内容**：必须包括：
   - **技术问题**：发明所要解决的问题。
   - **技术方案**：与独立权利要求相对应，且必须与权利要求语言一致。
   - **有益效果**：具有支持数据或推理的技术效果。每项效果均须可追溯至具体技术特征。
4. **附图说明**：列出每幅附图及其内容。此处不写结构说明（结构说明应置于具体实施方式）。
5. **具体实施方式**：每项独立权利要求至少提供一个可实施实施例。优先提供展示完整范围的多个实施例。对化合物发明，在可用时提供合成实施例和生物学测试数据；对序列发明，提供序列表和功能验证。

## 摘要要求

- CNIPA 摘要：不超过 300 个汉字（含标点）。
- 必须包含：技术领域 + 技术方案 + 主要技术效果。
- 不得包含：商业性主张、主观评价或对附图的引用。
- 从说明书附图中选取一幅作为摘要附图。

## 序列表要求

当发明涉及含有不少于 10 个核苷酸或不少于 4 个氨基酸的核苷酸或氨基酸序列时：

- CNIPA 要求提交一份符合 WIPO ST.25 格式的独立序列表。
- 每条序列必须具有唯一的序列标识符。
- 序列表是与说明书分开的文件，通过序列标识符交叉引用。
- 如用户提供序列，确认格式并准备序列表。如用户未以 ST.25 格式提供序列，标记为必需交付物缺口。

## 化学结构处理（通道 B 参考细节）

本节为步骤 3 中通道 B 使用的工具提供详细参数指引。

- `ls_structure_search`：使用 `type=SIM` 且 `threshold >= 0.7` 获取广泛格局；使用 `threshold >= 0.95` 进行近似精确匹配。使用 `type=EXT` 进行子结构/精确检索，并设置 `include_tautomer=true` 以覆盖互变异构体。
- `ls_structure_fetch`：按 InChIKey 列表批量获取（最多 100 个）。返回 canonical_smiles、molecular_formula、compound_name 和专利关联信息。
- `ls_patent_structure_fetch`：使用 offset+limit 翻页（每页最多 100 条）。用于核验现有技术专利是否实际公开了所请求的化合物。
- `ls_chemical_mcs_analyze`：输入申请人化合物和现有技术化合物的 SMILES 列表。如 MCS 骨架具有新颖性 → 可考虑马库什式权利要求；如仅特定 R 基不同 → 应采用更窄的化合物权利要求。
- `ls_sar_submit` + `ls_sar_fetch`：异步操作。使用专利 pn 提交，轮询至 SUCCESS。用于理解现有技术 SAR 并避免将权利要求范围收窄过度。
- `ls_admet_predict`：输入 SMILES 列表（1–100 个）。用于生成支持创造性的辅助数据（例如相较现有技术具有意料不到的 ADMET 优势）。

## 生物序列处理（通道 C 参考细节）

本节为步骤 3 中通道 C 使用的工具提供详细参数指引。

- `ls_sequence_search_submit`：使用 `database=ALLPATENT` 进行全面检索；使用 `database=CLAIMS` 仅检索权利要求。设置 `identity` 阈值（如近似精确匹配为 0.95，广泛检索为 0.80），并适当设置 `coverage` 阈值。异步操作：返回 job_id。
- `ls_sequence_search_check_status`：使用 job_id 轮询。返回 SUCCESS/RUNNING/FAILED。调用 get_results 前等待 SUCCESS。
- `ls_sequence_search_get_results`：支持翻页。按同一性/覆盖度区间进行事后筛选，并按同一性降序排列。
- `ls_sequence_fetch`：按 sequence_number 列表批量获取（最多 100 条）。返回完整序列文本、物种、基因、药物和 is_antibody 标记。
- `ls_sequence_alignment`：使用 `alignment_type=PSA` 进行成对比对（申请人与最接近现有技术）；使用 `alignment_type=MSA` 进行多序列比对。支持 NUCLEOTIDE 和 PROTEIN 类型。
- `ls_patent_sequence_fetch`：使用 offset+limit 翻页（每页最多 100 条）。用于从现有技术专利中提取全部序列。
- `ls_antibody_antigen_search`：需要 `target_name`。返回重链/轻链序列、专利信息、物种和基因符号。使用分面筛选进一步细化。
- `ls_modification_search_submit`：需要 `modification_location` 列表（位置 + modification_name）。异步操作：返回 job_id。之后调用 check_status 和 get_results。

## 完整获取规则

如撰写任务包括新颖性、可专利性或现有技术获取，不得只选取方便的一小部分。必须翻页直至来源耗尽或达到 API 限制，并报告：

- 检索输入和筛选条件；
- 工具在可用时报告的总记录数；
- 已获取的页码/偏移量；
- 端点施加的上限；
- 去重规则；
- 仅因明确 API 限制或用户约束而省略的记录。

## 工具架构（三层工具架构）

工具分为三个层级。**工作流程步骤中仅指定第一层工具。** 第二层工具按条件触发。第三层工具存放在 `references/source-map.md` 中，并通过 ToolSearch 按需加载。

### 第一层：核心工具（固定在流程步骤中）

| 步骤 | 操作 | 工具 | 说明 |
|------|--------|------|-------|
| 1. OCR | 图像/扫描版 PDF 识别 | AI60 CLI：`python "$USERPROFILE/.workbuddy/api-wrappers/ai60/cli.py" smart_doc --file PATH [-o output.md]` | 云端 OCR 服务，需要 API 密钥。自动识别文件类型（PDF/图像/Office）。文件模式需要上传权限；URL 模式（`--document URL`）可使用标准权限。原生 PDF 回退使用 Read 工具。 |
| 2. 规范化 | 生成 tech_solution 文本 | （编排层，无工具） | |
| 3. 通道 A（默认） | 一键式新颖性评估 | `novelty_lite_submit` → `novelty_lite_get` | **优先使用。** 提交 tech_solution，轮询直至完成，自动执行通道 A 的所有步骤。 |
| 3. 通道 A（手动） | 分步新颖性评估 | `novelty_feature_extract` → `novelty_keywords_extract` → `novelty_lite_search` → `patsnap_search`（补充）→ `novelty_feature_comparison` → `novelty_summary` → `novelty_lite_report_generate` | 仅在需要细粒度检查时使用。 |
| 3. 通道 B | 化学结构新颖性 | `ls_structure_search`（SIM）→ `ls_structure_search`（EXT）→ `ls_patent_structure_fetch` → `ls_chemical_mcs_analyze` → `ls_sar_submit`+`ls_sar_fetch` → `ls_admet_predict` | 仅用于化合物发明。 |
| 3. 通道 C | 生物序列新颖性 | `ls_sequence_search_submit` → `ls_sequence_search_check_status` → `ls_sequence_search_get_results` → `ls_sequence_alignment` / `ls_antibody_antigen_search` / `ls_modification_search_submit` | 仅用于序列发明。 |
| 4. 可专利性 | 依据专利法第 22/25/26 条进行预检查 | （编排层，无工具） | 如 IPC 范围不清楚，使用 `classification_description`（7cc6ae）。 |
| 5. 技术交底书 | 生成技术交底书 | AI32 CLI：`node "$USERPROFILE/.workbuddy/api-wrappers/ai32/cli.mjs" create_and_wait --tech_solution "..." [--api-key KEY] [--output disclosure.docx]` | 通过 CLI 参数或环境变量传入凭据。 |
| 6. 权利要求 | 起草初始权利要求文本 | （编排层，无工具） | 范围由步骤 3+4 决定。 |
| 7. 说明书 | 生成 CNIPA 说明书 | AI37 CLI：`python "$USERPROFILE/.workbuddy/api-wrappers/ai37/cli.py" run_full_flow --claim "..." --disclosure "..." [--title "名称"] [--api-key SK]` | 通过 `--api-key` 或 `AI_API_KEY` 环境变量传入凭据。`--title` 不超过 50 个字符（自动截断）。需要 claim + disclosure 输入。 |

### 第二层：扩展工具（条件分支触发）

**触发条件：发明涉及生物医药药物、靶点、疾病或临床应用（通道 D）**
- `ls_ner_nor_normalize`：在查询药物情报工具前规范化药物/靶点/疾病名称。
- `ls_drug_search`：查找在研竞品药物（用于确定权利要求范围：III 期及以上 → 权利要求更窄）。
- `ls_clinical_trial_search`：查找临床试验背景（用于确定充分公开所需的说明书细节层级）。
- `ls_drug_deal_search`：了解商业格局（用于评估权利要求价值）。
- `ls_epidemiology_vector_search`：获取疾病患病率数据（支持说明书中的适应症范围）。
- `ls_organization_pipeline_fetch`：获取竞争对手企业的药物管线。
- **通道 D 补充通道 A，而非替代通道 A。** 始终先运行通道 A。通道 D 补充专利数据库未收录的药物研发背景。

### 第三层：参考工具（按需加载）

以下工具位于 `references/source-map.md` 中，需要时通过 ToolSearch 加载：
- 专利内容（958a46）：`tech_summary`、`description`、`claims`、`legal_status`、`family`、`bibliography`
- 材料/分类（7cc6ae）：`tech_problem_benefit_summary`、`technology_topic`、`seic_classification`
- 药物情报：`ls_drug_fetch`、`ls_target_fetch`、`ls_disease_fetch`、`ls_organization_fetch`、`ls_news_vector_search`、`ls_paper_vector_search`、`ls_patent_vector_search`、`ls_patent_search`、`ls_translational_medicine_search`、`ls_fda_label_vector_search`

## 互斥规则（必须遵守）

1. **`novelty_lite_submit` 或 6 步手动流程**：同一 `tech_solution` **绝不**同时运行两者。在步骤 3 开始时选择一种方式并全程坚持。默认使用 `novelty_lite_submit`。
2. **始终运行通道 A。** 通道 B/C/D 是补充，而非替代。不得跳过通道 A。
3. **每次专利详情获取只用一个工具。** 同一专利不得同时调用 `patsnap_fetch` 和 `958a46.description`；二选一。
4. **每次技术摘要操作只用一个工具。** 同一专利不得同时调用 `958a46.tech_summary` 和 `7cc6ae.tech_problem_benefit_summary`；二选一。
5. **`ls_patent_search`（pharma_intelligence）不能替代 `patsnap_search`。** 前者仅检索生物医药专属索引；始终运行 `patsnap_search` 以获得全面的专利覆盖。
6. **AI32（本地封装器）与 MCP 工具的区别**：AI32 从 `tech_solution` 生成技术交底书。不得使用 `958a46.description` 或 MCP 工具生成交底书，它们只获取既有专利内容，不生成新的技术交底书。
7. **AI37（本地封装器）与 MCP 工具的区别**：AI37 根据 `claim` + `disclosure` 生成 CNIPA 说明书。不得使用 MCP 工具生成说明书文本。AI37 是通过 Bash 调用的本地封装器，不是 MCP 工具。

## 交付物完整性

每份最终答复或文件必须区分：

- 用户提供的事实；
- OCR 提取的文本；
- API 生成的技术交底书；
- 编排层起草的权利要求；
- AI37 生成的 CNIPA 输出；
- 智能体分析或建议。
