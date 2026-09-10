# Workflow Manager

Workflow Manager 根据任务阶段、影响面和风险选择最小的能力组合，管理输入输出和门禁。

默认阶段：

```text
Requirement -> Architecture -> Design -> Plan -> Implementation -> Test -> Review -> Delivery
```

阶段可以按任务裁剪。只有任务确实需要时才启用完整架构审查、专项安全检查或多 Agent 委派；上游 Skill 是可替换组件，不能反过来决定总体系。

输出：当前阶段、选择的组件、进入下一阶段的门禁、未解决问题和验证证据。
