# Architecture Review 源码级审计

## 结论

- **定位**：Architecture Review Reference，专门在重大需求前挑战现有技术栈和沉没成本。
- **成熟度**：S1 Reviewed。思想和阶段流程清晰，但仓库规模小、没有真实项目验证数据。
- **建议**：保留为参考组件，不直接进入默认实现流程；在新增平台、同步、桥接或 sidecar 时触发。

## 证据

- 六阶段流程依次要求理解真实使用、绘制现状架构、提出 greenfield 方案、计算迁移成本、比较 bolt-on/pivot/hybrid、记录决策。
- 明确识别 bridge-to-a-bridge、three-process stack、sunk-cost architecture 和 bolting-on。
- 使用“如果今天从零开始并知道全部需求，我还会选当前架构吗？”作为强制问题。
- 要求输出保留、重写、舍弃和迁移路径，适合补充本地 ADR。

## 与本地工程的关系

| 上游能力 | 本地对应 | 决定 |
| --- | --- | --- |
| Greenfield question | `architecture/architecture-review.md` | 作为重大架构变更的前置检查 |
| Bridge/sidecar smells | `architecture/dependency-rules.md` | 作为风险提示，不自动判定必须重写 |
| Pivot cost | `templates/ADR.md` | 在 ADR 中记录保留、重写和回滚 |
| Six phases | `orchestration/workflow.md` | 只对高影响架构任务启用 |

## 风险与限制

- 阶段 1 要求询问大量使用场景；在需求已明确的任务中应按需裁剪，避免流程形式化。
- “超过 50% 可保留即适合 pivot”等阈值是启发式，不应作为自动决策规则。
- 该 Skill 不包含 C++/Qt 具体知识，必须与本地模块、线程、所有权和构建规则组合。

## 下一步

在第一个真实重构项目中，选择一个确实涉及跨进程或模块桥接的变更，检验 greenfield/pivot 分析是否改变最终方案。
