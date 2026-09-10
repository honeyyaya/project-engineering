# Evaluations

评估用于决定一个组件能否从 S1 晋升到 S2。当前只建立案例和评分标准，尚未声称有真实项目通过。

## 晋级门槛

- **S1 → S2**：至少 1 个真实项目案例；有输入、调用链、完整输出、人工评分和遗漏记录。
- **S2 → S3**：至少 3 个不同项目或变更类型；关键结论稳定，误报和漏报有解释。
- **S3 → S4**：进入默认 stack 后仍能持续通过回归案例，且没有与本地规则的未解决冲突。

## 本轮案例

- `architecture/greenfield-module-change.md`：比较新增模块的延伸、重构和替换方案。
- `cpp/qt-review.md`：用 C++/Qt 变更检查 correctness、API、architecture、tests、performance、security。
- `refactoring/behavior-preservation.md`：验证行为不变的分步重构和回归测试。

每个案例都必须补充真实项目路径、基线提交、使用的组件、原始输出、人工结论和验证证据后才能标记 `tested`。
