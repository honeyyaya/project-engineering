# Roles

Project Engineering Manager 由多个职责组成。角色是治理视角，不等于必须创建多个 Agent；一次任务可以由一个 Agent 按角色顺序完成，也可以在工具允许时委派专项检查。

| 角色 | 负责的问题 | 主要输入 | 主要产出 |
| --- | --- | --- | --- |
| Architect | 结构是否适合当前和未来需求？ | 需求、代码、构建、运行配置 | 架构分析、方案、ADR |
| Engineering Standards | 实现是否符合项目技术约束？ | `policies/`、项目配置 | 适用策略和偏差说明 |
| Project Structure Manager | 文件、模块和依赖放置是否合理？ | 目录、目标、依赖图 | 结构约束、迁移影响 |
| Workflow Manager | 当前阶段应该调用哪些能力？ | 任务类型、风险、Stack | 路由、门禁、下一步 |
| Test Engineer | 如何证明行为正确且可回归？ | 需求、不变量、变更 | 测试计划、结果和缺口 |
| Code Reviewer | 变更是否有高置信度问题？ | diff、上下文、策略 | 严重性排序 findings |
| Technical Debt Manager | 哪些债务影响当前决策？ | TODO、重复、复杂度、历史 | 债务条目、优先级、触发条件 |
| ADR Manager | 为什么采用这个决策？ | 候选方案、约束、证据 | ADR、迁移和回滚条件 |

角色输出必须回到 `evaluations/` 的案例或真实项目记录中，不能只生成状态标签。
