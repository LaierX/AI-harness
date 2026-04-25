# 10. Changelog v4.1.1「变更记录」

## 版本定位
- 本版本为 v4.1.0 的 patch release「补丁版本」。
- 目标是收紧字段口径、装配边界、模板门槛与治理反审入口。
- 不新增 workflow_state「流程状态」。

## 更新
- `README.md`：当前版本推进到 `v4.1.1`，补充版本说明。
- `00_INDEX.md`：当前版本推进到 `v4.1.1`，目录清单新增本变更记录。
- `02_EXECUTION_PROFILE_CONTROLLER.md`：明确 Regression Asset 与 Regression Executor 的条件装配边界。
- `03_RECORD_AND_EVIDENCE_MODULE.md`：补齐 Step Snapshot 的 `evidence_pointer` 与 `readback_status` 字段。
- `04_RUN_ENGINE_ENTRY.md`：补充 `module_mode` 推荐用法说明。
- `04G_DEVELOPMENT_MODULE.md`：补充 recommended module_mode「推荐模块调用模式」。
- `04H_INSTALLATION_MODULE.md`：补充 recommended module_mode「推荐模块调用模式」。
- `04I_DEPLOYMENT_MODULE.md`：补充 recommended module_mode「推荐模块调用模式」。
- `04J_DEBUG_MODULE.md`：补充 recommended module_mode「推荐模块调用模式」。
- `06_REGRESSION_ASSET_MODULE.md`：补充 regression rule status「规则状态」枚举。
- `07_REGRESSION_EXECUTOR_MODULE.md`：明确执行器只读取 `status = active` 的 rule。
- `08_GOVERNANCE_MODULE.md`：补充 Governance Review Checklist 使用要求。
- `09_TEMPLATES.md`：统一 `rule_required` 字段，补齐 Record Gate 相关模板字段，新增治理反审清单模板。
- `00_ENTRYPOINT_SINGLE_FILE.md`：同步参考总版中的字段口径，避免与模块版漂移。

## 字段收口
- Closing 输出统一使用 `rule_required`，不再使用 `rule_generated` / `regression_needed`。
- Execution Plan 统一使用 `execution_profile`，不再使用 `profile` 表示执行档位。
- Step Snapshot 与 Capability Module Snapshot 必须显式记录 `evidence_pointer` 与 `readback_status`。

## 装配边界
- 当 Closing Module 判定 `rule_required = true` 时，`06_REGRESSION_ASSET_MODULE.md` 为条件必装模块。
- `07_REGRESSION_EXECUTOR_MODULE.md` 仅在需要执行 active rule「激活规则」或周期性回归任务时装配。

## 设计原则
- 本版本只做规范收口，不改变 v4 主流程。
- capability modules 仍不构成新的 workflow_state。
- Record Gate 仍是所有 step 与 capability module 的统一退出门。
