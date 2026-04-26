# 🧠 Harness v4 模块化规范套件 v4.4.0

> 目标：提供一套可由 Hermes / Agent「智能体」直接读取、装配与执行的 Harness v4 模块化规范。
> 定位：本套件为 v4 的目录化版本；保留 workflow「流程」主线，同时把能力拆为 module「模块」与 controller「控制器」。
> 本版更新：新增 Minimal Runner，跑通 schema 校验、artifact 写入与 readback 的最小本地可执行路径。

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

### 如需机器校验 / runner 接入
按需附加：
18. `12_SCHEMAS_MODULE.md`
19. `schemas/`
20. `13_MINIMAL_RUNNER_MODULE.md`
21. `runner/`
22. `examples/`

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
├── Runtime Adapter Module「运行时适配器模块」
├── Schemas Module「结构校验模块」
└── Minimal Runner Module「最小运行器模块」
```

---

## 三、硬规则

- module「模块」可以单独调用；workflow_state「流程状态」只能由 Step Orchestrator「步骤编排器」推进。
- 不记录，不算完成；不回读，不算退出。
- `closing` 是 workflow_state「流程状态」；`closed` 是 lifecycle_state「生命周期结果态」。
- `run_uid / issue_uid / rule_uid / source_issue_uid` 是业务主标识；`id` 仅用于数据库内部主键。
- `checks.result` 与 `regression_rule_runs.result` 不共享枚举。
- Context Controller 不推进 workflow_state；它只负责上下文装配、裁剪、恢复与防漂移。
- Context Gate 是进入工具调用或模型决策前的前置门；Record Gate 是步骤或模块退出前的出口门。
- Tool Contract Registry 不执行工具；它只定义工具契约、边界、产物与回读要求。
- L2 / L3 正式工具调用必须引用 Tool Contract，并通过 Runtime Adapter 产出可回读 pointer。
- Memory Layer 不替代 primary record db；记忆只能辅助决策，不能覆盖当前证据。
- Memory 只能从已闭环且已回读的 run 中沉淀；读取 memory 时必须标记适用性与置信度。
- Runtime Adapter 不改变 Harness 状态机；它只把工具契约映射到具体运行环境。
- Runtime Adapter 输出的 pointer 必须具备可定位、可回读、可复核的最小字段。
- JSON Schema 只负责结构校验；schema 校验通过不等于 Record Gate 通过。
- L3 强结构对象必须通过对应 `schemas/*.schema.json` 校验后，才允许进入完整闭环资产。
- Minimal Runner 只执行 schema 校验、artifact 写入与 readback，不推进 workflow_state。
- runner readback 通过只证明 artifact 可定位、可解析，不等于 Record Gate 通过。
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
- `10_CHANGELOG_v4.2.1.md`
- `10_CHANGELOG_v4.3.0.md`
- `10_CHANGELOG_v4.4.0.md`
- `11_RUNTIME_ADAPTER_MODULE.md`
- `12_SCHEMAS_MODULE.md`
- `13_MINIMAL_RUNNER_MODULE.md`
- `examples/`
- `runner/`
- `schemas/`

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
  10_CHANGELOG_v4.2.1.md
  10_CHANGELOG_v4.3.0.md
  10_CHANGELOG_v4.4.0.md
  11_RUNTIME_ADAPTER_MODULE.md
  12_SCHEMAS_MODULE.md
  13_MINIMAL_RUNNER_MODULE.md
  examples/
  runner/
  schemas/
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
- 需要机器校验、runner 接入或强结构闭环：再读取 `Schemas Module + schemas/`
- 需要本地最小执行闭环：再读取 `Minimal Runner Module + runner/ + examples/`
- 版本治理：再读取 `Governance Module`
