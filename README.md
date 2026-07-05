# Claude for Legal — 中国法版本

<p align="center">
  <a href="https://github.com/CSlawyer1985/claude-for-legal-ZH/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
  <a href="https://github.com/CSlawyer1985/claude-for-legal-ZH"><img src="https://img.shields.io/badge/version-v1.1.0-brightgreen" alt="Version"></a>
  <a href="https://github.com/CSlawyer1985/claude-for-legal-ZH/stargazers"><img src="https://img.shields.io/github/stars/CSlawyer1985/claude-for-legal-ZH?style=social" alt="Stars"></a>
  <a href="https://github.com/CSlawyer1985/claude-for-legal-ZH"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
  <br>
  <b>为最常见的中国法律工作流提供的参考 Agent、技能和数据连接器</b>
  <br>
  涵盖商事合同 · 隐私数据 · 产品合规 · 公司并购 · 劳动用工 · 争议解决 · 监管合规 · AI 治理 · 知识产权 · 法学教育 · 法律诊所
</p>

---

> **新用户？** 从 [QUICKSTART.md](QUICKSTART.md) 开始——60 秒完成安装。本文是完整参考手册。

<p align="center">
  <img src="docs/assets/hero.png" alt="Claude for Legal 中国法版本 — 着陆页 Hero" width="800">
</p>

本仓库所有内容可通过**两种方式**使用：安装为 [Claude Code](https://claude.com/product/claude-code) 插件，或通过 [Claude Managed Agents API](https://docs.anthropic.com/en/api/managed-agents) 部署在你自己的工作流引擎后台。同一套 system prompt，同一套技能——你选择在哪里运行。

## 在 Claude Code 中安装

```bash
# 添加市场源（使用本仓库的绝对路径或 GitHub URL）
/plugin marketplace add <path-to-this-repo>

# 安装你需要的插件
/plugin install commercial-legal@claude-for-legal-zh
/plugin install privacy-legal@claude-for-legal-zh
/plugin install corporate-legal@claude-for-legal-zh

# 重启 Claude Code，然后为每个已安装插件运行初始化设置。
# 设置过程将你的实践画像写入 ~/.claude/plugins/config/claude-for-legal-zh/<插件名>/CLAUDE.md
/commercial-legal:cold-start-interview
/privacy-legal:cold-start-interview
/corporate-legal:cold-start-interview
```

**先运行冷启动面试。** 插件中的其他所有技能都从实践画像读取配置。跳过设置是技能输出泛化的最常见原因。每个插件的面试耗时 10–20 分钟，会要求你提供种子文件（已签署的主合同、审查指引、过往审查备忘录——取决于插件类型）。种子材料越多效果越好；也可选择**快速启动**模式，2 分钟即可开始工作，后续再精细调整。

**先连接法律检索工具。** 连接检索工具后一切效果更好，未连接时引用标注为"未验证"。本套件已预配置 **yuandian（元典）MCP** 连接器用于案例检索和法规检索。详见 [MCP 连接器](#mcp-连接器)。

> [!IMPORTANT]
> **这些插件的所有输出均为律师审查草稿——不是法律意见，不是法律结论，不替代律师。** 插件在设计层面内置了相应的安全机制：每条引用标注来源，涉主观法律判断默认保守处理，管辖权假设明示标注，任何提交、发送或依赖前设有明确门槛。律师审查、核实并对所有对外产出承担专业责任。插件让审查更快，但不能替代审查。
>
> **这些插件不代表 Anthropic 的法律立场。** 它们是帮助律师分析问题的工具。技能中包含的清单项目、建议框架、风险标记、案例法或监管指引的定性描述，均为辅助审查律师自身分析的参考，而非 Anthropic 对法律的表态。许多领域的法律处于未定和演进之中。使用插件的律师——而非插件本身，也非 Anthropic——对其工作成果中的法律立场负责。

## 中国法本地化改造说明

本仓库是 [Anthropic claude-for-legal](https://github.com/anthropics/claude-for-legal) 的中国法适配版本，在保持原仓库完整文件结构的前提下，对美国法内容进行了系统性中国法本地化改造。

### 核心改造

| 维度 | 原版（美国法） | 中国法版本 |
|------|--------------|-----------|
| **合同法** | UCC、Governing law (Delaware/NY) | 民法典合同编、民法典担保制度司法解释 |
| **劳动法** | FLSA/FMLA/ADA/NLRA/at-will | 劳动合同法/劳动争议调解仲裁法/工伤保险条例 |
| **诉讼程序** | FRCP/FRE/discovery/deposition | 民事诉讼法/民诉法司法解释/证据规定 |
| **隐私数据** | GDPR/CCPA/DPA | 个人信息保护法/数据安全法/网络安全法 |
| **知识产权** | USPTO/DMCA/Lanham Act | 商标法/专利法/著作权法/信息网络传播权保护条例 |
| **公司治理** | Delaware corporate law/SEC | 公司法/证券法/三会制度 |
| **法学教育** | Bar exam/MBE/Socratic method | 法考（客观题+主观题）/中国法学教育方式 |
| **案例检索** | Westlaw/CourtListener/Trellis | 元典 yuandian MCP/人民法院案例库/北大法宝 |
| **合同管理** | Ironclad/DocuSign/iManage | e签宝/法大大/飞书知识库 |
| **监管追踪** | Federal Register/eCFR | 中国政府网/司法部法律法规数据库 |

### 规则体系升级

本版本在原版安全机制基础上，注入以下规则升级：

| 升级项 | 说明 |
|--------|------|
| **风险评价六维度方法论** | 每个风险点完成：风险定性→风险敞口→发生概率→可规避性→商业权衡→紧迫性，六维评价 |
| **双轴风险评价** | 法律风险与商业/操作摩擦独立评价，两个维度不互相替代 |
| **三层来源溯源标签** | 所有法律依据强制标注来源（法条原文/yuandia检索/模型知识等），按可信度分层 |
| **三轮检索策略** | 改写检索表达→分层关键词→三轮递进检索，禁止直接拿用户原话开搜 |
| **五组内容分离** | 诉讼文书编辑时强制区分：证据列举/质证意见/证据认定/查明事实/争议焦点分析 |
| **时效验证流程** | 引用具体法条、司法解释、诉讼时效时强制独立检索验证 |
| **知识库路由** | 优先源（理解与适用/类案指南/最高院审判实务）→扩展源→效力警示源，按权威分级检索 |
| **知识库路径可配置** | `[KB_ROOT]` 变量抽象，各人按自己的环境配置一次根目录，仓库不再绑定特定机器的绝对路径 |
| **多端适配（社区贡献）** | 新增 17 个 Codex Desktop/CLI adapter skill，同一套法律知识和工作流可同时服务 Claude Code 与 Codex 用户 |
| **知识库四步交叉引用协议** | 路由规则加载 → Wiki 概念检索 → 原始数据源检索（优先源→扩展源）→ 外部补充（MCP/联网搜索），每步强制不得跳过 |
| **主体信用自动查询** | 首次出现非自然人主体时触发信用查询：实体锚定 → 基础画像+风险扫描（并行）→ 关键人员穿透，生成结构化信用报告 |
| **Agentic Search 路由** | 三层 C1/C2/C3 路由：复杂多维问题自动跳过常规管线进入多源并行深度检索，常规管线不足时自动升级 |
| **法律文书编辑纪律** | 基准稿锁定 → 五组内容分离 → 证据边界纪律 → 跨段落一致性校验 → 联动更新顺序 → 常见失误自检 |
| **合同审核质量门禁** | 效力审查（名实不符/格式条款/审批登记）→ 主体授权审查 → 八维条款审查 → 修订方式路由决策树（自检四问）→ 终稿三件套 |
| **尽职调查六阶段方法论** | 项目立项 → 指引加载 → 底稿摄入与转换 → 事实查明与证据映射 → 问题条线推进 → 交付输出（报告三段式写作+质量门禁） |
| **庭审准备框架** | 材料收集 → 案件分析 → 五模块庭审提纲（案件概览/争议焦点/事实查明/法律适用/发问提纲），多角色适配 |
| **法律咨询分析工作流** | 启动门禁（先建文件夹再检索）→ 意图分析与问题拆解 → 分层研究 → 综合解答 → 效力审计，四档服务深度自动匹配 |
| **法律服务报价框架** | 八阶段流程：项目启动 → 需求分析 → 知识库检索 → 服务策略 → 报价策略（六种方式决策矩阵）→ 方案撰写 → 质量审核 → 输出 |

<p align="center">
  <img src="docs/assets/method-1.png" alt="方法论 — 步骤 1" width="400">
  <img src="docs/assets/method-2.png" alt="方法论 — 步骤 2" width="400">
  <img src="docs/assets/method-3.png" alt="方法论 — 步骤 3" width="400">
  <img src="docs/assets/method-4.png" alt="方法论 — 步骤 4" width="400">
</p>

### 知识库集成

本版本支持深度集成本地法律知识库体系（知识库根目录在 `company-profile.md` 的「本地知识库」段配置），包含：

- **法律优先源**：最高法法官权威释义（理解与适用丛书）、类案裁判指引、最高院审判实务观点、指导案例/典型案例/人民法院案例库、税务/财政/国资委权威答复
- **扩展检索源**：32,500+ 法律公众号文章（按领域+权威双维组织）、法律法规数据库、分类实务文章
- **效力警示源**：各省法院指导意见（部分已失效未标注）、历史投行规则

知识库原始数据层 AI 只读，不得修改。

### 底层规则参考文件

为方便无知识库的用户直接使用，10 个业务领域插件内置了自足的中国法核心规则参考文件（`<插件名>/references/` 下），覆盖各领域最底层、最高频的法条原文和裁判规则，无需额外配置即可引用：

| 文件 | 插件 | 行数 | 覆盖内容 |
|------|------|------|----------|
| `labor-core-rules.md` | employment-legal | 710 | 劳动关系认定（三要素）、解除类型（第36-42条）、经济补偿/赔偿金、竞业限制、工伤认定、工时加班、试用期、年休假、三期保护、医疗期 |
| `civil-procedure-core.md` | litigation-legal | 297 | 管辖（地域/合同/侵权/协议/专属）、当事人、诉讼时效（3年+中断/中止）、审级与程序、保全（财产/行为/证据）、送达与期间 |
| `evidence-rules-core.md` | litigation-legal | 258 | 举证责任分配、8种证据类型、自认规则、举证时限与证据失权、证明标准（高度盖然性/排除合理怀疑）、证据三性审查、鉴定与专家辅助人 |
| `enforcement-core.md` | litigation-legal | 282 | 执行依据与管辖、财产调查、执行措施体系（查封/冻结/拍卖/变卖）、执行异议与异议之诉、执行和解、失信被执行人/限制消费、执行转破产、迟延履行利息、拒不执行判决裁定罪 |
| `company-law-2024-core.md` | corporate-legal | 501 | 限期认缴制（第47条）、出资加速到期（第54条）、股东失权（第51-52条）、治理结构、审计委员会、董监高义务（第180-192条）、公司担保（第15条）、股权转让（第84/88条）、人格否认（第23条）、简易注销（第240条） |
| `contract-law-core.md` | commercial-legal | 496 | 合同成立与效力（第471-489条）、格式条款（第496-498条）、履行抗辩权、合同变更与转让、合同解除（第563-566条）、违约责任体系（继续履行/损害赔偿/违约金/定金）、情势变更（第533条）与不可抗力（第590条）、保证担保（第686条） |
| `ip-core-rules.md` | ip-legal | 374 | 商标法（注册条件/侵权/撤三/损害赔偿）、专利法（三性/职务发明/等同侵权/抗辩）、著作权法（作品类型/合理使用/避风港）、反不正当竞争法（商业秘密/混淆/虚假宣传） |
| `pipil-core-provisions.md` | privacy-legal | 396 | 个保法核心（定义/合法性基础/告知同意/敏感个人信息/主体权利/自动化决策/PIA/数据出境/5%营业额罚款）、数据安全法（分类分级/重要数据）、网络安全法（等保/CIIO）、三法关系与合规核查清单 |
| `admin-law-core.md` | regulatory-legal | 523 | 行政处罚法（种类/设定/程序/时效/首违不罚）、行政复议法（2023修订）、行政诉讼法（受案范围/管辖/举证责任/判决类型）、行政许可法、行政强制法、政府信息公开、行政协议、国家赔偿 |
| `ai-governance-core.md` | ai-governance-legal | 403 | 生成式AI管理办法（训练数据/内容标识/安全评估）、算法推荐管理规定（备案/透明度/选择权）、深度合成管理规定、科技伦理审查办法、行业AI监管（金融/医疗/自动驾驶） |

所有参考文件引用法条均标注 `[法条原文]` 来源溯源标签，独立于知识库使用。

### 共享工作流参考文件（v1.1 新增）

除各插件内置的法律规则参考文件外，`references/` 目录下新增 7 个跨插件共享的工作流方法论参考文件，可被任意插件按需引用：

| 文件 | 适用插件 | 内容 |
|------|----------|------|
| `knowledge-base-crossref.md` | 全部插件 | 四步知识库交叉引用协议——路由规则加载 → Wiki 概念检索 → 原始数据源检索 → 外部补充，含来源标注速查表和 C2 Agentic Search 升级钩子 |
| `agentic-search-routing.md` | 全部插件 | 三层路由规则（C1 自动判定/C2 管线兜底/C3 用户指令）——当问题涉及 ≥3 个独立法律维度或常规管线不足时，自动升级至多源并行深度检索 |
| `due-diligence-workflow.md` | corporate-legal | 六阶段尽调方法论——项目立项 → 指引加载 → 底稿摄入与转换 → 事实查明与证据映射（含证据链格式）→ 问题条线推进 → 交付输出（三段式报告写作+质量门禁） |
| `trial-preparation-framework.md` | litigation-legal | 庭审准备框架——案件材料收集 → 分析（基础信息/时间线/法律问题/检索）→ 五模块庭审提纲（案件概览/争议焦点/事实查明/法律适用/发问提纲），支持原告/被告/仲裁员多角色适配 |
| `contract-review-quality-gates.md` | commercial-legal | 合同审核质量门禁——效力审查（名实不符/格式条款/审批登记）→ 主体与授权 → 八维条款审查 → 修订方式路由决策树（自检四问）→ 终稿三件套 → 特殊合同类型矩阵 |
| `consulting-workflow.md` | legal-clinic | 法律咨询分析工作流——启动门禁（先建文件夹再检索）→ 意图分析与问题拆解 → 分层检索研究 → 综合解答 → 效力审计，四档服务深度自动匹配（法条确认/单一问题/复杂商业法律问题/正式法律意见书） |
| `pricing-proposal-framework.md` | legal-clinic | 法律服务报价八阶段流程——项目启动与意图分析 → 客户需求结构化分析（七维度+复杂度评估）→ 知识库检索与研究 → 服务策略制定（核心/推荐/可选/排除四级服务范围）→ 报价策略选择与计算（六种方式决策矩阵+费用调整机制）→ 方案撰写 → 质量审核 → 输出，支持三类方案结构（诉讼代理/非诉专项/常年顾问） |

所有共享工作流参考文件均来源于中国法律实务经验，不包含个人路径或密钥。各插件 CLAUDE.md 的"共享安全机制"段落中已内联引用对应文件。

---

## 盒子里有什么

- **12 个业务领域插件**——覆盖律所、法务和学术法律工作，每个插件围绕冷启动面试构建，生成实践画像（`CLAUDE.md`），所有技能从中读取配置。
- **托管 Agent 蓝图**——用于定时、持续监控型工作流（续签监控、案件进度监控、法规动态监控、尽调网格、产品上线雷达）。
- **MCP 连接器**——覆盖通用生产力工具（飞书、Google Drive）和法律专属系统（元典 yuandian、北大法宝、威科先行、e签宝、聚法案例等）。
- **命名 Agent**——端到端工作流 Agent（供应商合同审查、个人信息主体权利响应、劳动合同解除审查、要件分析表构建……），每个 Agent 有独立的职位式名称和单一启动命令。

<p align="center">
  <img src="docs/assets/capabilities.png" alt="能力展示 — Agent 卡片网格" width="800">
</p>

## Agent 列表

每个 Agent 以其运行的工作流命名。从与你工作匹配的 Agent 开始，然后调整底层技能、实践画像和连接器以适应团队工作方式。

| Agent | 功能 | 插件 | 命令 |
|---|---|---|---|
| **供应商合同审查** | 依据审查指引审查供应商主协议，生成修订备忘录 | `commercial-legal` | `/commercial-legal:review` |
| **保密协议分流** | 对 incoming 保密协议进行绿/黄/红三色分流，仅复杂协议进入律师审查 | `commercial-legal` | `/commercial-legal:review` |
| **合同修订追踪** | 追踪合同从原始版本到历次修订的完整变更 | `commercial-legal` | `/commercial-legal:amendment-history` |
| **合同续签监控** | 扫描合同台账中的解约和续签截止日期 | `commercial-legal` | scheduled agent |
| **签署合同复盘** | 每周梳理已签署协议中的审查指引偏离项 | `commercial-legal` | scheduled agent |
| **审查指引更新** | 监控偏离日志，在条款持续偏移时提出审查指引更新建议 | `commercial-legal` | scheduled agent |
| **问题升级路由** | 将合同问题路由至适当审批人并起草请示 | `commercial-legal` | `/commercial-legal:escalation-flagger` |
| **表格式尽调审查** | 对数据室文件逐份表格式审查，每格附带引用来源 | `corporate-legal` | `/corporate-legal:tabular-review` |
| **尽调问题提取** | 按预设类别和重要性阈值提取数据室文件中的问题 | `corporate-legal` | `/corporate-legal:diligence-issue-extraction` |
| **董事会/股东会决议起草** | 按内部格式起草决议，附带先例检索 | `corporate-legal` | `/corporate-legal:written-consent` |
| **重大合同披露清单** | 依据尽调发现和收购协议阈值编制披露清单 | `corporate-legal` | `/corporate-legal:material-contract-schedule` |
| **企业合规追踪** | 跨地域、跨主体类型的申报节点计算和合规体检 | `corporate-legal` | `/corporate-legal:entity-compliance` |
| **交割清单管理** | 追踪阻碍交割的各项条件、同意、文件和申报 | `corporate-legal` | `/corporate-legal:closing-checklist` |
| **并购整合管理** | 分阶段交割后整合计划，含同意追踪和周报 | `corporate-legal` | `/corporate-legal:integration-management` |
| **数据室监控** | 监控数据室新增文件，按计划推送交割清单状态 | `corporate-legal` | scheduled agent |
| **劳动合同解除审查** | 对拟议解除进行法定事由审查和风险标记 | `employment-legal` | `/employment-legal:termination-review` |
| **录用审查** | 审查录用通知及竞业限制/服务期条款 | `employment-legal` | `/employment-legal:hiring-review` |
| **劳动关系认定** | 依据劳动和社会保障部〔2005〕12号三要素测试用工关系 | `employment-legal` | `/employment-legal:worker-classification` |
| **假期追踪** | 监控在休假期（年休假/产假/病假），含截止日期预警 | `employment-legal` | scheduled agent |
| **内部调查** | 启动、追踪、补充和汇总内部调查事项 | `employment-legal` | `/employment-legal:investigation-open` |
| **规章制度起草** | 起草劳动规章制度，含民主程序和公示要求 | `employment-legal` | `/employment-legal:policy-drafting` |
| **跨省用工规划** | 启动新省份用工规划及外部律师委托简报 | `employment-legal` | `/employment-legal:expansion-kickoff` |
| **劳动用工问答** | 面向"快速问答"渠道的劳动用工法律咨询 | `employment-legal` | `/employment-legal:wage-hour-qa` |
| **个人信息主体权利响应** | 在法定期限内起草权利响应告知和实质回复 | `privacy-legal` | `/privacy-legal:dsar-response` |
| **个人信息处理协议审查** | 依据审查指引审查个人信息处理协议（控制者或处理者视角） | `privacy-legal` | `/privacy-legal:dpa-review` |
| **个人信息保护影响评估** | 按内部格式生成新功能或新活动的个人信息保护影响评估报告 | `privacy-legal` | `/privacy-legal:pia-generation` |
| **个保场景分流** | 判断处理活动是否需要个保法第55条评估、或可直接推进 | `privacy-legal` | `/privacy-legal:use-case-triage` |
| **隐私法规差距分析** | 将新规或修订与现行隐私政策和实践进行差异比对 | `privacy-legal` | `/privacy-legal:reg-gap-analysis` |
| **隐私政策监控** | 扫描已存评估、协议审查和分流结果，检查政策与实践的偏差 | `privacy-legal` | `/privacy-legal:policy-monitor` |
| **产品上线审查** | 依据风险校准审查产品上线 | `product-legal` | `/product-legal:launch-review` |
| **营销宣传审查** | 标记需要补强、改写或删除的宣传文案（广告法/反不正当竞争法） | `product-legal` | `/product-legal:marketing-claims-review` |
| **"这是问题吗？" 快速判断** | 快速回答产品/营销法律咨询——依据你的风险校准做模式匹配 | `product-legal` | `/product-legal:is-this-a-problem` |
| **产品上线雷达** | 监控上线追踪器中即将需要法务审查的产品 | `product-legal` | scheduled agent |
| **法规动态监控** | 轮询法规信息源并撰写周一晨会监管简报 | `regulatory-legal` | scheduled agent |
| **即时法规检查** | 即时检查法规动态，报告上次检查以来的更新 | `regulatory-legal` | `/regulatory-legal:reg-feed-watcher` |
| **政策差异分析** | 将特定法规变化与已索引的政策库进行差异比对 | `regulatory-legal` | `/regulatory-legal:policy-diff` |
| **合规差距追踪** | 开放差距追踪器——已标记尚未关闭的项目 | `regulatory-legal` | `/regulatory-legal:gaps` |
| **政策重述** | 带修改标记的政策重述以关闭差距——供政策负责人审阅的建议稿 | `regulatory-legal` | `/regulatory-legal:policy-redraft` |
| **征求意见稿追踪** | 审查开放的征求意见期、记录决策、追踪截止日期 | `regulatory-legal` | `/regulatory-legal:comments` |
| **AI 场景分流** | 对照登记册对拟议 AI 应用场景进行分类 | `ai-governance-legal` | `/ai-governance-legal:use-case-triage` |
| **AI 影响评估** | 对适用范围内的各监管制度开展算法安全评估/科技伦理审查 | `ai-governance-legal` | `/ai-governance-legal:aia-generation` |
| **AI 供应商审查** | 审查 AI 供应商条款——训练数据使用、责任分配、模型变更、政策差距 | `ai-governance-legal` | `/ai-governance-legal:vendor-ai-review` |
| **AI 法规差距分析** | 将新的 AI 法规与当前治理状态进行差异比对 | `ai-governance-legal` | `/ai-governance-legal:reg-gap-analysis` |
| **AI 政策监控** | 扫描已存评估、分流结果和供应商审查，检查 AI 政策偏差 | `ai-governance-legal` | `/ai-governance-legal:policy-monitor` |
| **商标可注册性检索** | 初步检索——相同/近似商标筛查和混淆可能性判断 | `ip-legal` | `/ip-legal:clearance` |
| **侵权警告函** | 起草或分流警告函，依据你的维权策略校准 | `ip-legal` | `/ip-legal:cease-desist` |
| **通知-删除** | 起草删除通知、分流收到通知或起草反通知（信息网络传播权保护条例） | `ip-legal` | `/ip-legal:takedown` |
| **开源合规检查** | 依据你的部署模式对开源许可证进行分类 | `ip-legal` | `/ip-legal:oss-review` |
| **FTO 初步分析** | 对潜在阻碍专利的结构化初步审视——分流而非法律意见 | `ip-legal` | `/ip-legal:fto-triage` |
| **侵权初步判断** | 商标/著作权/专利/商业秘密跨权利初步分流 | `ip-legal` | `/ip-legal:infringement-triage` |
| **知识产权条款审查** | 审查转让、归属、许可授权、保证和赔偿条款 | `ip-legal` | `/ip-legal:ip-clause-review` |
| **知识产权组合管理** | 注册、续展、维护费、使用声明管理 | `ip-legal` | `/ip-legal:portfolio` |
| **IP 续展监控** | 知识产权组合台账的定时截止日期报告 | `ip-legal` | scheduled agent |
| **要件分析表** | 逐要件分析表——专利侵权或民事案由 | `litigation-legal` | `/litigation-legal:claim-chart` |
| **案件进度监控** | 监控法院案件进展和截止日期 | `litigation-legal` | scheduled agent |
| **律师函起草** | 起草律师函，设置发送门槛 | `litigation-legal` | `/litigation-legal:demand-draft` |
| **律师函准备** | 起草前背景收集——当事人、事实、依据、谈判筹码 | `litigation-legal` | `/litigation-legal:demand-intake` |
| **收函分流** | 分流收到的律师函——选项、案件交叉检查、转交 | `litigation-legal` | `/litigation-legal:demand-received` |
| **法院调查令/协查通知处理** | 分类、界定范围并规划合规方案 | `litigation-legal` | `/litigation-legal:subpoena-triage` |
| **大事记构建** | 从已声明来源和上传材料构建或更新大事记 | `litigation-legal` | `/litigation-legal:chronology` |
| **庭前准备** | 构建与案件理论挂钩的庭前准备提纲，含文书和质证要点 | `litigation-legal` | `/litigation-legal:deposition-prep` |
| **法律文书起草** | 按律所/团队格式起草法律文书章节 | `litigation-legal` | `/litigation-legal:brief-section-drafter` |
| **证据三性审查** | 第一轮证据三性审查——初步判断 + 标注律师需复核事项 | `litigation-legal` | `/litigation-legal:privilege-log-review` |
| **证据保全** | 签发、更新、解除或报告证据保全 | `litigation-legal` | `/litigation-legal:legal-hold` |
| **案件登记** | 新案件统一登记——写入案件文件、历史记录，追加日志 | `litigation-legal` | `/litigation-legal:matter-intake` |
| **案件深度简报** | 单个案件深度简报——适用于主任或外部律师会议准备 | `litigation-legal` | `/litigation-legal:matter-briefing` |
| **案件组合状态** | 风险分布、临近截止日期、停滞案件 | `litigation-legal` | `/litigation-legal:portfolio-status` |
| **外部律师状态** | 为活跃案件组合生成每周状态催问草稿 | `litigation-legal` | `/litigation-legal:oc-status` |
| **法律诊所接待** | 结构化客户接待，含跨领域问题识别和冲突标记 | `legal-clinic` | `/legal-clinic:client-intake` |
| **案件备忘录框架** | IRAC 结构案件分析备忘录，标注研究缺口 | `legal-clinic` | `/legal-clinic:memo` |
| **检索路线图** | 需检查的法条、案例领域、检索关键词——线索而非引用 | `legal-clinic` | `/legal-clinic:research-start` |
| **法律诊所节点追踪** | 添加、报告、更新和关闭案件节点，含执业风险警告 | `legal-clinic` | `/legal-clinic:deadlines` |
| **案件状态汇总** | 按受众分类的案件状态——客户版、指导老师版、法院版 | `legal-clinic` | `/legal-clinic:status` |
| **客户信函起草** | 常规客户信函——预约确认、材料索取、进展更新 | `legal-clinic` | `/legal-clinic:client-letter` |
| **学生学期导入** | 学期导入——诊所流程、工具导览、实践练习 | `legal-clinic` | `/legal-clinic:ramp` |
| **学期移交** | 期末案件移交备忘录 | `legal-clinic` | `/legal-clinic:semester-handoff` |
| **指导老师审查队列** | 教授审查队列（配置正式审查督导时） | `legal-clinic` | `/legal-clinic:supervisor-review-queue` |
| **法考备考教练** | 针对薄弱科目提供客观题和主观题练习 | `law-student` | `/law-student:bar-prep-questions` |
| **课堂问答训练** | 它问、你答、它追问——不直接给答案 | `law-student` | `/law-student:socratic-drill` |
| **IRAC 写作批改** | 对 IRAC 作文的结构、问题识别、规则引用、分析逻辑评分 | `law-student` | `/law-student:irac-practice` |
| **案例摘要** | 按你偏好的格式做案例摘要 | `law-student` | `/law-student:case-brief` |
| **知识体系搭建** | 从课堂笔记和教材构建或扩展知识体系 | `law-student` | `/law-student:outline-builder` |
| **课堂准备** | 预测教授提问并在课前进行针对性训练 | `law-student` | `/law-student:cold-call-prep` |
| **考试预测** | 分析同一教授历年试题，预测可能重点 | `law-student` | `/law-student:exam-forecast` |
| **法律写作反馈** | 对草稿的结构性反馈——从不代写 | `law-student` | `/law-student:legal-writing` |
| **记忆卡片训练** | 生成或训练记忆卡片——Leitner 式分层记忆 | `law-student` | `/law-student:flashcards` |
| **学习计划** | 长期学习计划，含排课和基于学习记录的适应性调整 | `law-student` | `/law-student:study-plan` |
| **技能注册表浏览器** | 搜索已关注注册表中的社区法律技能 | `legal-builder-hub` | `/legal-builder-hub:registry-browser` |
| **技能安装器** | 安装社区技能，含信任检查和安全审查 | `legal-builder-hub` | `/legal-builder-hub:skill-installer` |
| **技能质量评估** | 依据法律技能设计框架评估技能 | `legal-builder-hub` | `/legal-builder-hub:skills-qa` |
| **社区技能推荐** | 基于其他插件中的近期活动推荐社区技能 | `legal-builder-hub` | `/legal-builder-hub:related-skills-surfacer` |
| **社区技能更新** | 检查已安装社区技能的更新 | `legal-builder-hub` | `/legal-builder-hub:auto-updater` |
| **注册表同步** | 定期检查已关注注册表中的新增和更新技能 | `legal-builder-hub` | scheduled agent |

<p align="center">
  <img src="docs/assets/lab-1.png" alt="Lab — Agent 工作界面 1" width="250">
  <img src="docs/assets/lab-2.png" alt="Lab — Agent 工作界面 2" width="250">
  <img src="docs/assets/lab-3.png" alt="Lab — Agent 工作界面 3" width="250">
  <img src="docs/assets/lab-4.png" alt="Lab — Agent 工作界面 4" width="250">
  <img src="docs/assets/lab-5.png" alt="Lab — Agent 工作界面 5" width="250">
</p>

托管 Agent 部署——`agent.yaml`、leaf-worker 子 Agent、steering 事件示例和各 Agent 安全说明，详见 **[managed-agent-cookbooks/](./managed-agent-cookbooks)**。

## 仓库布局

```
commercial-legal/         # 商事合同——供应商/保密协议/SaaS审查、续签、问题升级
corporate-legal/          # 公司并购——尽调、交割清单、董事会决议、主体合规
employment-legal/         # 劳动用工——录用/解除审查、劳动关系认定、假期、内部调查
privacy-legal/            # 隐私数据——个人信息处理协议、主体权利响应、影响评估、政策监控
product-legal/            # 产品合规——上线审查、营销宣传、快速判断
regulatory-legal/         # 监管合规——法规动态监控、政策差异、差距追踪、征求意见
ai-governance-legal/      # AI 治理——场景分流、算法评估、供应商AI审查、法规差距
ip-legal/                 # 知识产权——商标检索、FTO、侵权警告、通知-删除、开源合规、组合管理
litigation-legal/         # 争议解决——案件组合、登记、证据保全、律师函、庭前准备、要件分析
legal-clinic/             # 法律诊所——诊所设置、学生导入、接待、节点、备忘录、移交
law-student/              # 法学教育——课堂训练、知识体系、IRAC、法考备考、记忆卡片
legal-builder-hub/        # 社区技能发现与安装，含信任门槛
references/               # 共享参考文件——知识库协议、Agentic Search 路由、尽调/庭审/合同审核/咨询/报价工作流
external_plugins/         # 合作方构建的插件（由供应商维护）
managed-agent-cookbooks/  # Claude Managed Agent 蓝图——每个定时 Agent 一个目录
  diligence-grid/
  docket-watcher/
  launch-radar/
  reg-monitor/
  renewal-watcher/
scripts/                  # deploy-managed-agent.sh · validate.py · orchestrate.py · lint-tool-scope.py
.claude-plugin/
  marketplace.json        # 插件注册表
```

每个插件目录具有相同结构：

```
<插件名>/
  .claude-plugin/plugin.json
  CLAUDE.md               # 实践画像模板——由 /<插件名>:cold-start-interview 填充
  README.md
  skills/                 # 技能文件——每个是 /<插件名>:<技能名> 斜杠命令
  agents/                 # 定时 Agent（如有）
  hooks/                  # 工具前后钩子（如有）
```

## 如何组合

| | 是什么 | 在哪 |
|---|---|---|
| **插件** | 自包含的业务领域套件——技能、Agent、钩子和实践画像模板。按需安装。 | `<插件名>/` |
| **技能** | 领域专业知识、惯例和分步方法论，Claude 在相关时自动调用——也可以通过斜杠命令显式触发：`/commercial-legal:review`、`/privacy-legal:dsar-response`、`/litigation-legal:claim-chart`。 | `<插件名>/skills/<技能名>/SKILL.md` |
| **Agent** | 定时或事件驱动的工作流（续签监控、案件进度监控、法规变化监控）。在后台运行，推送到渠道或写入文件。 | `<插件名>/agents/` |
| **实践画像** | 描述你的审查指引、升级规则和内部风格的纯文本 `CLAUDE.md`。所有技能从中读取。 | `~/.claude/plugins/config/claude-for-legal-zh/<插件名>/CLAUDE.md` |
| **连接器** | 将 Claude 与你的数据系统连接的 [MCP 服务器](https://modelcontextprotocol.io/)——合同管理、文档管理、电子取证、检索平台、生产力工具。 | `.mcp.json`（每个插件） |
| **托管 Agent 蓝图** | `agent.yaml` + 一级子 Agent + steering 示例，用于无头部署。 | `managed-agent-cookbooks/<slug>/` |

一切皆为 Markdown 和 JSON。无需构建步骤。

<p align="center">
  <img src="docs/assets/work-1.png" alt="工作成果展示 1" width="400">
  <img src="docs/assets/work-2.png" alt="工作成果展示 2" width="400">
</p>

## 业务领域插件

按工作领域分组。每个插件的冷启动面试是使其适配你团队的关键——从这里开始。

### 交易与咨询

| 插件 | 功能 |
|------|------|
| **[commercial-legal](./commercial-legal)** | 基于审查指引的供应商协议、保密协议和 SaaS 订阅合同审查。合同修订追踪。含解约预警的续签台账。问题升级路由。业务人员可读摘要。 |
| **[corporate-legal](./corporate-legal)** | 并购尽调——表格式审查、逐格引用。披露清单、交割清单、董事会/股东会决议、会议纪要。企业合规追踪。交割后整合。 |
| **[privacy-legal](./privacy-legal)** | 个保场景分流（个保法第55条评估/直接推进），个人信息保护影响评估生成，个人信息处理协议审查（控制者/处理者视角），主体权利响应。政策与实践偏差监控。 |
| **[product-legal](./product-legal)** | 基于风险校准的产品上线审查。营销宣传合规检查（广告法/反不正当竞争法）。快速判断分流。功能风险评估。 |
| **[employment-legal](./employment-legal)** | 录用和解除审查，含跨省风险标记。劳动关系认定（〔2005〕12号三要素）。假期追踪（年休假/产假/病假）。内部调查。规章制度起草（民主程序+公示）。 |
| **[ai-governance-legal](./ai-governance-legal)** | AI 应用场景对照登记册分流。算法安全评估/科技伦理审查。AI 供应商审查。法规到政策差距分析。 |
| **[regulatory-legal](./regulatory-legal)** | 法规动态监控、政策差异分析、合规差距追踪、征求意见稿追踪。你的团队真正会读的周一晨报。 |
| **[ip-legal](./ip-legal)** | 商标可注册性检索、FTO 初步分析、侵权警告函起草和分流、通知-删除及反通知（信息网络传播权保护条例/电子商务法）、开源合规、知识产权条款审查、组合管理。 |

### 争议解决

| 插件 | 功能 |
|------|------|
| **[litigation-legal](./litigation-legal)** | 两个工作界面。**法务/组合管理：** 案件登记、组合状态、证据保全、外部律师状态、律师函。**律所/诉讼律师：** 大事记构建、要件分析表（专利和民事）、庭前准备、证据三性审查、法律文书起草。 |

### 学习与实践

| 插件 | 功能 |
|------|------|
| **[law-student](./law-student)** | 课堂问答训练、案例摘要、知识体系搭建、IRAC 写作批改、课堂准备、记忆卡片、法考备考、考试预测、学习计划。**学习模式而非替答模式**——从不替你写答案。 |
| **[legal-clinic](./legal-clinic)** | 指导老师设置和学生学期导入。按业务领域的指导手册（含教学模式：辅助/引导/教学）。结构化接待（含跨领域问题识别）。含执业风险警告的节点追踪。备忘录框架、客户信函（常规+通俗语言）、学期移交。 |

### 生态系统

| 插件 | 功能 |
|------|------|
| **[legal-builder-hub](./legal-builder-hub)** | 社区技能发现和安装，含真实信任层——已关注注册表、质量评估框架（`/legal-builder-hub:skills-qa`）、SHA 锁定更新，以及技能落地前的强制信任检查。 |

### 外部/合作方构建

`external_plugins/` 下的插件由供应商构建和维护。它们与本市场中的其他插件一样安装，但供应商拥有代码、连接器和支持渠道。欢迎中国法律科技服务商提交集成。

## 社区法律技能的信任层

社区正快速构建法律技能——LegalOps Consulting 的 `lpm-skills`、Lawvable 等注册表已列出数十个。但没有人认证社区技能，律师从 GitHub 安装一个随机技能，就是安装一段以访问其案件文件、实践画像和检索连接器权限运行的代码。

`legal-builder-hub` 为生态系统提供所需的安全层：

- **安全审查**——每次安装时进行隐藏内容扫描、注入检测和结构信任检查
- **白名单**——默认严格的来源门槛（注册表、发布者、连接器、许可证）
- **许可证门槛**——区分部署场景的许可证策略（个人/律所内部/产品嵌入）
- **时效门槛**——追踪捆绑的参考内容（法规、法条、程序）是否超出验证窗口，在调用时发出警告
- **更新时重新扫描**——v1.0 干净、v1.1 被投毒会被捕获
- **安装日志**——可审计的记录：安装了什么、从哪里来、什么许可证、什么审查结论

白名单默认严格。宽松模式是明确选择。非律师用户被路由到其律师联系人，而非"仍然安装"按钮。

社区技能经过与官方插件相同的设计审查（`/legal-builder-hub:skills-qa`）。如果你为律师构建工具，在发布前对自己的技能运行质量评估。

## MCP 连接器

> [!IMPORTANT]
> **先连接检索工具。** 每个插件已预配置法律检索连接器——yuandian（元典）MCP 用于案例检索和法规检索。首次需要时系统会提示授权。连接后，Claude 从权威来源获取信息并对引用进行验证。通过检索连接器获取的引用标注来源标签。仅来自模型知识的引用标记为 `[需验证]`，如果完全没有连接检索工具，交付物上方的审查备注会记录来源未经验证，提醒你核实。连接器让引用可信——在任何其他设置之前先配置它。

以下连接器随插件提供：

| 连接器 | 功能 | 适用插件 | 备注 |
|--------|------|----------|------|
| **飞书（Lark）** | 读取频道、搜索、发送消息和文档 | 全部插件 | 你的工作空间 |
| **Google Drive** | 读取文档、表格、幻灯片；按链接获取 | 全部插件 | 你的账户（可选） |
| **yuandian（元典）** | 案例检索、法规检索——覆盖裁判文书和法律法规 | 全部插件 | 公共；OAuth |
| **北大法宝** | 法律法规、司法解释、案例检索 | `ip-legal`、`litigation-legal`、`law-student`、`legal-clinic` | 客户订阅 |
| **威科先行** | 法律数据库——法规、案例、实务文章 | `commercial-legal`、`corporate-legal`、`litigation-legal` | 客户订阅 |
| **聚法案例** | 案例检索和裁判文书分析 | `litigation-legal` | 客户订阅 |
| **e签宝 / 法大大** | 电子合同签署和合同台账 | `commercial-legal` | 客户订阅 |
| **国家知识产权局** | 商标/专利检索和状态查询 | `ip-legal` | 公共 |
| **中国政府网 / 司法部法律法规数据库** | 官方法规数据库 | `regulatory-legal`、`ai-governance-legal` | 公共 |
| **Linear / Jira / Asana** | 产品上线追踪器、项目管理 | `product-legal` | 客户工作空间（可选） |

> "客户订阅"标记的连接器需要客户自身的账户和 API 密钥。在各插件的 `.mcp.json` 中配置，或通过 Claude Code 的 `claude mcp` 进行设置。

> **构建连接器？** 详见 [CONNECTORS.md](./CONNECTORS.md)，了解优秀法律 MCP 服务器的标准及提交方式。

## 成为你自己的

这些是参考模板。当它们与你团队的工作方式对齐时会发挥更大作用——定制机制就是插件本身。

- **运行冷启动面试。** 它**就是**定制机制。它会询问你的实务方式、读取你的种子文件、写入你的实践画像。所有其他技能从中读取。一次 `/commercial-legal:cold-start-interview`，附上五份已签署的主合同、你的审查指引和升级矩阵，审查技能将显著更精准。
- **编辑实践画像。** 你的画像位于 `~/.claude/plugins/config/claude-for-legal-zh/<插件名>/CLAUDE.md`。直接编辑以修正小问题——错误的升级阈值、新的集成、政策更新。它在插件更新后保留。
- **重新运行设置。** 当实务发生重大变化时（新业务领域、新系统、新政策），再次运行 `/<插件名>:cold-start-interview`。
- **更换连接器。** 将 `.mcp.json` 指向你的合同管理系统、文档管理系统、电子取证平台、上线追踪器、HR 系统。连接器未配置时技能优雅降级——不会静默空转。
- **带入你的审查指引和模板。** 将你的术语、内部风格和品牌模板放入插件的 `CLAUDE.md` 和 `references/`。技能会自动拾取。
- **Fork 技能适配内部风格。** 每个技能是 `skills/` 下的一个 markdown 文件。编辑步骤、门槛和输出格式。
- **添加定时 Agent。** `<插件名>/agents/` 下的 Agent 是带 cron 风格调度的 markdown 文件。为你的团队所需的监控任务添加自定义 Agent。

无需构建步骤。一切皆为 Markdown 和 JSON。

## 技能与命令参考

所有插件的完整命令映射。冷启动面试是任何插件中第一个要运行的东西。

### ai-governance-legal

| 命令 | 技能 | 功能 |
|------|------|------|
| `/ai-governance-legal:cold-start-interview` | cold-start-interview | 冷启动——了解你的 AI 治理实践 |
| `/ai-governance-legal:use-case-triage` | use-case-triage | 对 AI 应用场景分类——批准/附条件/禁止 |
| `/ai-governance-legal:aia-generation` | aia-generation | 按内部格式运行 AI 影响评估（算法安全评估/科技伦理审查） |
| `/ai-governance-legal:vendor-ai-review` | vendor-ai-review | 依据治理立场审查供应商 AI 条款 |
| `/ai-governance-legal:reg-gap-analysis` | reg-gap-analysis | 将新 AI 法规与你的治理状态进行差异比对 |
| `/ai-governance-legal:policy-monitor` | policy-monitor | 保持 AI 政策与实践同步 |
| `/ai-governance-legal:policy-starter` | policy-starter | 基于已发布的示范政策起草律所/企业 AI 使用政策 |
| `/ai-governance-legal:matter-workspace` | matter-workspace | 管理事项工作空间 |

### legal-builder-hub

| 命令 | 技能 | 功能 |
|------|------|------|
| `/legal-builder-hub:cold-start-interview` | cold-start-interview | 实践画像面试和入门包推荐 |
| `/legal-builder-hub:registry-browser` | registry-browser | 搜索已关注注册表中的社区法律技能 |
| `/legal-builder-hub:skill-installer` | skill-installer | 安装社区技能，含信任检查 |
| `/legal-builder-hub:skills-qa` | skills-qa | 依据设计框架评估技能 |
| `/legal-builder-hub:related-skills-surfacer` | related-skills-surfacer | 基于其他插件的活动推荐社区技能 |
| `/legal-builder-hub:auto-updater` | auto-updater | 检查已安装社区技能的更新 |
| `/legal-builder-hub:disable` | skill-manager | 禁用社区技能而不删除文件 |
| `/legal-builder-hub:uninstall` | skill-manager | 卸载通过 hub 安装的社区技能 |
| scheduled | registry-sync (agent) | 定期检查已关注注册表的更新 |

### legal-clinic

| 命令 | 技能 | 功能 |
|------|------|------|
| `/legal-clinic:cold-start-interview` | cold-start-interview | 指导老师设置——领域、管辖、指导风格 |
| `/legal-clinic:build-guide` | build-guide | 指导老师业务领域指南——接待、教学模式、审查门槛 |
| `/legal-clinic:ramp` | ramp | 学生学期导入，含实践练习 |
| `/legal-clinic:client-intake` | client-intake | 结构化接待，含跨领域问题识别 |
| `/legal-clinic:client-comms-log` | client-comms-log | 记录客户沟通——每个案件仅追加 |
| `/legal-clinic:research-start` | research-start | 检索路线图——法条、案例、检索关键词 |
| `/legal-clinic:memo` | memo | IRAC 结构分析备忘录，标注研究缺口 |
| `/legal-clinic:draft` | draft | 常用法律诊所文件的初稿 |
| `/legal-clinic:client-letter` | client-letter · plain-language-letters | 基于模板的常规客户信函 |
| `/legal-clinic:status` | status | 按受众分类的案件状态——客户、教授、法院 |
| `/legal-clinic:deadlines` | deadlines | 追踪案件节点，含执业风险警告 |
| `/legal-clinic:supervisor-review-queue` | supervisor-review-queue | 教授审查队列（如配置正式审查督导） |
| `/legal-clinic:semester-handoff` | semester-handoff | 期末案件移交备忘录 |

### commercial-legal

| 命令 | 技能 | 功能 |
|------|------|------|
| `/commercial-legal:cold-start-interview` | cold-start-interview | 冷启动——了解你的商事合同实践 |
| `/commercial-legal:review` | vendor-agreement-review · nda-review · saas-msa-review | 审查供应商协议、保密协议或 SaaS 订阅合同 |
| `/commercial-legal:amendment-history` | amendment-history | 追踪合同从原始版本到历次修订的变更 |
| `/commercial-legal:renewal-tracker` | renewal-tracker | 显示 90 天内解约截止日期的合同 |
| `/commercial-legal:escalation-flagger` | escalation-flagger | 路由合同问题并起草请示 |
| `/commercial-legal:review-proposals` | (internal) | 审查和批准待处理的审查指引更新建议 |
| `/commercial-legal:matter-workspace` | matter-workspace | 管理事项工作空间 |
| — | stakeholder-summary | 将审查结果转化为业务人员可读的摘要 |
| scheduled | renewal-watcher (agent) | 每周扫描续签台账 |
| scheduled | deal-debrief (agent) | 每周汇总含偏离项的已签署协议 |
| scheduled | playbook-monitor (agent) | 当条款持续偏移时建议审查指引更新 |

### corporate-legal

| 命令 | 技能 | 功能 |
|------|------|------|
| `/corporate-legal:cold-start-interview` | cold-start-interview | 内部冷启动，可选 `--new-deal` 启动新交易 |
| `/corporate-legal:tabular-review` | tabular-review | 表格式审查——每份文件一行，每格附带引用 |
| `/corporate-legal:diligence-issue-extraction` | diligence-issue-extraction | 按内部阈值从数据室文件中提取问题 |
| `/corporate-legal:material-contract-schedule` | material-contract-schedule | 编制重大合同披露清单 |
| `/corporate-legal:closing-checklist` | closing-checklist | 阻碍交割的事项和关键路径 |
| `/corporate-legal:written-consent` | written-consent | 按内部格式起草董事会/股东会决议 |
| `/corporate-legal:entity-compliance` | entity-compliance | 跨地域企业合规追踪 |
| `/corporate-legal:integration-management` | integration-management | 交割后整合追踪，含同意管理 |
| `/corporate-legal:matter-workspace` | matter-workspace | 管理事项工作空间 |
| — | board-minutes | 按内部格式起草董事会/股东会会议纪要 |
| — | deal-team-summary | 将尽调发现汇总为交易简报 |
| — | ai-tool-handoff | 检测 AI 尽调工具输出，进行质量检查 |
| scheduled | dataroom-watcher (agent) | 监控数据室上传并推送清单状态 |

### employment-legal

| 命令 | 技能 | 功能 |
|------|------|------|
| `/employment-legal:cold-start-interview` | cold-start-interview | 冷启动——了解用工地区和升级规则 |
| `/employment-legal:wage-hour-qa` | wage-hour-qa | 劳动用工法律问答 |
| `/employment-legal:hiring-review` | hiring-review | 审查录用通知和竞业限制/服务期条款 |
| `/employment-legal:termination-review` | termination-review | 解除审查，含高风险标记检测 |
| `/employment-legal:worker-classification` | worker-classification | 依据〔2005〕12号三要素认定劳动关系 |
| `/employment-legal:policy-drafting` | policy-drafting | 起草劳动规章制度（含民主程序和公示） |
| `/employment-legal:leave-tracker` | leave-tracker | 检查在休假期中的截止日期预警 |
| `/employment-legal:log-leave` | log-leave | 新增假期记录 |
| `/employment-legal:investigation-open` | internal-investigation | 启动新的内部调查事项 |
| `/employment-legal:investigation-add` | internal-investigation | 向进行中的调查添加数据——文件、笔记 |
| `/employment-legal:investigation-memo` | internal-investigation | 起草或更新调查备忘录 |
| `/employment-legal:investigation-query` | internal-investigation | 就已开调查记录提问 |
| `/employment-legal:investigation-summary` | internal-investigation | 基于调查备忘录起草按受众分类的摘要 |
| `/employment-legal:expansion-kickoff` | international-expansion | 启动新省份用工规划 |
| `/employment-legal:expansion-update` | international-expansion | 更新进行中的跨省用工项目状态 |
| `/employment-legal:matter-workspace` | matter-workspace | 管理事项工作空间 |
| — | handbook-updates | 差异对比员工手册变更并标记地区影响 |
| scheduled | leave-tracker (agent) | 每周监控在休假期（含硬截止日期） |

### ip-legal

| 命令 | 技能 | 功能 |
|------|------|------|
| `/ip-legal:cold-start-interview` | cold-start-interview | 冷启动——了解你的知识产权实践和策略 |
| `/ip-legal:clearance` | clearance | 商标可注册性初步检索——相同/近似筛查 |
| `/ip-legal:fto-triage` | fto-triage | 自由实施初步分析（非正式 FTO 意见） |
| `/ip-legal:cease-desist` | cease-desist | 起草侵权警告函或分流收到的警告函 |
| `/ip-legal:takedown` | takedown | 通知-删除及反通知（信息网络传播权保护条例） |
| `/ip-legal:infringement-triage` | infringement-triage | 跨四种知识产权的侵权初步分流 |
| `/ip-legal:ip-clause-review` | ip-clause-review | 审查知识产权条款——转让、许可、保证 |
| `/ip-legal:oss-review` | oss-review | 开源许可证合规检查 |
| `/ip-legal:portfolio` | portfolio | 追踪知识产权组合的截止日期和续展 |
| `/ip-legal:matter-workspace` | matter-workspace | 管理事项工作空间 |
| scheduled | ip-renewal-watcher (agent) | 每周知识产权组合截止日期报告 |

### litigation-legal

| 命令 | 技能 | 功能 |
|------|------|------|
| `/litigation-legal:cold-start-interview` | cold-start-interview | 冷启动——风险、格局、内部文书风格 |
| `/litigation-legal:matter-intake` | matter-intake | 登记新案件——写入案件文件和历史记录 |
| `/litigation-legal:matter-briefing` | matter-briefing | 单个案件深度简报——会议准备 |
| `/litigation-legal:matter-update` | matter-update | 为案件历史追加带日期的事件 |
| `/litigation-legal:portfolio-status` | portfolio-status | 案件组合汇总——风险、截止日期、停滞案件 |
| `/litigation-legal:matter-close` | matter-close | 结案——归档、保留记录 |
| `/litigation-legal:matter-workspace` | matter-workspace | 管理事项工作空间 |
| `/litigation-legal:demand-intake` | demand-intake | 律师函起草前准备——当事人、事实、谈判筹码 |
| `/litigation-legal:demand-draft` | demand-draft | 起草律师函，设置发送门槛 |
| `/litigation-legal:demand-received` | demand-received | 分流收到的律师函——选项、案件交叉检查 |
| `/litigation-legal:subpoena-triage` | subpoena-triage | 分流法院调查令/协查通知——范围、负担、方案 |
| `/litigation-legal:legal-hold` | legal-hold | 签发、更新、解除或报告证据保全 |
| `/litigation-legal:oc-status` | oc-status | 致外部律师的每周状态催问 |
| `/litigation-legal:claim-chart` | claim-chart | 要件分析表——专利或民事案由 |
| `/litigation-legal:chronology` | chronology | 从来源和上传材料构建或更新大事记 |
| `/litigation-legal:deposition-prep` | deposition-prep | 庭前准备提纲——与案件理论挂钩 |
| `/litigation-legal:privilege-log-review` | privilege-log-review | 第一轮证据三性审查，附标记 |
| `/litigation-legal:brief-section-drafter` | brief-section-drafter | 按内部风格起草法律文书章节 |
| scheduled | docket-watcher (agent) | 监控法院案件进展和截止日期 |

### privacy-legal

| 命令 | 技能 | 功能 |
|------|------|------|
| `/privacy-legal:cold-start-interview` | cold-start-interview | 冷启动——了解你的隐私数据实践 |
| `/privacy-legal:use-case-triage` | use-case-triage | 判断是否需要个保法第55条评估或可直接推进 |
| `/privacy-legal:pia-generation` | pia-generation | 按内部格式生成个人信息保护影响评估报告 |
| `/privacy-legal:dpa-review` | dpa-review | 审查个人信息处理协议——自动检测控制者/处理者 |
| `/privacy-legal:dsar-response` | dsar-response | 处理主体权利请求并起草回复——核实、定位、评估 |
| `/privacy-legal:reg-gap-analysis` | reg-gap-analysis | 将法规与现行政策和实践进行差异比对 |
| `/privacy-legal:policy-monitor` | policy-monitor | 保持隐私政策与实践同步 |
| `/privacy-legal:matter-workspace` | matter-workspace | 管理事项工作空间 |

### product-legal

| 命令 | 技能 | 功能 |
|------|------|------|
| `/product-legal:cold-start-interview` | cold-start-interview | 冷启动——连接上线追踪器，了解风险校准 |
| `/product-legal:is-this-a-problem` | is-this-a-problem | 快速判断——对"快速问答"给出即时答案 |
| `/product-legal:launch-review` | launch-review | 依据框架和校准进行完整上线审查 |
| `/product-legal:marketing-claims-review` | marketing-claims-review | 审查需要调整的营销文案（广告法/反不正当竞争法） |
| `/product-legal:matter-workspace` | matter-workspace | 管理事项工作空间 |
| — | feature-risk-assessment | 当上线审查标记时对单个功能的深度风险评估 |
| scheduled | launch-watcher (agent) | 监控上线追踪器中即将需要审查的产品 |

### regulatory-legal

| 命令 | 技能 | 功能 |
|------|------|------|
| `/regulatory-legal:cold-start-interview` | cold-start-interview | 冷启动——监控清单、政策索引、重要性阈值 |
| `/regulatory-legal:reg-feed-watcher` | reg-feed-watcher | 即时检查法规动态并报告更新 |
| `/regulatory-legal:policy-diff` | policy-diff | 将法规变化与政策库进行差异比对 |
| `/regulatory-legal:gaps` | gap-surfacer | 开放差距追踪器——已标记尚未关闭的项目 |
| `/regulatory-legal:policy-redraft` | policy-redraft | 带修改标记的政策重述——供政策负责人审阅的建议稿 |
| `/regulatory-legal:comments` | (tracker) | 审查开放的征求意见期和截止日期 |
| `/regulatory-legal:matter-workspace` | matter-workspace | 管理事项工作空间 |
| scheduled | reg-change-monitor (agent) | 定时法规动态扫描，含重要性过滤 |

### law-student

| 命令 | 技能 | 功能 |
|------|------|------|
| `/law-student:cold-start-interview` | cold-start-interview | 关于你的面试——课程、法考、学习风格 |
| `/law-student:socratic-drill` | socratic-drill | 课堂问答训练——它问、你答、它追问 |
| `/law-student:case-brief` | case-brief | 按你偏好的格式做案例摘要 |
| `/law-student:outline-builder` | outline-builder | 按你的格式构建或扩展知识体系 |
| `/law-student:irac-practice` | irac-practice | IRAC 作文评分——结构、问题、规则、分析 |
| `/law-student:legal-writing` | legal-writing | 对你写作的结构性反馈——从不代写 |
| `/law-student:cold-call-prep` | cold-call-prep | 预测教授提问并进行针对性训练 |
| `/law-student:bar-prep-questions` | bar-prep-questions | 针对薄弱科目的客观题或主观题练习 |
| `/law-student:flashcards` | flashcards | 生成或训练记忆卡片——Leitner 式 |
| `/law-student:exam-forecast` | exam-forecast | 分析历年试题以预测可能重点 |
| `/law-student:study-plan` | study-plan | 构建或更新长期学习计划 |
| `/law-student:session` | study-plan | 运行一个 N 题的专注学习单元并更新计划 |

## 贡献

一切皆为 Markdown 和 JSON。Fork、编辑、提交 PR。

- **新技能** → 添加到 `<插件名>/skills/<技能名>/SKILL.md`，使用现有技能的前置元数据（`name`、`description`、`argument-hint`）。描述保持在 1024 字符以内——这是触发信号。技能可通过 `/<插件名>:<技能名>` 调用。纯参考技能标记 `user-invocable: false`。
- **新 Agent** → 添加 `<插件名>/agents/<名称>.md`，含调度前置元数据和 system prompt。如需无头部署，添加匹配的 `managed-agent-cookbooks/<名称>/`。
- **社区技能** → 使用 `/legal-builder-hub:skill-installer` 在你的环境中测试社区技能。Hub 在每次安装前运行 `/legal-builder-hub:skills-qa`，对技能进行评分（九个设计参数、三种法律失败模式、信任面检查），拒绝任何不通过的技能。
- **推送前验证蓝图** → `bash scripts/test-cookbooks.sh` 对所有托管 Agent 蓝图进行预检，并对编排器工具范围进行 lint。

## 许可证

依据 [Apache License, Version 2.0](LICENSE) 许可。

<p align="center">
  <img src="docs/assets/about.png" alt="关于作者 — 着陆页 About 区域" width="800">
</p>

## 关于作者

**陈石律师**，浙江海泰律师事务所副主任、高级合伙人、房地产与建设工程部主任，宁波市律师协会副秘书长、第七届宁波仲裁委员会仲裁员，聚焦建筑房地产、投融资、并购重组及商事争议解决。曾获多家法律媒体与专业机构认可，荣登 LegalOne 2025 中国区建工及房地产实务先锋 45 强、律新社 2025 年度管理合伙人 20 佳（华东），入选《商法》The A-List 法律精英，获评 ALB China 区域市场十五佳长三角地区律师新星，并获律新社 2024 年度并购领域品牌之星。长期为万科、华润置地、信达地产、保利置业、招商蛇口、中海地产等企业提供法律服务，承办"首宗百亿地王""长春第一高楼""台州第一高楼"等代表性项目，累计服务项目投资额超千亿。近年来持续推动 AI 与法律实务融合，强调以结构化方法打通技术逻辑、法律判断与商业场景；著有《赋能法律人：AI 底层思维与应用范式》，并在多地开展相关主题讲座与分享。

本中国法适配版本由陈石律师基于其本地法律知识库体系和多年法律实务经验完成从美国法到中国法的系统改造。

<p align="center">
  <img src="docs/assets/testimonial.png" alt="用户评价" width="800">
</p>

## 社区贡献者

感谢每一位为本项目做出贡献的社区成员 🎉

<table align="center">
  <tr>
    <td align="center" width="300">
      <a href="https://github.com/kanekanefy">
        <img src="https://github.com/kanekanefy.png" width="80" style="border-radius: 50%;" alt="kanekanefy"><br>
        <b>@kanekanefy</b>
      </a><br>
      Codex 多端适配层<br>一键安装脚本
    </td>
    <td align="center" width="300">
      <a href="https://github.com/icedfish">
        <img src="https://github.com/icedfish.png" width="80" style="border-radius: 50%;" alt="Xiaopai"><br>
        <b>@icedfish</b>（Xiaopai）
      </a><br>
      知识库检索约定收敛<br>民诉法条号修正
    </td>
  </tr>
</table>

<p align="center"><sub>头像来自 GitHub，点击可跳转至贡献者主页</sub></p>

---

## 致谢

- **[Anthropic](https://www.anthropic.com/)** — 提供 `claude-for-legal` 开源插件框架和 Claude 模型能力，为中国法本地化改造奠定了坚实基础
- **[DeepSeek-V4](https://www.deepseek.com/)** — 提供优惠算力支持，使大规模法律技能文件的本地化改造在经济上可行
- **[浙江海泰律师事务所](https://www.hightac.com/)** — 提供专业成长环境和实务土壤，本版本中融入的合同审查方法论、诉讼分析框架和风险评价体系均源于海泰的长期培养

---

<p align="center">
  <img src="docs/assets/cta.png" alt="开始使用 Claude for Legal" width="800">
</p>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CSlawyer1985/claude-for-legal-ZH&type=Date)](https://www.star-history.com/?repos=CSlawyer1985%2Fclaude-for-legal-ZH)
