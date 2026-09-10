---
name: project-engineering
description: 面向 C++/Qt/QML 项目的 Engineering Governance Manager，根据项目上下文、任务阶段、风险和治理门禁选择并编排工程能力。
metadata:
  short-description: Engineering Governance Manager for C++/Qt/QML projects
---

# Engineering Governance Manager

这是 Project Engineering 的总入口。它管理工程决策和验证链，不把所有规则一次性加载，也不把上游 Skill 复制成另一套总规则。

## 管理循环

```text
项目上下文 -> 任务阶段与风险 -> 角色 -> 能力组件 -> 质量门 -> 可追溯交付物
```

能力按五类理解：[Role](governance/taxonomy.md#五类能力)、Skill、Standard、Workflow 和 Superpower。Manager 负责把它们组合起来；Registry 和 Evaluation 负责版本、成熟度与证据，不直接替代任何一类能力。实际激活通过 [Profiles](profiles/qt-project.yaml) 完成，Harness 接入规则见 [Superpowers Integration](integrations/superpowers/manifest.yaml)。

每次任务按以下顺序工作：

1. 读取项目事实：目录、构建入口、测试、运行时约束、兼容性要求和现有 ADR。
2. 判断阶段和风险，激活一个或多个角色；Workflow Manager 负责去重、排序和冲突裁决。
3. 从 [registry/skills.yaml](registry/skills.yaml) 和 [registry/compatibility.yaml](registry/compatibility.yaml) 选择 Skill；再按 [Profile](profiles/qt-project.yaml) 和 [stack/project-engineering.yaml](stack/project-engineering.yaml) 组装能力。固定的 `sources/` 快照只作为原始证据。
4. 按门禁推进：Requirement -> Architecture -> Design -> Plan -> Implementation -> Test -> Review -> Delivery。
5. 将结论写入稳定产物，并把证据回填到 [evaluations/](evaluations/)。未经过 S2 评估的组件不能成为默认 Core。

## 阶段、角色与门禁

| 阶段 | 主要角色 | 必要门禁 | 主要产物 |
| --- | --- | --- | --- |
| Requirement | Workflow Manager、Architect | [Requirement Gate](workflow/requirement.md) | 目标、非目标、约束、验收标准 |
| Architecture | Architect、Project Structure Manager、ADR Manager | [Architecture Gate](workflow/architecture-gate.md) | 现状分析、候选方案、边界、ADR |
| Design | Architect、Engineering Standards | [Architecture Gate](workflow/architecture-gate.md) | 接口、所有权、数据流和适用策略 |
| Plan | Workflow Manager、Test Engineer | [Implementation Gate](workflow/implementation-gate.md) | 分步计划、风险、回滚点、测试计划 |
| Implementation | Engineering Standards、Project Structure Manager | [Implementation Gate](workflow/implementation-gate.md) | 代码、配置、迁移和变更记录 |
| Test | Test Engineer | [Test Gate](workflow/test-gate.md) | [TEST_PLAN](templates/TEST_PLAN.md)、命令、结果和缺口 |
| Review | Code Reviewer、Technical Debt Manager | [Review Gate](workflow/review-gate.md) | [REVIEW](templates/REVIEW.md)、债务登记和修复结论 |
| Delivery | ADR Manager、Workflow Manager | [Review Gate](workflow/review-gate.md) | ADR、验证摘要、已知风险和后续事项 |

门禁按风险收缩或扩展，但不能跳过与变更事实直接相关的验证。重大架构、公共 API、线程/生命周期、持久化格式和跨模块迁移必须留下决策与回滚条件。

## 角色与规则加载

角色说明位于 [roles/](roles/)。角色不是必须创建的独立 Agent，而是一次任务中需要承担的工程责任。按需加载：

- Architect：读取 [governance/architecture/](governance/architecture/) 和 [governance/design/](governance/design/)；重大平台、同步、桥接、sidecar 或 adapter 变化再调用架构参考组件。
- Engineering Standards：读取 [policies/](policies/) 中与语言、框架、构建和兼容性匹配的策略。
- Project Structure Manager：读取 [module-boundary.md](governance/architecture/module-boundary.md)、[dependency-rules.md](policies/dependency-rules.md) 和 [layering.md](policies/layering.md)。
- Workflow Manager：读取 [workflow/routing.md](workflow/routing.md)、[workflow/conflict-resolution.md](workflow/conflict-resolution.md) 和当前 Stack。
- Test Engineer：读取 [workflow/test-gate.md](workflow/test-gate.md) 与项目测试事实，按风险选择测试层级。
- Code Reviewer：读取 [governance/review/](governance/review/)；需要时加载安全增强 skill 和上游审查基准。
- Technical Debt Manager：读取 [roles/technical-debt-manager.md](roles/technical-debt-manager.md) 和 [technical-debt/registry.yaml](technical-debt/registry.yaml)。
- ADR Manager：读取 [templates/ADR.md](templates/ADR.md) 和现有 ADR，确保决策、迁移和回滚可追溯。

Superpowers 通过 [integrations/superpowers/](integrations/superpowers/) 作为开发流程底座，负责怎么开发；Addy Agent Skills 通过 Registry 作为工程质量层，负责按照什么工程标准开发。FluidFramework review 是审查基准，byliu 是重大架构决策参考。上游原始内容只从 `sources/` 的固定快照加载，来源流行度不能替代代码、构建、测试和项目证据。

## 组合层次

```text
Superpowers -> Engineering Modules -> Profiles -> Actual Project
```

- Superpowers：跨 Harness 的开发流程底座。
- Engineering Modules：本地 Governance、Policies、Workflow、Roles 与被采用的 Skills。
- Profile：针对项目类型的激活配置，例如 `qt-project`；它不是第六类能力。
- Actual Project：提供目录、构建、测试、兼容性和发布事实，并产出评估证据。

## 输出协议

所有结论都要说明输入事实、适用角色、使用的组件、验证证据、未覆盖区域和下一步。审查 finding 按阻断、高、中、低排序，并包含位置、触发条件、证据、影响和修复方向。发现冲突时保留项目约束和可验证事实，记录取舍，必要时创建 ADR。

结构定型前，本仓库内部的目录、Registry、路由、评估方式和规则组织可以继续重构；对真实业务项目的代码、依赖、数据格式和发布操作，仍按实际任务范围执行。
