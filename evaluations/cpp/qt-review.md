---
id: cpp-qt-review-001
status: planned
target_components: [addy.code-review-and-quality, fluidframework-review, local-code-review, local-cpp, local-qt, local-qml]
---

# C++/Qt Review 案例

## 输入

选择一个真实 C++/Qt/QML 变更，固定基线提交和变更提交。优先选择涉及 QObject 生命周期、跨线程信号槽、Model/View、公共接口或构建目标的变更。

## 要求

分别检查：

- correctness：失败路径、边界、并发和生命周期；
- API quality：接口稳定性、所有权、信号槽语义和兼容性；
- architecture：模块职责、层级和依赖方向；
- tests：回归、边界和 Qt 构建验证；
- performance：复杂度、线程阻塞和资源生命周期；
- security：输入、权限、敏感数据和外部边界。

每条 finding 必须有文件/位置、触发条件、证据、影响和修复方向；没有证据的疑虑不计入 finding。

## 对比方式

分别运行：

1. 本地 `governance/review/code-review.md`；
2. Addy `code-review-and-quality`；
3. FluidFramework review 的高置信度门；
4. 合并去重后的组合输出。

## 评分

- 高置信度问题召回 0-3
- 误报控制 0-2
- Qt/C++ 特有问题 0-2
- 严重性和证据格式 0-2
- 建议可执行性 0-1

`tested` 的最低要求：总分 ≥ 8，且没有把风格偏好报告成缺陷。
