# Project Engineering Context

## 初衷

本工程不是重新编写一套“大而全”的 `SKILL.md`。它要建立一个 Engineering Governance Manager：对成熟工程 Skill 做采集、筛选、组合、版本化和实际验证，并根据项目上下文、任务阶段、风险和质量门选择能力：

```text
Superpowers -> Engineering Modules -> Profiles -> Actual Project
```

Superpowers 是开发流程底座，Engineering Modules 是本地治理与工程规则，Profiles 是针对项目类型的激活配置，Actual Project 提供事实和行为证据。Registry、Evaluation 和 Integration 负责版本、采用关系、成熟度、Harness 适配和验证结果。

Project Engineering 是第一个大型 Skill Stack，目标是最终用于真实 C++/Qt/QML 项目的架构分析、设计、实现、审查和重构。

## 核心资产

本工程自己维护五类资产：

1. **Registry**：来源、许可证、版本、能力、成熟度和证据；
2. **Evaluation**：用真实项目案例判断 Skill 是否有效；
3. **Governance**：定义角色、质量门、稳定产物和领域适配规则；
4. **Composition**：定义路由、调用顺序、输入输出传递和冲突裁决。
5. **Profiles / Integrations**：分别定义项目类型激活组合和外部流程底座接入方式。

上游 Skill 保持原始内容和固定版本。需要本地适配时，只增加薄的 adapter、路由或评估规则，不复制并重写成熟上游能力。

## 五类能力模型

对外统一使用五类概念：**Role** 定义责任，**Skill** 执行具体动作，**Standard** 定义合格约束，**Workflow** 编排阶段和门禁，**Superpower** 提供跨多个 Skill 的高阶组合方法。详细定义见 [governance/taxonomy.md](governance/taxonomy.md)。

五类能力不是五个互相独立的目录层级。Role、Skill、Standard 和 Workflow 是日常编排的基本单元；Superpower 是可选的组合能力包。Registry、Evaluation 和 Engineering Governance Manager 属于管理平面，负责来源、版本、成熟度、证据和路由。

## 质量原则

- `S0 Candidate -> S1 Reviewed -> S2 Tested -> S3 Proven -> S4 Core`；没有行为证据的组件不能进入 Core。
- 能力选择优先于仓库选择：先问需要什么能力，再选择最合适的 Skill。
- 工作流、质量门、架构参考、案例库和发现索引分层管理，避免把所有内容塞进一个入口文件。
- C++/Qt/QML 的线程、QObject 生命周期、信号槽、Model/View、构建和 ABI 语义必须由本地领域规则与项目事实确认。
- 结论必须能追溯到固定来源、代码证据、测试结果或人工评估；Star 数量和主观偏好不能替代验证。

## 当前阶段

Registry v0.1 已收录四个第一轮来源：

- `obra/superpowers`：固定版本的开发流程底座；
- `addyosmani/agent-skills`：Engineering Quality 候选；
- `microsoft/FluidFramework` review：真实工程 Review Benchmark；
- `byliu-labs/claude-skill-architecture-review`：Architecture Review Reference。

来源和组件当前均为 `S1 Reviewed`，尚未声称已经在真实 C++/Qt 项目中通过行为评估。下一阶段是选定一个真实项目，运行架构、Review 和行为保持重构案例，依据结果晋升、降级或淘汰组件。

## 当前重构授权

在工程结构、Registry 约定和组合方式正式定型之前，允许根据审计结果和真实项目验证主动重构本仓库，包括目录、文件、命名、Registry schema、路由、评估方式和现有规则的组织方式。此阶段优先追求结构正确、职责清晰和可验证性；不需要为了保持初版结构而保留明显不合理的设计。结构定型后，再切换为受控的增量演进。

## 角色与门禁模型

Manager 由八个治理角色组成：Architect、Engineering Standards、Project Structure Manager、Workflow Manager、Test Engineer、Code Reviewer、Technical Debt Manager 和 ADR Manager。角色表示需要承担的责任，不要求一项任务创建八个 Agent。

任务沿 `Requirement -> Architecture -> Design -> Plan -> Implementation -> Test -> Review -> Delivery` 推进。每个阶段通过对应 Gate，并留下决策、测试、审查、债务或交付记录；风险较低时可以合并阶段，但不能跳过与变更事实相关的验证。

## 最终使用方式

面对真实需求时，系统应先判断任务类型，再组合适用能力：

```text
需求与约束
  -> 架构分析
  -> 模块边界与接口
  -> 实现与测试
  -> 代码/架构审查
  -> 验证、ADR 和交付记录
```

Project Engineering 的价值在于这条组合链是否能持续改善真实项目结果，而不是仓库里收集了多少 Skill。
