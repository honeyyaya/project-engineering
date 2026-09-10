# Workflow Manager

Workflow Manager 根据任务阶段、风险和项目事实选择角色与能力，并确保每个阶段产生可验证的交付物。它负责顺序、去重、输入输出传递和冲突裁决；具体治理约束位于 `governance/` 与 `policies/`。

## 阶段链

`Requirement -> Architecture -> Design -> Plan -> Implementation -> Test -> Review -> Delivery`

新建项目按 [new-project.md](new-project.md) 从空目录建立事实与入口。每个阶段的进入/退出及重要事实变化均触发 [风险发现](risk-discovery.md)；Guardian 汇总风险，专项检查由现有角色负责。[gates.yaml](../registry/gates.yaml) 是可执行阶段产物清单，下面的 Gate 文档提供语义通过条件。

各阶段门禁：

- [Requirement Gate](requirement.md)：目标、非目标、约束、验收标准和风险。
- [Architecture Gate](architecture-gate.md)：现状证据、边界、候选方案、兼容性和 ADR 触发条件。
- [Implementation Gate](implementation-gate.md)：分步计划、文件/模块影响、回滚点和验证命令。
- [Test Gate](test-gate.md)：不变量、测试层级、结果和未覆盖区域。
- [Review Gate](review-gate.md)：审查范围、严重性排序、债务登记和交付结论。

## 路由原则

- 一般功能按完整阶段链执行，低风险任务可合并阶段但必须保留对应证据。
- 重大架构、公共 API、线程/生命周期、持久化和跨模块迁移触发 Architect、Project Structure Manager 和 ADR Manager。
- Superpowers 只作为 Workflow Manager 的候选能力；Addy 用于质量门；FluidFramework 用于审查基准；byliu 用于重大架构方案挑战。
- 发生冲突时，按 [conflict-resolution.md](conflict-resolution.md) 记录项目事实、约束优先级和最终取舍。
