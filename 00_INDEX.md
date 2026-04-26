# 🧠 Harness v4 模块化规范套件 v4.2.0

> 目标：提供一套可由 Hermes / Agent「智能体」直接读取、装配与执行的 Harness v4 模块化规范。
> 定位：本套件为 v4 的目录化版本；保留 workflow「流程」主线，同时把能力拆为 module「模块」与 controller「控制器」。
> 本版更新：新增 Context Controller、Tool Contract Registry、Memory Layer 与 Runtime Adapter，补齐上下文装配、工具契约、长期记忆与运行适配边界。

---

## 一、阅读顺序

### 最小入口
1. `00_INDEX.md`
2. `01_KERNEL_MODULE.md`
3. `02_EXECUTION_PROFILE_CONTROLLER.md`
4. `02A_CONTEXT_CONTROLLER_MODULE.md`
5. `02B_TOOL_CONTRACT_REGISTRY.md`
6. `03_RECORD_AND_EVIDENCE_MODULE.md`
7. `04_RUN_ENGINE_ENTRY.md`
8. `05_CLOSING_MODULE.md`

### 如需长期防复发
继续阅读：
9. `06_REGRESSION_ASSET_MODULE.md`
10. `07_REGRESSION_EXECUTOR_MODULE.md`

### 如需规范治理
最后阅读：
11. `08_GOVERNANCE_MODULE.md`

### 如需工程变更 / 环境处理 / 调试能力
按需附加：
12. `04G_DEVELOPMENT_MODULE.md`
13. `04H_INSTALLATION_MODULE.md`
14. `04I_DEPLOYMENT_MODULE.md`
15. `04J_DEBUG_MODULE.md`

### 如需跨运行记忆或环境适配
按需附加：
16. `03A_MEMORY_LAYER_MODULE.md`
17. `11_RUNTIME_ADAPTER_MODULE.md`

---

## 二、总模块图

```text
Harness v4
├── Kernel Module「内核模块」
├── Execution Profile Controller「执行档位控制器」
├── Context Controller Module「上下文控制器模块」
├── Tool Contract Registry「工具契约注册表」
├── Record & Evidence Module「记录与证据模块」
├── Memory Layer Module「记忆层模块」
├── Run Engine「运行引擎」
│   ├── Step Orchestrator「步骤编排器」
│   ├── Observing Modules「观察模块组」
│   ├── Reproducing Modules「复现模块组」
│   ├── Isolating Modules「隔离模块组」
│   ├── Attributing Modules「归因模块组」
│   ├── Fixing Modules「修复模块组」
│   ├── Verifying Modules「验证模块组」
│   └── Optional Capability Modules「可选能力模块」
│       ├── Development Module「开发模块」
│       ├── Installation Module「安装模块」
│       ├── Deployment Module「部署模块」
│       └── Debug Module「调试模块」
├── Closing Module「闭环模块」
├── Regression Asset Module「回归资产模块」
├── Regression Executor Module「回归执行器模块」
├── Governance Module「治理模块」
└── Runtime Adapter Module「运行时适配器模块」
```

---

## 三、硬规则

- module「模块」可以单独调用；workflow_state「流程状态」只能由 Step Orchestrator「步骤编排器」推进。
- 不记录，不算完成；不回读，不算退出。
- `closing` 是 workflow_state「流程状态」；`closed` 是 lifecycle_state「生命周期结果态」。
- `run_uid / issue_uid / rule_uid / source_issue_uid` 是业务主标识；`id` 仅用于数据库内部主键。
- `checks.result` 与 `regression_rule_runs.result` 不共享枚举。
- Context Controller 不推进 workflow_state；它只负责上下文装配、裁剪、恢复与防漂移。
- Tool Contract Registry 不执行工具；它只定义工具契约、边界、产物与回读要求。
- Memory Layer 不替代 primary record db；记忆只能辅助决策，不能覆盖当前证据。
- Runtime Adapter 不改变 Harness 状态机；它只把工具契约映射到具体运行环境。
- `04G~04J` 为 optional capability modules；它们可以被调用，但不单独构成新的 workflow_state。
- optional capability modules 退出前仍必须通过 Record Gate「记录出口守卫」。

---

## 四、目录清单

- `01_KERNEL_MODULE.md`
- `02_EXECUTION_PROFILE_CONTROLLER.md`
- `02A_CONTEXT_CONTROLLER_MODULE.md`
- `02B_TOOL_CONTRACT_REGISTRY.md`
- `03_RECORD_AND_EVIDENCE_MODULE.md`
- `03A_MEMORY_LAYER_MODULE.md`
- `04_RUN_ENGINE_ENTRY.md`
- `04A_OBSERVING_MODULES.md`
- `04B_REPRODUCING_MODULES.md`
- `04C_ISOLATING_MODULES.md`
- `04D_ATTRIBUTING_MODULES.md`
- `04E_FIXING_MODULES.md`
- `04F_VERIFYING_MODULES.md`
- `04G_DEVELOPMENT_MODULE.md`
- `04H_INSTALLATION_MODULE.md`
- `04I_DEPLOYMENT_MODULE.md`
- `04J_DEBUG_MODULE.md`
- `05_CLOSING_MODULE.md`
- `06_REGRESSION_ASSET_MODULE.md`
- `07_REGRESSION_EXECUTOR_MODULE.md`
- `08_GOVERNANCE_MODULE.md`
- `09_TEMPLATES.md`
- `10_CHANGELOG_v4.1.0.md`
- `10_CHANGELOG_v4.1.1.md`
- `10_CHANGELOG_v4.2.0.md`
- `11_RUNTIME_ADAPTER_MODULE.md`

---

## 五、推荐落盘方式

```text
/harness-v4/
  00_INDEX.md
  01_KERNEL_MODULE.md
  02_EXECUTION_PROFILE_CONTROLLER.md
  02A_CONTEXT_CONTROLLER_MODULE.md
  02B_TOOL_CONTRACT_REGISTRY.md
  03_RECORD_AND_EVIDENCE_MODULE.md
  03A_MEMORY_LAYER_MODULE.md
  04_RUN_ENGINE_ENTRY.md
  04A_OBSERVING_MODULES.md
  04B_REPRODUCING_MODULES.md
  04C_ISOLATING_MODULES.md
  04D_ATTRIBUTING_MODULES.md
  04E_FIXING_MODULES.md
  04F_VERIFYING_MODULES.md
  04G_DEVELOPMENT_MODULE.md
  04H_INSTALLATION_MODULE.md
  04I_DEPLOYMENT_MODULE.md
  04J_DEBUG_MODULE.md
  05_CLOSING_MODULE.md
  06_REGRESSION_ASSET_MODULE.md
  07_REGRESSION_EXECUTOR_MODULE.md
  08_GOVERNANCE_MODULE.md
  09_TEMPLATES.md
  10_CHANGELOG_v4.1.0.md
  10_CHANGELOG_v4.1.1.md
  10_CHANGELOG_v4.2.0.md
  11_RUNTIME_ADAPTER_MODULE.md
```

---

## 六、使用原则

- 普通快速检查：读取 `Kernel + Execution Profile + Context + Tool Contract + Record + Run Engine`
- 一般排障：再读取全部 `04A~04F` 模块
- 需要代码/配置变更实现：再读取 `04G_DEVELOPMENT_MODULE.md`
- 需要装环境或装依赖：再读取 `04H_INSTALLATION_MODULE.md`
- 需要发版、切流量、做回滚：再读取 `04I_DEPLOYMENT_MODULE.md`
- 需要低副作用调试与探针：再读取 `04J_DEBUG_MODULE.md`
- 完整闭环：再读取 `Closing Module`
- 长期巡检：再读取 `Regression Asset + Regression Executor`
- 需要跨 run 经验复用：再读取 `Memory Layer`
- 需要接入具体文件、命令、浏览器、数据库、CI 或发布环境：再读取 `Runtime Adapter`
- 版本治理：再读取 `Governance Module`
