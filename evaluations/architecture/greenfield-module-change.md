---
id: architecture-greenfield-module-change-001
status: planned
target_components: [byliu-architecture-review, local-architecture-analysis, local-module-boundary]
---

# 架构案例：新增跨边界模块

## 输入

选择一个真实 C++/Qt 项目中需要新增基础设施、跨进程通信、同步、平台能力或桥接的需求。记录基线提交、需求文本、运行环境、线程模型和兼容性约束。

## 要求

1. 先描述当前模块、边界、依赖和负载点。
2. 独立提出 greenfield 方案，不以现有代码为前提。
3. 比较继续扩展、局部重构、替换/迁移三种方案。
4. 列出保留、重写、舍弃、迁移和回滚条件。
5. 输出 ADR，并明确哪些结论是事实、推断和建议。

## 评分

- 现状证据 0-2
- greenfield 方案 0-2
- 依赖/线程/所有权影响 0-2
- 迁移与回滚 0-2
- 是否改变了原始决策质量 0-2

`tested` 的最低要求：总分 ≥ 8，且没有遗漏关键跨模块依赖。
