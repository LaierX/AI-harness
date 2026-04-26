# 12. Schemas Module「结构校验模块」

> 作用：为 Harness v4 的核心记录、工具、记忆、运行适配与回归资产提供机器可校验的 JSON Schema。
> 原则：Markdown 模板服务于阅读与填写；JSON Schema 服务于自动校验、运行器接入与治理反审。

---

## 一、定位

Schemas Module 是结构校验资产模块，不构成新的 workflow_state「流程状态」。

它负责：
- 定义核心对象的机器可校验字段结构
- 固定枚举口径
- 约束必填字段
- 为 runner / executor / governance review 提供校验依据
- 发现模板与 schema 字段漂移时触发治理反审

它不负责：
- 推进 workflow_state
- 替代 Record Gate
- 替代 Context Gate
- 替代数据库 DDL
- 替代业务判断

---

## 二、权威边界

### 2.1 人类填写口径

`09_TEMPLATES.md` 是人类可读模板入口。

适用场景：
- 手动创建记录
- 人类审阅
- 规范讲解
- 低自动化场景

### 2.2 机器校验口径

`schemas/*.schema.json` 是机器校验入口。

适用场景：
- runner 输入校验
- tool call snapshot 校验
- memory entry 写入前校验
- runtime adapter pointer 校验
- regression rule asset 校验
- governance review 自动反审

### 2.3 漂移处理

当 Markdown 模板与 JSON Schema 字段不一致：
- 不得静默选择其中一方
- 必须记录 schema_drift「结构漂移」
- 必须由 Governance Module 判定修正方向
- 修正前不得把该对象作为强结构记录写入 L3 闭环资产

---

## 三、Schema 文件清单

### 3.1 公共定义

- `schemas/common.schema.json`

### 3.2 Run / Record

- `schemas/execution_plan.schema.json`
- `schemas/step_snapshot.schema.json`
- `schemas/capability_module_snapshot.schema.json`
- `schemas/closing_summary.schema.json`

### 3.3 Context / Tool

- `schemas/context_assembly_snapshot.schema.json`
- `schemas/tool_contract.schema.json`
- `schemas/tool_call_snapshot.schema.json`

### 3.4 Memory / Runtime

- `schemas/memory_entry.schema.json`
- `schemas/evidence_pointer.schema.json`
- `schemas/runtime_adapter_capability.schema.json`
- `schemas/runtime_adapter_snapshot.schema.json`

### 3.5 Regression / Governance

- `schemas/regression_rule.schema.json`
- `schemas/governance_review_checklist.schema.json`

---

## 四、校验规则

### 4.1 L1

L1 可使用 Markdown 模板或 JSON Schema。

若使用 JSON Schema：
- 至少校验 `execution_plan` 或当前 standalone module 对应 snapshot
- 校验失败不得宣称结构化记录完成

### 4.2 L2

L2 建议使用 JSON Schema 校验：
- Execution Plan
- Step Snapshot
- Tool Call Snapshot，如调用工具
- Evidence Pointer，如生成证据指针
- Closing Summary，如进入简化闭环

### 4.3 L3

L3 必须使用 JSON Schema 校验：
- Execution Plan
- 每个 Step Snapshot
- 每个 Capability Module Snapshot，如适用
- Context Assembly Snapshot，如发生上下文装配
- Tool Contract 与 Tool Call Snapshot，如发生工具调用
- Evidence Pointer 与 Runtime Adapter Snapshot，如使用适配器
- Closing Summary
- Regression Rule，如 `rule_required = true`
- Memory Entry，如写入长期 memory

任一必校对象未通过 schema 校验时：
- 不得宣称 L3 完整闭环
- 必须写入 Record & Evidence Module
- 必须给出 next_or_rollback

---

## 五、Schema 版本规则

每个对象可以包含 `schema_version` 字段。

建议：
- v4.3.0 初始 schema 使用 `schema_version = "v4.3.0"`
- patch release 只修正约束时，可保持对象语义版本不变
- 若字段含义或必填性改变，应推进 schema version

---

## 六、命名规则

- Schema 文件名使用 snake_case。
- JSON 字段名使用 snake_case。
- 公共 `$defs` 可以使用 camelCase，但业务字段不得混用。
- 业务主标识仍统一使用 `run_uid / issue_uid / rule_uid / source_issue_uid`。
- 不得新增 `run_id` / `rule_id` 作为业务主标识。

---

## 七、治理反审

Governance Module 应定期检查：
- Markdown 模板与 JSON Schema 是否字段漂移
- JSON Schema 中枚举是否与 Kernel Module 口径一致
- required 字段是否低于对应模块的最小输出要求
- schema 是否引用了不存在的 `$defs`
- L3 闭环资产是否存在未校验结构

---

## 八、禁止事项

- 不得用 JSON Schema 替代业务判断
- 不得用 schema 校验通过冒充 Record Gate 通过
- 不得让 schema 字段漂移长期滞留
- 不得在 L3 中写入未通过 schema 校验的强结构对象
- 不得把数据库内部主键 `id` 当作业务主标识写入 schema
