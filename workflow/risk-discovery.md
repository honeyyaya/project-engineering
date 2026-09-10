# 跨阶段风险发现

这是一项横切职责，沿现有八阶段流程运行，不增加第六类能力，也不取代 Superpowers 的开发方法。

## 运行方式

1. Explorer 读取项目事实；Workflow Manager 选择 Profile、任务类型和当前阶段。
2. Guardian 从 [risks.yaml](../registry/risks.yaml) 按阶段与实际项目特征选择规则，再把具体分析交给 owner。默认特征来自 Profile；队列、并发、外部输入、持久化等由事实补充，不凭项目名称猜测。
3. 每项检查记录 passed、failed、unverified 或 not-applicable。不适用也必须有原因和适用性证据。工具缺失记录 unverified、原因及替代验证计划，不能自动改成 not-applicable。
4. 真实问题另存 issues：包含规则 ID、触发条件、位置、发现阶段/角色/组件、影响、owner、严重性、缓解计划与验证。假设要明确标记，不虚构已发生的缺陷。
5. 用 [gates.yaml](../registry/gates.yaml) 检查产物与风险证据。高风险问题未处理时阻断；交付时剩余问题必须验证关闭，或为中低风险且有明确接受者与理由。接受风险的字段是审计记录，不是操作授权。

检查点：每个阶段边界、新增依赖/线程/接口、需求改变、测试失败，以及准备交付时。不是常驻后台监控；本版需 Agent 在这些点显式调用。

特征名必须来自 risks.yaml 的 features 列表，拼写错误会拒绝运行。新增特征应先登记并说明检查规则；漏识别真实特征仍需要 Explorer/Reviewer 发现，脚本无法仅凭标签判断业务事实。

## 命令与能力边界

从管理器根目录安装依赖后运行：

```powershell
python -m pip install -r requirements.txt
python scripts/engineering_guard.py validate
python scripts/engineering_guard.py init --project D:/Projects/MyProject --profile qt-project --features queue concurrency
python scripts/engineering_guard.py check --project D:/Projects/MyProject --stage architecture
```

`init` 仅创建目标项目的 `.engineering/run.yaml`，不会生成产品代码，也不会覆盖已有记录。无证据的新记录必须返回 blocked。`check` 只读，检查请求阶段及该 Workflow 的所有前置阶段；返回码 0 为通过、1 为阻断、2 为输入/配置错误。不会自行推进 current_stage。

本版脚本检查证据存在、非空、SHA-256 未变化、revision 一致及结果结构；它不是 C++ 静态分析器，不会自行运行构建、理解报告真伪或发现任意代码缺陷。Agent/Reviewer 负责检查语义、执行命令和确定项目特征。变更影响既有判断时更新 revision，重新审查受影响内容，明确复用哪些仍有效证据。

## 记录契约

记录保存在目标项目，格式见 [运行记录模板](../templates/GUARD_RUN.yaml)。证据路径相对目标项目根目录，必须留在该目录内；每项 evidence 包含 path 与文件内容的 sha256。计算散列可用 `Get-FileHash -Algorithm SHA256` 或 Python hashlib；记录十六进制小写结果。产物 ID 对应 gates.yaml；检查以 stage + risk_id 唯一标识。

同一文件可承载多个产物，但 Reviewer 必须核对对应章节，而不能只靠文件存在判定完成。phase 的 passed 只表示该阶段的检查完成：设计阶段可评估拟定契约，test 阶段必须有实际运行证据。

散列按文件原始字节计算。目标项目需为证据与被引用源码确定稳定的换行/编码策略，避免 Git checkout 自动转换内容。本仓库的 Qt 示例使用 `.gitattributes` 禁止该目录的自动换行转换；文件经编辑后仍需重新审查并更新散列。

selected_components 使用 Registry 真实 ID；S1 只能 reference 或 evaluation，只有 S4 可 default。若只是使用本地规则，components 为空，不把上游名称当作已经调用的证明。各来源现有成熟度不因脚本或合成案例通过自动晋升。

风险状态：open → mitigated → verified；误报用 dismissed 并附证据；中低风险可 accepted 并记录 accepted_by、理由、剩余影响与复查条件。单条 check 的 passed 不能抵消未处理的高风险 issue。

## 评估

每次真实运行保留“阶段—发现者—组件—规则—证据—措施—复核结果”。要声称“没有某 Skill 就会漏掉”，必须做有/无该组件的对照评估；单次发现只能证明发现过问题。本仓库 evaluations 保存脱敏案例和结论，目标项目保留原始日志与风险状态。
