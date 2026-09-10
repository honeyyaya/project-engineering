# Engineering Capability Taxonomy

Project Engineering 对外使用五类能力概念。Engineering Governance Manager 负责在它们之间路由；`Registry` 和 `Evaluation` 是支撑这些概念的管理平面，不作为第六类运行时能力。

## 五类能力

| 类别 | 回答的问题 | 典型内容 | 粒度 |
| --- | --- | --- | --- |
| **Role** | 谁对哪类工程责任负责？ | Architect、Test Engineer、Code Reviewer | 责任边界 |
| **Skill** | 如何完成一个具体工程动作？ | 模块边界分析、API 设计、TDD、依赖审查 | 原子能力 |
| **Standard** | 什么结果才算符合项目约束？ | C++、Qt/QML、线程、ABI、错误处理规则 | 可验证约束 |
| **Workflow** | 在什么阶段、以什么顺序完成？ | Requirement 到 Delivery、质量门、冲突裁决 | 流程编排 |
| **Superpower** | 如何把多项能力组合成高阶方法？ | Superpowers 的规划/TDD/验证组合、重大架构评审 playbook | 组合能力包 |

## 关系

```text
Role 选择责任
  -> Workflow 决定阶段和顺序
  -> Skill 执行动作
  -> Standard 判断是否合格
  -> Superpower 在需要时提供跨阶段的组合方法
```

Superpower 可以包含 Skill、Standard、Workflow 引用和交付模板，但不能绕过本地项目事实、质量门或成熟度规则。上游仓库通常登记为 `Source`，其可用内容再映射为 Skill 或 Superpower。

## Profile 与 Integration

`Profile` 是组合配置层，不是新的能力类别。它根据项目类型选择 Standards、Skills、Superpowers、Workflows、Quality Gates 和 Outputs，例如 [profiles/qt-project.yaml](../profiles/qt-project.yaml)。

`Integration` 描述外部 Superpower 或 Harness 如何接入本地工程体系，包括固定版本、组件映射、加载顺序、能力适配和降级策略。它不复制上游内容，也不替代 Registry 的来源与成熟度记录。

```text
Superpowers -> Engineering Modules -> Profiles -> Actual Project
```

## 管理平面

- `Registry`：记录来源、版本、许可证、组件 ID、成熟度、重叠关系和组合关系。
- `Evaluation`：用真实项目证据判断 Skill 或 Superpower 是否有效，并决定晋升、降级或淘汰。
- `Governance Manager`：读取项目上下文，选择 Role、Workflow、Skill、Standard 和 Superpower，最终输出可验证产物。

因此，五类是能力模型；Registry、Evaluation 和 Manager 是让模型可维护、可审计、可演进的控制面。
