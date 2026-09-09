# Project Engineering Skill

这是面向 C++/Qt/QML 项目的工程化 skill 框架，覆盖架构分析、模块边界、接口设计、实现、代码 review、架构 review 和重构。

总入口：[SKILL.md](SKILL.md)

## 目录

- `architecture/`：架构分析、模块边界、依赖和分层
- `coding/`：C++、Qt、QML、命名、错误处理和复杂度
- `design/`：接口、所有权、职责和数据流
- `review/`：代码、模块、依赖和架构 review
- `templates/`：ADR、模块说明和架构说明模板
- `skills/`：按需加载的官方增强 skill

## 更新约定

每次修改框架或新增 skill 后，在“更新记录”顶部追加一条记录，至少包含：

- 日期
- 更新内容
- 影响范围
- 验证方式和结果
- 已知风险或后续待办

记录应简洁、可追溯；重大架构变化同时更新 `templates/ADR.md` 或 `templates/ARCHITECTURE.md`。

## 更新记录

### 2026-09-09：初始化工程 skill 框架

- 建立总控路由 `SKILL.md`，支持按任务选择分析、设计、实现、审查和重构规则。
- 建立 `architecture/`、`coding/`、`design/`、`review/` 和 `templates/` 目录及基础规则。
- 加入官方增强 skill：`security-best-practices`、`security-threat-model`、`security-ownership-map`、`gh-address-comments`、`gh-fix-ci`。
- 完成所有 skill 的 frontmatter 和本地链接检查。

## 更新条目模板

复制下面的区块，放到“更新记录”最上方：

```markdown
### YYYY-MM-DD：简短标题

- 更新内容：
- 影响范围：
- 验证方式/结果：
- 已知风险或后续待办：
```
