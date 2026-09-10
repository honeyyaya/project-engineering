---
id: refactoring-behavior-preservation-001
status: planned
target_components: [superpowers.test-driven-development, addy.code-simplification, superpowers.verification-before-completion, local-refactoring-routing]
---

# 重构案例：保持行为不变

## 输入

选择一个已有测试的 C++/Qt 模块，要求降低复杂度、切开模块 seam 或改善所有权，但不改变公开行为。固定基线构建和测试结果。

## 要求

1. 先记录行为基线、调用者、依赖和风险。
2. 先补足能表达关键不变量的测试，再做最小分步改动。
3. 每一步都运行匹配风险的构建和测试。
4. 完成后给出 blast radius、剩余风险和回滚点。

## 评分

- 行为基线完整性 0-2
- 测试先行和回归覆盖 0-2
- 每步变更可回滚 0-2
- 复杂度/边界是否实际改善 0-2
- 验证证据 0-2

`tested` 的最低要求：总分 ≥ 8，且基线与最终测试均通过。
