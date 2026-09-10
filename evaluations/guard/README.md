# Engineering Guard 首次实验

日期：2026-09-10。基线：88c9127。状态：本地最小闭环实验，不作为上游 Skill 的 S2 晋级结果。

## 已验证

- 门禁引擎 16 项测试通过：缺证据、前置阶段遗漏、内容散列变化、版本过期、非法特征、S1 默认启用、风险接受等场景。
- [QtCore 小项目](qt-queue/README.md) 实际配置与编译成功，5 项行为测试通过。
- 同一过载测试检出预设缺陷：10,000 条输入、0 条消费，无界实现保留 10,000 条并失败；有界实现保留最新 4 条并通过。

问题发现矩阵保存在 [.engineering/run.yaml](qt-queue/.engineering/run.yaml) 的 checks 与 issues：包含阶段、角色、组件、规则、措施和证据。上游组件为空，避免把 Registry 候选冒充实际调用。

## 门禁状态回放

- [初始检查](qt-queue/.engineering/evidence/initial-gate.json)：新记录没有产物或风险证据，必须阻断。
- [未关闭风险的记录](qt-queue/.engineering/run.blocked.yaml) 与 [检查结果](qt-queue/.engineering/evidence/risk-blocked-gate.json)：保留失败的过载检查及 open/high 问题，不能交付。
- [修复后检查](qt-queue/.engineering/evidence/final-gate.json)：补齐实际实现、测试及复核证据，问题记为 verified，再检查八阶段。

这组状态是已知缺陷实验的记录回放；各阶段材料在实验中补全，不能视为真实业务项目按时间顺序完成了全部角色交接。

## 尚未证明

检查器不会自行执行 C++ 分析、性能测试或持续监控，也无法判断报告内容是否真实。此例未验证视频延迟、内存峰值、并发安全、WebRTC、Android 或商业发布。

未做“启用/不启用某 Skill”的对照，未取得人工评分。下一次评估应选择一个实际项目的小变更，事前记录基线与风险、显式选择上游组件，按真实阶段保存发现与复核，评估漏报、误报、角色重复和使用成本。原有真实业务评估案例仍待执行。
