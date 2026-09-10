# Skill Registry

Registry 是上游 Skill 的目录和决策入口。它记录来源、版本、能力、成熟度、重复关系和组合方式；原始内容始终保存在 `sources/`，不在这里改写上游 Skill。`skills.yaml` 是 Skill 级主索引，`compatibility.yaml` 是跨来源采用和冲突矩阵。

Engineering Governance Manager 通过 Registry 选择角色所需的能力。来源登记回答“能力来自哪里”，Skill Registry 回答“如何采用和组合”，`stack/` 回答“默认如何编排”，`profiles/` 回答“项目类型激活什么”，`integrations/` 回答“外部底座如何接入”，`workflow/` 回答“何时调用”，`governance/` 和 `policies/` 回答“项目必须满足什么”。

## 成熟度

```text
S0 Candidate  已发现，尚未人工审计
S1 Reviewed   已核对仓库结构、触发方式、许可证和内容
S2 Tested     已在至少一个真实案例中运行并人工评价
S3 Proven     在多个真实案例中稳定有效
S4 Core       进入 Project Engineering 默认主流程
```

当前四个来源均为 `S1 Reviewed`。任何来源在晋升到 S2 前，必须有 `evaluations/` 中的输入、输出和人工结论。

## 文件

- `sources.yaml`：来源级登记和固定提交
- `skills.yaml`：Skill 级主索引、采用策略、激活条件和组合关系
- `compatibility.yaml`：Superpowers 与 Addy 的兼容矩阵和重复能力裁决
- `capabilities.yaml`：能力矩阵、证据路径和重叠关系
- `architecture.yaml`、`coding.yaml`、`review.yaml`、`testing.yaml`、`refactoring.yaml`、`security.yaml`：按能力域登记可组合组件；组件 ID 供 Stack 和 Workflow 引用

## 更新规则

1. 先增加或更新 `sources/github/<id>/ORIGINAL` 和 `manifest.json`。
2. 再更新来源 `metadata.yaml`、`audit.md` 和本目录的能力记录。
3. 真实案例通过后才提高成熟度；不要用 Star、发布时间或个人偏好替代行为证据。
