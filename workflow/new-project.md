# New Project

入口为自然语言新建项目任务，或先用 engineering_guard.py init 建立风险记录；后者不等于项目脚手架生成器。

## Bootstrap 与需求

- Explorer 检查目标目录、已有内容、平台/架构、编译器、Qt/CMake 和测试工具。初始化记录不会覆盖既有 run.yaml；业务文件也按真实任务范围创建。
- 记录项目名/路径、目标、非目标、首个可观察行为、约束与验收标准。只有会改变方案而无法推断的缺失信息才询问用户。
- 空项目的 build-entry、test-entry、module-map 标为 planned；实际入口在实现阶段补齐并运行。不要求用户先提供不存在的文件，不把 planned 当构建通过。

## 沿八阶段执行

Requirement 明确验收；Architecture 确定职责、目标依赖和关键决策；Design 明确接口、所有权、线程与错误语义；Plan 拆分最小可验证步骤与测试；Implementation 创建可构建骨架并实现首条功能链；Test 执行正常、边界和失败验证；Review 复核缺陷、未覆盖区域和证据；Delivery 提供运行说明、结果及剩余风险。

每个阶段都插入 [风险发现](risk-discovery.md)，按 [gates.yaml](../registry/gates.yaml) 留存证据。目标目录不强制固定分层；由项目规模和依赖方向选择。简单项目允许在同一文档完成多个阶段的记录。

发布只在明确包含 release 的任务范围内启用，额外选择 release 特征，核对适用的恢复/回滚、性能和安全证据。创建项目或通过 Delivery Gate 不意味着已经授权发布。

## 最小验收

有目标项目自己的运行记录、实际构建与测试命令、关键行为测试和审查结论。缺少工具时可交付明确标记的未验证骨架，但不能宣称可运行、风险已解除或整个 Workflow 已通过。
