# Qt

- QObject 的 parent、智能指针和跨线程移动策略必须唯一且清晰，禁止悬空 signal/slot receiver。
- 检查线程亲和性、事件循环、queued/direct connection 选择及 GUI 线程限制。
- 信号表示已发生的事实，槽/命令表示请求；参数尽量使用稳定值类型并记录线程语义。
- Model/View 变更必须正确发出 begin/end 与 dataChanged 等通知；不要在 model 外部修改内部容器。
- Qt 元对象、moc、资源和构建配置的变更要纳入构建验证。
