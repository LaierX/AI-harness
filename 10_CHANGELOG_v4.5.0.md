# 10. Changelog v4.5.0「变更记录」

## 版本定位
- 本版本为 v4.4.0 后的 minor release「小版本」。
- 目标是提供 Regression Executor MVP「回归执行器最小可行版本」。
- 不新增 workflow_state「流程状态」。
- 不引入高风险自动修复或外部工具执行。

## 新增
- `runner/harness_runner.py`：新增 `run-regression` 命令，读取 active regression rule 并执行安全的 `schema_validation` worker。
- `examples/regression_rule.schema_validation.active.json`：新增 active regression rule 示例。
- `schemas/regression_executor_result.schema.json`：新增回归执行结果 schema。

## 更新
- `07_REGRESSION_EXECUTOR_MODULE.md`：补充 v4.5 MVP 执行边界、命令接口、当前支持的 worker 与结果结构。
- `12_SCHEMAS_MODULE.md`：新增 `regression_executor_result` schema 清单。
- `13_MINIMAL_RUNNER_MODULE.md`：补充 `run-regression` 命令说明。
- `README.md` 与 `00_INDEX.md`：版本推进到 `v4.5.0`，新增 Regression Executor MVP 入口。
- `00_ENTRYPOINT_SINGLE_FILE.md`：同步参考总版中的 v4.5 执行器边界。

## 设计原则
- Regression Executor MVP 只执行 `status = active` 的 rule。
- 当前 worker 仅支持 `executor_type = schema_validation`。
- 执行结果必须写入 artifact，并产出 `evidence_pointer`。
- `fail` / `error` 不触发自动修复，只返回 `next_action`。
- 执行器运行成功不等于主流程闭环成功。
