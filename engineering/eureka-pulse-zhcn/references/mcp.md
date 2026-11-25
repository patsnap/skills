# MCP 与文件管理

## 工具职责

| 任务 | eureka-pulse Tool |
|---|---|
| 生成基础参数 | `generate_mcp_brief_params_from_intent` |
| 创建 | `create_personal_mcp_brief` |
| 查询 | `list_mcp_briefs`、`get_mcp_brief_info` |
| 修改及计划运行设置 | `update_personal_mcp_brief` |
| 运行 | `run_mcp_personal_brief`，按报告目标传入 `period_type=month|week`；同一服务实际提供对应的 `run_mcp_month_brief` 或 `run_mcp_week_brief` 时优先使用 |
| 状态与周期结果 | `get_mcp_brief_run_status`、`get_mcp_brief_data` |
| 删除 | `delete_mcp_brief` |

- **报告周期与计划运行**：监控配置的 `period_type=week` 保持周计划；报告默认目标为上一个完整自然月，查询与运行请求从 `target.json` 读取周期，不能沿用配置中的周周期。用户明确要求周报时使用周目标。
- **历史读取与图表**：月报按[历史模块](history.md)逐期调用 `get_mcp_brief_data`，默认读取包含目标月的最近十二个完整自然月；已有简报的周报读取最近八个完整自然周。已取得的目标期完整响应直接登记复用。独立统计程序计算有来源的数量，[图表模块](charts.md)负责绘图；有可比较期次时显示历史变化，没有可比历史时显示当期分布。历史缺失不触发运行，HTML 渲染不触发远程统计或历史查询。

## MCP 请求语言

- **固定语言**：本 Skill 的 MCP HTTP 请求固定发送 `X-Site-Lang: CN`，覆盖整个连接生命周期中的初始化、工具发现与业务调用。输出语言由连接设置管理；参数生成的 `input` 按[创建模块](create.md#步骤二生成与检查配置)保留用户业务需求。
- **详情读取范围**：`get_mcp_brief_info` 与 `get_mcp_brief_data` 均使用此 Header。首次读取、任务完成后的再次读取、恢复执行，以及历史窗口内每个月或每周的读取，都使用当前已核验的中文连接；连接重新建立或切换入口后重新检查。该 Header 由传输连接发送，Tool 业务参数保持当前 schema。
- **设置位置**：语言 Header 由实际提供 HTTP 传输的连接发送。Tool 业务参数、用户输入语言和独立脚本中的 Header 设置分别检查；宿主直接调用与文件调用均须覆盖。其他连接 Header 与鉴权保持当前有效配置。

### 详情请求的程序入口

- **统一发送层**：SDK 文件调用使用下文的脚本。`http_transport.py` 在创建 HTTP 客户端和每次实际发送前设置唯一的 `X-Site-Lang: CN`，检查目标服务地址，并记录对应 HTTP 响应。使用宿主原生 Tool 时，核验该宿主当前连接支持的 Header 配置与加载方式；豆包按下文原生连接步骤执行。
- **Codex 桥接**：`codex_bridge.js` 遇到 `get_mcp_brief_info` 或 `get_mcp_brief_data` 时调用 `call_mcp.py`，读取明确指定的 `connection` 或 `codexConfig`；没有指定时读取当前 Codex 配置。其他 Tool 保留原有宿主调用方式。连接中的认证环境变量须真实可用；缺少时停止执行，不构造身份值。
- **Desktop 桥接**：`desktop_bridge.py` 的两个详情 Tool 同样进入 HTTP 发送层，读取当前 Desktop 服务地址与 Header。使用明确的 `bearer_token` 时直接沿用；使用宿主管理的 `credential_provider` 时，由宿主提供 `--connection <HTTP认证连接.json>`，程序严格检查其地址与当前 Desktop 服务一致。没有取得可用认证时停止执行。其他 Tool 继续使用宿主提供的 `eureka_tools.call`。
- **stdio 适配器**：详情请求通过内置 `stdio_bridge.py` 使用官方 MCP SDK 转发到明确的上游 HTTP 连接。只有该适配器支持的 stdio 配置可以用于此文件调用入口；缺少 HTTP 目标或发送记录时停止执行。
- **豆包原生连接**：豆包的 `execute_defer_tool` 使用宿主管理的个人 MCP 连接，HTTP Header 设置在该连接的 `mcp_config.headers`。配置与验证按[豆包原生连接](#豆包原生连接)执行，认证继续由豆包管理，原始响应使用宿主返回的完整内容或结果文件保存。
- **请求记录**：每次调用的 `http-requests.jsonl` 保存发送阶段、请求序号、HTTP 方法、RPC 方法、Tool 名称、语言值和响应状态码。记录不包含认证值、请求业务正文或响应正文；完整 MCP 响应单独保存在 `response.json`。结果中的 `http_audit.verification=httpx_request_and_response` 表示检查了实际客户端请求及对应响应；保存连接配置的检查结果单独记录。

### 步骤一：检查实际调用连接

1. **确定执行入口**：参数生成、查询及运行可能使用宿主直接 Tool，大型参数可能通过宿主文件调用提交。列出本次实际使用的入口与连接来源，在首次业务请求前完成对应连接检查。只执行当前宿主对应的检查：Eureka Desktop 使用步骤二至步骤四，Codex 与 stdio 使用步骤五，豆包使用下文原生连接步骤。
2. **配置 Desktop 连接**：Eureka Desktop 的直接 Tool 和 `eureka_tools.call` 使用 Desktop 管理的连接。根据当前 Desktop 数据目录找到 `mcp/.state/servers.json`，检查 `servers["eureka-pulse"].transport.headers`；将语言 Header 设置为唯一的 `X-Site-Lang: CN`，保留地址、认证提供方和其余配置。移除该连接中不适用的 `X-Language`。不得把其他客户端的配置作为 Desktop 连接检查依据。
3. **重新加载 Desktop 连接**：连接发生修改后，读取宿主 `mcp` 工具的当前 schema，使用其连接刷新能力加载当前配置，并重新读取连接设置。宿主说明新连接需要后续轮次生效时，保存当前执行位置及继续条件，等待连接可用。刷新后语言设置缺失或无法确认当前活动连接时，停止后续业务提交并说明原因。
4. **执行 Desktop 文件检查**：在宿主直接调用前执行以下命令；`desktop_bridge.py` 在每次提交前执行相同检查。检查失败时立即终止，不能继续提交业务请求。

   ```bash
   python scripts/monitor.py check-connection --desktop-config <Desktop数据目录>/mcp/.state/servers.json
   ```

   - 程序检查连接已启用、传输类型为 `streamable_http`、语言 Header 唯一且值为 `CN`，并返回已检查的配置路径。文件调用的检查结果保存到本次调用目录的 `connection.json`。
   - 检查结果中的 `verification=saved_connection`、`wire_verified=false` 明确表示仅核验保存的连接配置。实际请求证据需要宿主传输日志或请求检查能力提供；没有取得时完整保留这一限制，不能声称已验证实际发送的 Header。
5. **检查其他宿主入口**：Codex 的宿主原生调用检查当前 `mcp_servers["eureka-pulse"]` 连接，更新后按宿主要求重新加载。详情文件调用直接通过统一 HTTP 发送层读取配置并设置语言 Header；认证环境变量按实际配置解析。stdio 使用内置适配器及明确的上游 HTTP 连接，不接受无法检查发送过程的 stdio 进程。

#### 豆包原生连接

- **适用范围**：当前豆包使用 `execute_defer_tool` 调用个人自定义 MCP 连接时，使用本节核验语言设置。输入为本次实际连接名称与身份、原服务地址和已有认证状态。

1. **定位连接**：在豆包的连接器管理中找到本次 `eureka-pulse` Tool 所属连接，打开“编辑自定义连接器”。核实连接身份与服务地址，保留现有其他设置。当前界面没有该编辑入口时记录具体限制，不使用其他应用的连接配置证明豆包设置。
2. **设置语言 Header**：在“自定义 Headers”中添加一项，“Header 名称”填写 `X-Site-Lang`，“Header 值”填写 `CN`。已有同名或大小写不同的语言 Header 时编辑为唯一的一项；保留其余有效 Header。该字段属于连接配置 `mcp_config.headers`，业务 Tool 参数保持当前 schema。
3. **保存与加载连接**：点击“保存”，等待连接变更处理结束并确认状态为已连接。豆包的个人连接器更新流程会比较包括 Header 在内的 HTTP 配置；连接参数变化进入连接更新流程。再次打开配置确认语言项仍为 `CN`。保存成功但连接更新或授权尚未完成时，保留继续所需条件并停止依赖调用。
4. **执行只读核验**：通过当前原生连接调用 `get_mcp_brief_info`，参数只包含真实 `pulse-id`；按需读取 `get_mcp_brief_data`，使用目标文件中的身份与周期。保存完整原始响应及校验值。宿主返回完整结果文件路径时直接引用或逐字节复制该文件；只包含预览时继续取得完整结果。
5. **记录证据范围**：记录豆包版本、连接身份、服务地址、已保存的语言项、连接状态和对应只读调用。已保存配置标记 `verification=saved_connection`、`wire_verified=false`；只有宿主传输日志或服务端请求记录能够证明该次 HTTP 请求 Header 时，才记录已验证实际发送。响应内容语言单独检查，旧结果的语言不作为请求 Header 的证据。凭据由豆包管理，日志不保存认证内容。

- **输出与交接**：将当前连接检查结果、完整原始响应路径及校验值交回所属操作模块。平台没有提供受支持的连接编辑、结果保存或请求检查能力时，记录当前缺少的具体能力；继续执行条件由对应步骤明确管理。

### 步骤二：核验服务生成语言

1. **保存原始内容**：按本模块的文件规则保存完整请求、原始响应及校验值。
2. **检查生成内容**：参数生成后，AI 阅读 `summary_angle`、`ai_fields` 的显示名称与提取说明，以及重点规则和目录中的自然语言内容，确认采用中文。公司英文全称、identifier、检索表达式、引用原文和专用名词按业务需要保留。查询旧配置或旧周期结果时，其保存语言不能证明当前连接的请求语言。
3. **处理语言不符**：保留原始响应，记录实际入口、连接检查结果及不符字段，暂停依赖该配置的创建与更新。检查活动连接及服务语言处理，修正后重新执行必要的参数生成；不能翻译或改写原始响应来通过语言检查，也不能重复创建监控或触发已有周期任务。

- **交接结果**：连接检查信息与原始响应交给当前操作模块。保存配置检查、实际请求 Header 核验和返回内容语言核验分别记录其结果及证据范围。

## 目标定位与配置来源

- **输入**：用户提供的名称或 ID、操作目的。

1. 使用 `list_mcp_briefs`，固定传入 `pulse_type=PERSONAL_MCP`。
2. 结合真实 `pulse_id`、`title`、`description` 唯一定位。有歧义时由用户选择，不直接选取同名结果。
3. 按本模块的 [MCP 请求语言](#mcp-请求语言)检查实际连接后，调用 `get_mcp_brief_info` 取得最新完整配置，核对目标为 `PERSONAL_MCP`；已有监控的查看配置、修改、报告，以及创建后的配置读取均执行此要求。配置身份读取外层 `pulse_id`，完整显示配置同时读取外层及 `template_custom`，使用内置 `extract --kind config` 处理。

- **输出与交接**：返回实际名称、ID、类型、完整配置及保存路径，交回当前操作模块。

## 环境与目录

1. 使用 Python 3.11 或更新版本。检查 `requirements.txt` 中的依赖，详情发送与 stdio 适配使用 `mcp>=2.3,<3` 和 `httpx2>=2.16,<3`。优先使用已经满足要求的环境；需要安装时更新当前可复用环境中的依赖，并完成版本检查。
2. 宿主启用任务计划检查时，在执行任务工具前按其 schema 创建当前任务计划。在 Eureka Desktop 使用 `todolist` 的 `replace_plan`；这是宿主工具的任务记录功能。检查 `skills.run_script` 的当前参数格式：使用 `value_kind=literal` 时必须提供 `value_ref`；直接传字符串数组只适用于宿主明确接受的接口。
3. 执行 `python scripts/monitor.py init --root <工作目录>`，接收返回的绝对 `workspace` 路径。程序创建执行目录、`calls/` 和 `fetch/`，后续直接复用返回路径。
4. 需求保存为 `requirements.json`，其中 `intent_input` 记录业务意图文字，`report_request` 记录当前报告请求，`schedule_request` 记录宿主任务要求。当前目标保存为 `target.json`，当前配置的业务副本为可选的 `config.json`。完整请求与原始响应保存在 `calls/<调用ID>/arguments.json`、`response.json`；响应校验值保存在 `response.ref.json`。宿主每周任务的实际结果保存为 `schedule.json`。报告输入清单为 `report-inputs.json`，交付文件按[报告主题、日期范围和类型](html.md#步骤二自动生成)命名，配套同名检查文件；日志为 `events.jsonl`，当前执行位置为 `state.json`。
5. 报告输入清单引用真实配置响应、真实周期响应及目标文件的绝对路径和 SHA-256。渲染直接读取这些文件，来源变更必须重新执行输入准备和检查。原始响应保留所有字段及实际状态，禁止重写其配置、身份、周期、记录或业务状态。提取业务对象只生成单独的派生文件，输出路径不能覆盖来源。
6. HTML 生成入口直接读取本 Skill 的内置模板、基础样式、主题和脚本。检查安装资源是否完整时使用 `monitor.py check-report-assets`，返回当前 `assets` 目录及基础样式的 SHA-256；缺少本 Skill 的必需资源时按返回文件名修复安装。

## 从文件提交完整参数

- AI 负责形成业务参数文件并明确服务、Tool 和绝对路径。底层调用服务或内置 MCP SDK 客户端直接读取文件，完整提交参数；提交阶段不要求 AI 重写参数。
- 已有平台提供文件参数调用能力时优先使用该能力，按实际说明记录具体入口和返回文件。
- 当前 Codex 的 `functions.exec` 加载内置 `scripts/codex_bridge.js`。两个详情 Tool 由 HTTP 发送脚本读取完整参数文件并保存原始响应；其他 Tool 使用原有宿主连接与鉴权，分段完成文件交接。
- Eureka Desktop 通过当前 Python 工具的脚本路径与参数接口运行内置 `scripts/desktop_bridge.py`，使用 `--desktop-config` 指定当前连接配置。详情调用由统一 HTTP 发送层管理；其他 Tool 使用宿主提供的 `eureka_tools.call` 环境。
- 平台通用的内置入口为 `scripts/call_mcp.py`：使用官方 MCP Python SDK，读取连接配置和参数文件，按服务当前输入 schema 检查后提交一次请求，保存原始响应与调用元数据。连接与鉴权配置由当前宿主提供，凭据不写入 Skill。

### Eureka Desktop 文件调用

使用当前 Python 工具接受的脚本调用格式，指定内置脚本及以下参数：

```bash
python scripts/desktop_bridge.py --desktop-config <Desktop数据目录>/mcp/.state/servers.json --workspace <执行目录> --tool get_mcp_brief_data --arguments <完整参数.json>
```

- Desktop 使用宿主管理认证时，在以上命令增加 `--connection <宿主提供的同一服务HTTP认证连接.json>`。该文件采用下文 HTTP 连接字段，程序核对服务地址后解析认证；缺失认证时保持未执行状态，不切换服务环境。
- 默认月报查询参数文件内容示例：`{"pulse-id":"<真实ID>","period_type":"month","period":"<YYYYMM>"}`；周报使用 `period_type=week` 和 `YYYYWW`。实际运行使用真实目标文件中的 ID 与周期。
- 查询配置只提交 `pulse-id`；查询状态只提交真实 `run-id`。当前服务的通用个人运行 Tool 为 `run_mcp_personal_brief`，提交 `pulse-id`、目标 `period_type` 和 `period`；周期专用 Tool 仅提交 `pulse-id` 和 `period`。使用专用接口前核实同一连接确实提供该 Tool，保留当前服务环境。
- 已经明确的公司和产品直接传入参数生成 Tool。仅在主体确有歧义且需要公司检索时，加载该检索 Tool 的当前 schema，并按实际参数结构查询。
- 每次调用使用独立目录，以独占创建方式保存 `response.json`，成功及失败响应均保留。返回响应路径、校验值及调用状态；后续直接复用返回路径。

### Codex 本机配置示例

在 `functions.exec` 中加载本地桥接函数，随后调用；代码中的路径替换为当前实际路径：

- 列表查询示例的完整参数文件内容为 `{"pulse_type":"PERSONAL_MCP"}`。
- 详情查询可以在桥接选项中传入 `codexConfig: '<当前Codex配置路径>'` 或 `connection: '<宿主提供的HTTP连接.json>'`。脚本返回原始响应路径及 HTTP 请求检查结果；直接使用这些返回值继续处理。

```javascript
const source = await tools.exec_command({cmd: "cat '<Skill目录>/scripts/codex_bridge.js'", max_output_tokens: 6000});
if (source.exit_code !== 0) throw new Error('无法读取桥接程序');
const callPulse = eval(source.output);
text(await callPulse(tools, {python: '<Python路径>', skill: '<Skill目录>',
  workspace: '<执行目录>', tool: 'list_mcp_briefs', arguments: '<完整参数.json>'}));
```

### MCP SDK 文件调用

宿主没有上述编排能力时，使用官方 SDK 的命令行入口：

```bash
python scripts/call_mcp.py --codex-config <Codex配置文件> --server eureka-pulse --tool list_mcp_briefs --arguments <完整参数.json> --workspace <执行目录>
```

- `--codex-config` 读取 TOML 的 `mcp_servers[server]`，支持 HTTP URL、`http_headers`、`env_http_headers`、`bearer_token_env_var`，以及内置适配器的 stdio 配置。HTTP 连接也接受宿主明确提供的 `bearer_token`；认证内容不写入业务日志。
- 其他宿主使用 `--connection <连接.json>`，文件内容为单个 MCP 服务连接对象，采用相同字段。HTTP 必须使用宿主实际提供的地址和鉴权；程序不猜测地址。
- 返回调用目录、响应文件和状态；后续从响应文件提取正式配置或资料，不把日志作为业务输入。
- 连接配置依赖的环境变量必须已经提供；缺少时程序明确报错。宿主专用连接信息不能由 Skill 推测或补造。
- 可以通过 `python scripts/monitor.py extract --input <原始响应> --output <派生文件>` 解开标准 MCP 与业务响应封装；提取配置增加 `--kind config`。该操作保留业务对象内容，原始响应保持原样。报告入口允许直接使用原始响应，无需另写数据提取脚本。
- HTTP SSE 单个事件上限为 64 MiB；超过上限时保留调用记录并终止。程序完整保存 MCP 返回对象后，再检查业务状态与输出 schema；不会删减返回字段或改写数据来通过校验。

### stdio 文件调用

- **连接配置**：`command` 指向当前合格 Python；`args` 明确包含内置 `scripts/stdio_bridge.py` 的绝对路径，以及 `--connection <实际上游HTTP连接.json>`，也可以使用 `--codex-config <实际Codex配置> --server <服务名>`。
- **执行入口**：将该 stdio 连接 JSON 传给 `call_mcp.py --connection`，其他参数与上文相同。父进程通过 `PULSE_MCP_HTTP_AUDIT` 将本次 HTTP 请求记录路径交给子进程，适配器按真实上游结果转发。独立运行适配器时必须提供 `--audit <请求记录路径>`。
- **完成检查**：详情响应保存后，父进程核对实际 HTTP 请求记录中存在本次 Tool、唯一的中文 Header 及对应响应。缺少记录、认证失败或上游返回不符合要求时停止依赖步骤。

## 调用结果处理

- 同时检查传输结果、MCP `isError`、业务 `status`、`error_code`，以及操作所需身份和任务字段。成功的传输不等于业务成功。
- 创建或更新在连接终止后结果未知时，保留原调用记录，通过列表和完整配置核实。创建必须有本次请求对应的真实身份依据；同名对象不够充分。
- 周期运行响应未知时保存目标和调用位置，核实原任务；不再次触发该期。无法取得任务身份时说明阻断。
- 错误响应和无数据分别处理。只有服务明确表示目标期不存在时才进入首次运行；不能把权限、积分、参数错误当作不存在。
- 更新按 Tool 的完整 schema 提交。保留原始服务附加字段，提交对象仅包含该 Tool 接受的字段；不能将部分参数当作完整配置。
- 所有文件调用入口共用 `common.py` 的参数检查，验证目标 Tool、个人类型、周计划配置、报告目标周期、`pulse-id`、`run-id` 及六位周期编码。月编码的月份须为 `01` 至 `12`，周编码须为 `01` 至 `53`。各宿主继续依据当前 Tool schema 检查完整字段。发生参数或程序错误时，读取实际错误、检查输入及所属程序后修正；相同输入未变化时不重复执行失败调用。

## 日志与继续执行

- `monitor.py state` 保存 `step`、`status`、`pulse_id`、`run_id`、资料路径及 `continue_condition`，记录每次模块交接、远程调用后和中断位置。
- 日志通过 `monitor.py event` 统一写入，记录 UTC 时间、执行目录、步骤、操作、结果、异常说明和相关文件；鉴权内容不进入日志。
- 使用 `monitor.py inspect --workspace <执行目录>` 查看状态和日志位置。继续执行时读取正式文件与 `state.json`，确认已有结果仍适用，再接续未完成步骤。
- 日志默认保留 30 天。`monitor.py clean-logs --root <工作目录> --days 30` 只清理已结束且超过期限的日志，保留当前状态、正式资料、原始响应和交付文件。正在运行或中断待继续的任务不清理。
