# 10. Changelog v4.3.0「变更记录」

## 版本定位
- 本版本为 v4.2.1 后的 minor release「小版本」。
- 目标是把核心 Markdown 模板沉淀为机器可校验 JSON Schema。
- 不新增 workflow_state「流程状态」。
- 不改变 Context / Tool / Memory / Runtime 的职责边界。

## 新增
- `12_SCHEMAS_MODULE.md`：定义 schema 模块定位、权威边界、校验规则、版本规则与治理反审要求。
- `schemas/common.schema.json`：定义共享枚举与公共结构。
- `schemas/execution_plan.schema.json`
- `schemas/step_snapshot.schema.json`
- `schemas/capability_module_snapshot.schema.json`
- `schemas/closing_summary.schema.json`
- `schemas/context_assembly_snapshot.schema.json`
- `schemas/tool_contract.schema.json`
- `schemas/tool_call_snapshot.schema.json`
- `schemas/memory_entry.schema.json`
- `schemas/evidence_pointer.schema.json`
- `schemas/runtime_adapter_capability.schema.json`
- `schemas/runtime_adapter_snapshot.schema.json`
- `schemas/regression_rule.schema.json`
- `schemas/governance_review_checklist.schema.json`

## 更新
- `README.md` 与 `00_INDEX.md`：版本推进到 `v4.3.0`，新增 Schemas Module 与 schema 目录入口。
- `09_TEMPLATES.md`：清理重复 Runtime Adapter Snapshot 模板，并补充 schema 对照说明。
- `08_GOVERNANCE_MODULE.md`：补充 schema drift 与 required 字段反审项。
- `00_ENTRYPOINT_SINGLE_FILE.md`：同步参考总版中的 schema 模块边界与强制规则。

## 设计原则
- Markdown 模板服务于人类填写与审阅。
- JSON Schema 服务于 runner / executor / governance 的机器校验。
- Schema 校验通过不等于 Record Gate 通过。
- L3 强结构对象必须通过 schema 校验后才能进入完整闭环资产。
