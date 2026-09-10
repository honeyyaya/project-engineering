# Routing

Workflow Manager 先确定任务阶段和风险，再激活角色。表中的组件是候选能力，最终选择受 `stack/project-engineering.yaml` 的成熟度和项目事实约束。

| 任务信号 | 首选组件 | 必须组合 | 主要产出 |
| --- | --- | --- | --- |
| 新功能、需求不清 | Workflow Manager + Architect | `superpowers.brainstorming` / `superpowers.writing-plans`；本地架构和设计规则 | 需求、方案、实施计划 |
| 新平台、同步、桥接、sidecar | Architect + Project Structure Manager + ADR Manager | `byliu-architecture-review`；本地架构规则 | 继续扩展/迁移/替换决策 |
| C++/Qt/QML 实现 | Engineering Standards + Test Engineer | 本地 `policies/`；`superpowers.test-driven-development` / `superpowers.verification-before-completion` | 实现、测试和构建证据 |
| 公共 API 或跨模块接口 | Architect + Engineering Standards | `addy.api-and-interface-design`；本地 ownership/responsibility | 接口契约、兼容性说明 |
| 代码审查 | Code Reviewer + Technical Debt Manager | `addy.code-review-and-quality`；本地 review + Fluid benchmark | 严重性排序 finding、债务条目 |
| 行为不变重构 | Architect + Test Engineer + Code Reviewer | `addy.code-simplification`；`superpowers.test-driven-development` / `superpowers.verification-before-completion` + 本地 module-review | 分步重构与回归证据 |

## 路由限制

- 同一能力域只选择一个默认流程；重叠组件作为检查表或 benchmark，不并行生成互相竞争的计划。
- 任何上游结论涉及 C++/Qt 特有语义时，必须由本地规则和代码证据确认。
- 未通过 S2 评估的组件不能成为默认路由，只能作为 reference 或候选。
