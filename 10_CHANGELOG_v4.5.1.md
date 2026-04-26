# 10. Changelog v4.5.1「变更记录」

## 版本定位
- 本版本为 v4.5.0 后的 patch release「补丁版本」。
- 目标是补强可靠性门控、回退路由、issue 复用与 schema example 覆盖。
- 不新增 workflow_state「流程状态」。
- 不改变 Regression Executor MVP 的执行边界。

## 新增
- `04X_ROLLBACK_ROUTER_MODULE.md`：新增全局 rollback router，提供所有 step failure 的唯一回退表、输入、输出与退出条件。
- `examples/*.valid.json`：为每个非公共 schema 增加最小 valid example。

## 更新
- `04_RUN_ENGINE_ENTRY.md`：将 Rollback Router 纳入 Run Engine 结构，并规定 step failure 在继续、暂停或回退前必须先选择唯一 route。
- `04A_OBSERVING_MODULES.md`：在 Bootstrap 原子序列中加入 issue matching，普通 run 启动时必须先尝试复用 issue。
- `02_EXECUTION_PROFILE_CONTROLLER.md`：补充 L1 → L2、L2 → L3 升级触发、禁止降级条件与中途升级补记要求。
- `08_GOVERNANCE_MODULE.md`：将正式治理反审从建议性流程强化为必须执行，并新增 L3 阻断条件。
- `12_SCHEMAS_MODULE.md`：明确每个非公共 schema 必须有 valid example，并要求 schema 变更同步更新 fixture。
- `13_MINIMAL_RUNNER_MODULE.md`：补充 valid example 校验路径。
- `README.md` 与 `00_INDEX.md`：版本推进到 `v4.5.1`，新增 Rollback Router 与本轮治理补强说明。
- `00_ENTRYPOINT_SINGLE_FILE.md`：降级为历史总版参考，明确不得作为 prompt、cron、profile、runner 或 agent 装配入口。

## 设计原则
- Rollback Router 是共享控制模块，不单独代表 workflow_state。
- `run_uid` 每次 run 新建；`issue_uid` 必须先匹配复用，未命中或有歧义时才新建或暂停复核。
- execution profile 可以升级，但升级必须补记，执行后不得无记录降级。
- schema valid examples 是治理资产；缺失或无法校验会阻断 L3 完整闭环。
- `00_INDEX.md` 仍是唯一执行入口。
