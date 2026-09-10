# Superpowers 源码级审计

## 结论

- **定位**：Workflow / Orchestration 层，不直接替代 C++/Qt/QML 领域规则。
- **成熟度**：S1 Reviewed。结构完整、跨 Agent 适配和验证资产丰富；尚未在本项目真实案例中测试。
- **建议**：作为候选 Core，先接入流程实验，不复制内容。

## 证据

- 入口说明明确将仓库定位为完整的软件开发方法论，包含 brainstorming、计划、TDD、系统化调试、代码审查、工作树和完成前验证。
- `skills/using-superpowers/SKILL.md` 建立“先检查并调用适用 Skill”的启动规则。
- `skills/writing-plans/SKILL.md` 要求计划拆成可独立验证的小任务，并记录准确文件路径与验证步骤。
- `skills/requesting-code-review/SKILL.md` 将代码审查作为任务间的质量门。
- 仓库包含 `tests/`、`docs/testing.md`、插件清单和多个 Agent 平台适配文件，说明它维护的不只是几份 Prompt。

## 与本地工程的关系

| 上游能力 | 本地对应 | 决定 |
| --- | --- | --- |
| brainstorming / writing-plans | `architecture/`、`templates/` | 保留上游流程，输出改用本地 ADR/架构模板 |
| test-driven-development | `SKILL.md` 的实现与验证路由 | 作为测试流程候选，不覆盖 Qt 构建细节 |
| systematic-debugging | `review/` 与后续调试入口 | 作为通用调试流程候选 |
| verification-before-completion | 通用工作协议第 5、7 条 | 作为完成门，需适配 CMake/Qt 验证命令 |
| subagent-driven-development | `orchestration/` | 只在任务规模和平台能力允许时启用 |

## 风险与限制

- 强制“任何响应前先调用 Skill”的规则不应原样覆盖本地 Agent 行为；本地路由必须以用户任务和项目约束为准。
- 上游示例和测试主要围绕通用 Agent、JavaScript/脚本工具；尚未证明对 C++/Qt/QML 线程、moc、模型通知有效。
- 其完整插件分发层暂不纳入本项目运行时，只保留源码快照和可复用的流程思想。

## 下一步

使用 `evaluations/architecture/` 和 `evaluations/refactoring/` 的案例，在一个真实 Qt 变更上测试 planning → implementation → verification → review 链路。
