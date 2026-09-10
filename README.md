# Project Engineering Skill

这是面向 C++/Qt/QML 项目的 Engineering Governance Manager。它根据项目上下文、任务阶段和风险，组合上游能力、本地治理规则和质量门，支持架构分析、设计、实现、测试、审查和重构。

总入口：[SKILL.md](SKILL.md)

项目目标与长期边界：[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)

## 目录

- `governance/architecture/`：架构分析、模块边界、依赖和分层
- `policies/`：C++、Qt、QML、命名、错误处理和复杂度
- `governance/design/`：接口、所有权、职责和数据流
- `governance/review/`：代码、模块、依赖和架构 review
- `templates/`：ADR、模块说明、架构说明、测试计划、审查报告和技术债模板
- `skills/`：按需加载的官方增强 skill
- `registry/`：来源、能力、候选组件、角色、风险规则和阶段门禁登记
- `profiles/`：按项目类型激活 Standards、Skills、Superpowers 和 Gates
- `integrations/`：Superpowers 与不同 Harness 的版本、映射和适配规则
- `sources/`：上游原始快照与审计记录
- `evaluations/`：能力评估案例与 Guard 最小实验；实验通过不自动晋级
- `workflow/`：Skill 路由、顺序和冲突处理
- `stack/`：当前采用的 Project Engineering 组合
- `roles/`：11 个工程角色及其输入输出责任
- `scripts/`、`tests/`：证据门禁检查器与验证测试
- `technical-debt/`：影响当前决策的技术债登记
- `governance/taxonomy.md`：Role、Skill、Standard、Workflow、Superpower 五类能力模型

## 组合层次

```text
Superpowers -> Engineering Modules -> Profiles -> Actual Project
```

Superpowers 提供开发流程底座，Project Engineering 提供工程标准、治理模块和质量证据；Profile（例如 `profiles/qt-project.yaml`）决定一个真实项目启用哪些能力。

## 新建项目与风险发现

按 [新建项目 Workflow](workflow/new-project.md) 从项目事实、需求与验收开始，沿需求 → 架构 → 设计 → 计划 → 实现 → 测试 → 审查 → 交付执行。Explorer 读取事实，专业角色分析，Engineering Guardian 在阶段边界检查风险与遗漏。

当前包含 8 类风险、12 条规则、8 个阶段门禁。目标项目自己保存 `.engineering/run.yaml`、实际问题和证据；Registry 只保存可复用规则。初始化命令只建立运行记录，业务骨架由 Agent 按需求创建。

```powershell
python -m pip install -r requirements.txt
python scripts/engineering_guard.py validate
python scripts/engineering_guard.py init --project D:/Projects/MyProject --profile qt-project --features queue
python scripts/engineering_guard.py check --project D:/Projects/MyProject --stage architecture
```

无证据的新记录会阻断。检查器验证文件散列、版本、所需记录和风险状态；Agent 负责实际分析、执行工具和判断证据语义。目前不包含自动扫描器或后台调度。S1 组件为显式参考/评估候选，只有 S4 可默认启用。

规则与格式见 [风险发现 Workflow](workflow/risk-discovery.md)，实测结果见 [Qt 队列实验](evaluations/guard/README.md)，设计取舍见 [ADR-0001](governance/architecture/decisions/0001-evidence-based-guard.md)。

## 更新约定

每次修改框架或新增 skill 后，在“更新记录”顶部追加一条记录，至少包含：

- 日期
- 更新内容
- 影响范围
- 验证方式和结果
- 已知风险或后续待办

记录应简洁、可追溯；重大架构变化使用 `templates/ADR.md` 创建实际决策记录，保存在 `governance/architecture/decisions/`，需要时使用架构模板补充说明。

## 更新记录

### 2026-09-10：实现跨阶段 Engineering Guard 最小闭环

- 更新内容：新增 Explorer、Developer、Guardian 角色，角色/风险/门禁 Registry，目标项目证据记录及检查器；补齐新建项目入口并统一候选组件与 S4 默认启用的边界。
- 影响范围：入口、Stack、Profiles、Registry、Workflow、运行模板、Python 检查器及 QtCore 示例；上游快照未改写。
- 验证方式/结果：门禁 16 项测试通过；本机 MSVC/Qt5/CMake 配置和构建成功，5 项 CTest 通过；同一过载测试在无界对照上失败、有界实现上通过；风险未关闭的回放记录阻断，补齐证据后八阶段记录检查通过。
- 已知风险或后续待办：记录检查不等于自动发现或语义验证；实验采用单 Agent 与已知缺陷，尚未证明上游 Skill 增量价值，成熟度不变。下一步在真实业务变更中评估误报、漏报和实际使用成本。

### 2026-09-09：建立 Profile 与 Superpowers Integration 层

- 更新内容：新增 Skill 级 Registry、跨来源兼容矩阵、C++/Qt 项目 Profiles，以及 Superpowers 固定版本集成映射。
- 影响范围：`registry/skills.yaml`、`registry/compatibility.yaml`、`profiles/`、`integrations/superpowers/`、`SKILL.md`、`PROJECT_CONTEXT.md`、`governance/taxonomy.md`。
- 验证方式/结果：完成组件 ID、路径和加载顺序的静态核对；提交前执行全量链接、路径和 YAML 结构检查。
- 已知风险或后续待办：所有组件仍需在真实 C++/Qt 项目案例中完成 S2 行为评估。

### 2026-09-09：确定五类能力模型

- 更新内容：定义 Role、Skill、Standard、Workflow、Superpower 五类能力，并明确 Registry、Evaluation 和 Manager 属于管理平面。
- 影响范围：`governance/taxonomy.md`、`PROJECT_CONTEXT.md`、`SKILL.md`、目录理解和后续 Registry schema。
- 验证方式/结果：完成五类之间的关系、粒度和路由边界说明；本地链接检查通过。
- 已知风险或后续待办：后续需要为 Registry 增加 `kind`、`composes` 和 `provided_by` 字段，登记真实 Superpower 组合。

### 2026-09-09：重构为 Engineering Governance Manager

- 更新内容：将入口、Stack 和 Workflow 重组为八角色与 Requirement 到 Delivery 的质量门链；补充技术债登记、测试计划和审查报告模板。
- 影响范围：`SKILL.md`、`roles/`、`workflow/`、`stack/`、`technical-debt/`、`templates/`、`registry/`。
- 验证方式/结果：全量本地 Markdown 链接、旧路径扫描、上游快照 manifest 和 `git diff --check` 均通过；YAML 结构已完成静态字段和组件 ID 核对。
- 已知风险或后续待办：仍需在真实 C++/Qt/QML 项目运行案例，验证角色路由和门禁是否产生有效工程证据。

### 2026-09-09：明确未定型阶段的结构性重构授权

- 更新内容：允许在 Project Engineering 结构定型前主动重构目录、Registry、路由、评估方式和规则组织。
- 影响范围：`PROJECT_CONTEXT.md`、`SKILL.md` 及后续仓库结构演进。
- 验证方式/结果：同步更新项目上下文、总入口和停止条件。
- 已知风险或后续待办：结构定型前可能出现多次 schema 或目录调整，需要保持更新记录和迁移说明。

### 2026-09-09：建立工程 skill 框架初版

- 建立总控路由 `SKILL.md`，支持按任务选择分析、设计、实现、审查和重构规则。
- 建立 `governance/architecture/`、`policies/`、`governance/design/`、`governance/review/` 和 `templates/` 目录及基础规则。
- 加入官方增强 skill：`security-best-practices`、`security-threat-model`、`security-ownership-map`、`gh-address-comments`、`gh-fix-ci`。
- 完成所有 skill 的 frontmatter 和本地链接检查。

### 2026-09-09：建立上游 Skill Registry v0.1

- 收录并固定审计 `obra/superpowers`、`addyosmani/agent-skills`、`microsoft/FluidFramework` review 和 `byliu-labs/claude-skill-architecture-review` 四个来源。
- 增加来源元数据、原始快照校验清单、能力矩阵、评估案例模板、组合路由和首版 stack 配置。
- 影响范围：`registry/`、`sources/`、`evaluations/`、`workflow/`、`stack/`。
- 验证方式/结果：完成 GitHub API 提交、树结构、许可证和原始文件 SHA 校验；本地链接检查通过。
- 已知风险或后续待办：尚未在真实 C++/Qt 项目执行行为评估，四个来源暂定为 S1 Reviewed。

## 更新条目模板

复制下面的区块，放到“更新记录”最上方：

```markdown
### YYYY-MM-DD：简短标题

- 更新内容：
- 影响范围：
- 验证方式/结果：
- 已知风险或后续待办：
```
