# Addy Agent Skills 源码级审计

## 结论

- **定位**：Engineering Quality / Quality Gates 层，适合补足审查、接口、性能、安全和评估。
- **成熟度**：S1 Reviewed。仓库本身包含 `evals/`、结构校验和触发路由检查，但这些结果尚未迁移到 C++/Qt 案例。
- **建议**：作为候选 Core；优先实验 `code-review-and-quality`，再评估测试和接口设计。

## 证据

- 当前快照包含 25 个 `skills/*/SKILL.md`，并配有 `evals/cases/`、fixtures、结构校验脚本和运行说明。
- `code-review-and-quality` 将审查分为 correctness、readability、architecture、security、performance 五个轴，并强调高置信度问题。
- `using-agent-skills` 提供从需求、规划、实现、测试到审查的路由图，适合作为组合层参考。
- `evals/README.md` 将评估分为结构、触发/路由和行为三层，并要求新增 Skill 配套正向、负向和行为案例。

## 与本地工程的关系

| 上游能力 | 本地对应 | 决定 |
| --- | --- | --- |
| code-review-and-quality | `review/code-review.md` | 采用五轴检查，保留本地严重性和 C++/Qt 证据格式 |
| api-and-interface-design | `design/interface-design.md` | 作为接口设计检查的通用补充 |
| security-and-hardening | `skills/security-threat-model/` | 作为安全门候选，不覆盖本地威胁建模模板 |
| performance-optimization | `coding/complexity.md` | 采用“先测量再优化”原则 |
| evals 三层模型 | `evaluations/` | 作为 Registry 的评估结构基线 |

## 风险与限制

- 仓库的主要示例和质量规则偏 JavaScript/TypeScript/Web；它不能直接证明对 Qt 信号槽、QObject 生命周期或 C++ ABI 的判断能力。
- `security-best-practices` 本地增强 Skill 当前没有 C++/Qt 参考文件，不能把其现状误标为 C++ 安全覆盖。
- “完整路由图”与“每个 Skill 的行为质量”是两件事；需要按能力组件逐个测试。

## 下一步

先把 `code-review-and-quality` 与本地 `review/code-review.md` 做一次并行评估，记录重复 finding、漏报和误报，再决定默认顺序。
