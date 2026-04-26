# 04. Run Engine「运行引擎」入口

> 作用：负责一次问题处理 run 内的 workflow「流程层」推进。
> 原则：Run Engine 负责流程推进；具体能力由各模块组执行；workflow_state 只能由 Step Orchestrator「步骤编排器」推进。

---

## 一、总结构

```text
Run Engine
├── Step Orchestrator
├── Rollback Router
├── Context Controller
├── Tool Contract Registry
├── Observing Modules
├── Reproducing Modules
├── Isolating Modules
├── Attributing Modules
├── Fixing Modules
├── Verifying Modules
└── Optional Capability Modules
    ├── Development Module
    ├── Installation Module
    ├── Deployment Module
    └── Debug Module
```

---

## 二、职责分工

### 2.1 Step Orchestrator「步骤编排器」
负责：
- 进入哪个 workflow_state
- 当前步骤退出条件是否满足
- 是否允许下一步
- 是否必须 rollback「回退」
- 是否必须升级 execution profile
- 是否需要调用 optional capability modules

### 2.2 Rollback Router「回退路由器」
负责：
- 为所有 step failure 提供唯一全局回退表
- 将 failure reason、failure evidence、retry condition 与 cleanup / containment 写入记录
- 支撑 Step Orchestrator 做继续、暂停或回退判定
- 防止各模块自行定义互相冲突的 rollback route

Rollback Router 不推进 workflow_state；它只输出路由决策，最终推进仍由 Step Orchestrator 执行。

### 2.3 各 Step Module Group「步骤模块组」
负责：
- 执行当前步骤的局部能力
- 产出证据
- 产出结论候选
- 回写记录模块

### 2.4 Context Controller「上下文控制器」
负责：
- 在 run 启动、step 切换、module 调用与压缩恢复时装配上下文
- 标记 pointer-only context、过期假设与暂定内容
- 将装配结果写入 Record & Evidence Module

Context Controller 不推进 workflow_state。

### 2.5 Tool Contract Registry「工具契约注册表」
负责：
- 为工具调用提供契约、输入输出 schema、副作用等级、失败处理与证据落点
- 为 Runtime Adapter 提供执行映射依据
- 为 Context Controller 提供可注入工具摘要

Tool Contract Registry 不直接执行工具。

### 2.6 Optional Capability Modules「可选能力模块」
负责：
- 提供 development / installation / deployment / debug 能力
- 支撑 Fixing / Verifying / Observing 等步骤
- 产出工程类日志、产物与验证结果
- 回写记录模块

### 2.7 Record & Evidence Module「记录与证据模块」
负责：
- 计划
- 快照
- 清单
- 证据指针
- 回读验证

---

## 三、硬规则

- module 可以单独调用，但单独调用不等于 Step 完成。
- 只有 Step Orchestrator 能推进 workflow_state。
- 单模块调用必须标记 `module_mode`。
- `04G~04J` 不单独代表新的 workflow_state。
- `04G~04J` 退出前仍必须通过 Record Gate。
- Context Controller / Tool Contract Registry / Memory Layer / Runtime Adapter 不单独代表新的 workflow_state。
- Rollback Router 不单独代表新的 workflow_state，也不得替代 Step Orchestrator 推进流程。
- 任何 step failure 在继续推进、暂停或回退前，必须先通过 Rollback Router 选择唯一 route。
- 正式 L2 / L3 工具调用必须引用 Tool Contract，并产出可回读 evidence pointer。
- 工具调用前必须完成 Context Gate；工具调用后必须完成 Tool Call Snapshot 与 Record Gate。
- Runtime Adapter 失败只能作为运行环境证据，不得直接写成 Target System 根因。

### 3.1 module_mode「模块调用模式」
允许：
- `probe`
- `assist`
- `standalone_check`
- `in_workflow`
- `change_execution`
- `release_execution`

推荐用法：
- `probe`：低副作用探测，常用于 Debug Module。
- `assist`：支撑当前 workflow_state，但不独立完成当前 Step。
- `standalone_check`：独立核查，不推进 workflow_state。
- `in_workflow`：作为当前 Step 的组成部分执行。
- `change_execution`：执行代码、配置或环境变更，常用于 Development / Installation Module。
- `release_execution`：执行发布、切流量或回滚，常用于 Deployment Module。

---

## 四、退出规则

每个 Step 或 capability module 的退出，至少同时满足：
- 证据门槛满足
- 当前步或当前模块核心结论已写
- Record Gate 已通过
- 下一步或回退方向已明确

### 4.1 横切模块退出顺序

涉及工具或环境适配的调用，推荐顺序为：

```text
Context Gate
→ Tool Contract lookup
→ Runtime Adapter execution
→ Tool Call / Adapter Snapshot
→ Record Gate
→ Rollback Router decision（仅失败或无法推进时）
→ Step Orchestrator decision
```

说明：
- Context Gate 负责确认“模型看到什么”。
- Tool Contract Registry 负责确认“工具应该怎么被调用”。
- Runtime Adapter 负责确认“运行环境实际发生了什么”。
- Record Gate 负责确认“发生的事是否已写入并可回读”。
- Rollback Router 负责在失败或无法推进时给出唯一回退路由。
- Step Orchestrator 只在以上结果满足后决定是否推进 workflow_state。

---

## 五、Optional Capability Modules 装配原则

### 5.1 Development Module「开发模块」
- 主要由 Fixing Module 调用
- 也可被 standalone change task「独立变更任务」调用

### 5.2 Installation Module「安装模块」
- 可由 Fixing / Verifying / Deployment 前置检查调用
- 不默认等于部署完成

### 5.3 Deployment Module「部署模块」
- 主要由 Fixing 后或 release task 调用
- 必须受 health gate 与 rollback 约束

### 5.4 Debug Module「调试模块」
- 可横切 Observing / Reproducing / Isolating / Attributing / Verifying
- 只提供探针与证据，不直接等于修复

---

## 六、模块组说明

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
- `04X_ROLLBACK_ROUTER_MODULE.md`
- `02A_CONTEXT_CONTROLLER_MODULE.md`
- `02B_TOOL_CONTRACT_REGISTRY.md`
- `03A_MEMORY_LAYER_MODULE.md`
- `11_RUNTIME_ADAPTER_MODULE.md`
