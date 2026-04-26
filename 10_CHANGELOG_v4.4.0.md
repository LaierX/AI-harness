# 10. Changelog v4.4.0「变更记录」

## 版本定位
- 本版本为 v4.3.0 后的 minor release「小版本」。
- 目标是提供 Harness v4 的最小本地可执行路径。
- 不新增 workflow_state「流程状态」。
- 不改变 Schema / Record / Context / Tool / Runtime 的职责边界。

## 新增
- `13_MINIMAL_RUNNER_MODULE.md`：定义 Minimal Runner 的定位、命令接口、支持的 schema 子集、artifact 写入与 readback 边界。
- `runner/harness_runner.py`：零依赖 Python 最小 runner。
- `examples/execution_plan.valid.json`：Execution Plan 校验示例。
- `examples/step_snapshot.valid.json`：Step Snapshot 校验示例。

## 更新
- `.gitignore`：忽略本地运行产物 `artifacts/`。
- `README.md` 与 `00_INDEX.md`：版本推进到 `v4.4.0`，新增 runner 入口。
- `00_ENTRYPOINT_SINGLE_FILE.md`：同步参考总版中的 Minimal Runner 边界。

## 设计原则
- Minimal Runner 只跑通 `load schema -> validate object -> write artifact -> readback artifact`。
- runner 校验通过不等于 Record Gate 通过。
- runner readback 通过只证明 artifact 可定位、可解析。
- 当前 runner 只实现本仓库 schema 已使用的 JSON Schema 子集，不声明为通用 JSON Schema 引擎。
