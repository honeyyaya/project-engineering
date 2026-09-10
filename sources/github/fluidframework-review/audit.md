# FluidFramework Review 源码级审计

## 结论

- **定位**：真实大型项目中的 Code Review benchmark，不作为通用工程总控。
- **成熟度**：S1 Reviewed。审查流程和 API 规范已核对；尚未在本地 C++/Qt diff 上运行。
- **建议**：保留为参考层，用来校准审查深度、证据门和 API review 问题。

## 证据

- `.claude/skills/review/SKILL.md` 覆盖 correctness、API quality、architecture、tests、performance、security。
- Standard/Deep 模式将 Correctness 分给 Breaker、API Quality 分给 API Analyst，其余由 Inspector 审查，并要求去重和高置信度门。
- 审查规则明确要求识别比较基线、统计变更范围、读取完整上下文，并对不确定问题保持沉默。
- `api-conventions.md` 将 API 设计落到命名、类型、错误、事件、文档和用户可用性。

## 与本地工程的关系

| 上游能力 | 本地对应 | 决定 |
| --- | --- | --- |
| 高置信度审查门 | `review/code-review.md` | 采用“证据优先、偏好不算缺陷”原则 |
| API Analyst | `design/interface-design.md` | 加强公共接口和兼容性检查 |
| Breaker | `review/code-review.md` | 将边界、失败路径和并发列为重点 |
| Inspector | `review/architecture-review.md`、`coding/complexity.md` | 由本地规则负责 Qt/C++ 特有检查 |

## 风险与限制

- 其 API 规范以 TypeScript/Fluid Framework 为背景，不能直接当成 C++ API 规范。
- 快照只保留 review Skill 及相关许可证/说明，未复制整个 FluidFramework，避免把大型产品仓库误当作 Skill 包。
- 上游要求的 Breaker/API Analyst 多代理流程依赖特定 Agent 工具；本地组合层只能在工具可用时采用。

## 下一步

将其高置信度门、审查分工和五类问题纳入 `evaluations/cpp/qt-review.md` 的评分标准。
