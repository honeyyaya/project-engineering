---
name: project-engineering
description: 面向 C++/Qt/QML 项目的工程化总控 skill，按需求路由架构分析、模块边界、接口设计、实现、代码审查、架构审查和重构工作。
metadata:
  short-description: C++/Qt/QML project engineering workflow
---

# Project Engineering

这是工程任务的总入口。先判断用户要解决的工程问题，再只加载与当前问题相关的规则；不要把所有文档都当作一次任务的强制流程。

## 工作模式路由

根据请求选择一个或多个模式。若任务跨模式，按“分析 → 设计 → 实现 → 验证/审查”的依赖顺序处理：

| 用户意图 | 必读规则 | 主要产出 |
| --- | --- | --- |
| Architecture Analysis | [architecture-review.md](architecture/architecture-review.md)、[architecture-decision.md](architecture/architecture-decision.md) | 现状、约束、风险、候选方案和决策 |
| Module Boundary | [module-boundary.md](architecture/module-boundary.md)、[dependency-rules.md](architecture/dependency-rules.md)、[layering.md](architecture/layering.md) | 模块职责、依赖方向、边界及迁移影响 |
| Interface Design | [interface-design.md](design/interface-design.md)、[ownership.md](design/ownership.md)、[responsibility.md](design/responsibility.md)、[data-flow.md](design/data-flow.md) | API/信号槽/数据流契约、所有权和错误语义 |
| Implementation | 语言/框架相关的 [coding](coding/) 规则及对应设计规则 | 可维护实现、测试、构建与变更说明 |
| Code Review | [code-review.md](review/code-review.md)、[dependency-review.md](review/dependency-review.md)、必要时读取安全增强 skill | 按严重性排序的可复现问题、修复建议和未覆盖风险 |
| Architecture Review | [architecture-review.md](review/architecture-review.md) 及 architecture 规则 | 设计一致性、演进风险、架构决策建议 |
| Refactoring | [module-review.md](review/module-review.md)、[complexity.md](coding/complexity.md)、相关边界/所有权规则 | 保持行为不变的分步重构、风险控制和验证结果 |

## 通用工作协议

1. 明确目标、非目标、兼容性要求、构建环境和验收标准；信息不足时做最小假设并显式标注。
2. 先阅读现有代码和配置，再提出改动。以事实（调用关系、依赖、测试、构建输出）支持判断。
3. 将“必须修复的问题”和“可选改进”分开。不要为了形式上的整洁扩大变更范围。
4. 设计或实现时保留清晰的所有权、生命周期、线程/事件循环和错误传播语义；跨层依赖必须符合层级方向。
5. 实现后运行与风险匹配的格式检查、静态检查、单元/集成测试和构建；无法运行时说明原因及替代验证。
6. 审查输出按 `阻断 / 高 / 中 / 低` 排序；每个问题包含位置、触发条件、影响、证据和修复方向。没有发现问题时也说明检查范围和剩余不确定性。
7. 交付时总结变更文件、关键决策、验证命令/结果、已知风险和后续建议；必要时使用 [ADR](templates/ADR.md)、[MODULE](templates/MODULE.md) 或 [ARCHITECTURE](templates/ARCHITECTURE.md) 模板。

## 语言与框架规则

- C++：读取 [cpp.md](coding/cpp.md)、[naming.md](coding/naming.md)、[error-handling.md](coding/error-handling.md)；关注 RAII、const、异常/错误码约定和 ABI 兼容性。
- Qt/QML：涉及 Qt 时读取 [qt.md](coding/qt.md)；涉及 QML 时读取 [qml.md](coding/qml.md)。特别检查 QObject 生命周期、线程亲和性、信号槽契约、QML/C++ 边界和模型通知。
- 复杂度：当变更扩大控制流、状态或依赖图时读取 [complexity.md](coding/complexity.md)，优先降低认知负担而非仅追求代码行数。

## 可选增强 skill

仓库内 `skills/` 放置可按需加载的官方增强 skill：

- [security-best-practices](skills/security-best-practices/SKILL.md)：实现或审查涉及输入、身份、网络、存储、敏感数据时使用，并只读取匹配语言/框架的 reference。
- [security-threat-model](skills/security-threat-model/SKILL.md)：架构分析或高风险接口设计需要系统化威胁建模时使用。
- [security-ownership-map](skills/security-ownership-map/SKILL.md)：安全审查需要根据代码归属、维护者和敏感组件建立责任映射时使用。
- [gh-address-comments](skills/gh-address-comments/SKILL.md)：用户明确要求处理 GitHub PR review comments 时使用。
- [gh-fix-ci](skills/gh-fix-ci/SKILL.md)：用户要求诊断或修复 GitHub Actions/CI 失败时使用。

这些增强 skill 不会自动替代本地工程规则；若规则冲突，以用户约束和仓库现状为准，并记录取舍。

## 何时停止或请求确认

发现会破坏公开 API、数据格式、线程模型、持久化兼容性或大范围迁移时，先给出影响和可逆方案；只有在用户目标已明确覆盖该变更时才实施。对不在当前任务范围的清理、升级依赖或发布操作不主动执行。
