# 02. Execution Profile Controller「执行档位控制器」

> 作用：决定当前任务应装配哪些模块、记录到多重、证据要求多硬、能否进入闭环。
> 原则：v4 保留 L1 / L2 / L3，但其语义改为 execution profile「执行档位」，不再只是“跑哪几步”。

---

## 一、三档定义

### 1.1 L1 = Probe Profile「探针档」
适用：
- 快速判断
- 单点核查
- 低风险探测
- 独立模块调用

要求：
- 可只装配少量模块
- 不强制完整落库
- 必须有最小记录
- 必须至少一条有效证据
- 不得伪装成完整闭环

### 1.2 L2 = Standard Profile「标准档」
适用：
- 一般排障
- 一般修复验证
- 常规变更检查
- 一般安装 / 部署变更

要求：
- 必须有完整 plan「执行计划」
- 必须有 checklist「检查清单」
- 必须有 running note
- 必须可追踪
- 可进入简化闭环

### 1.3 L3 = Closure Profile「闭环档」
适用：
- 生产级闭环
- 长期维护
- 自动化执行
- 关键链路问题
- 高风险安装 / 部署 / 调试 / 发布

要求：
- 必须强制落库
- 必须强 schema「强结构」
- 必须可审计
- 必须可回放
- 必须完成完整闭环

---

## 二、判断维度

必须评估三项：

1. uncertainty「不确定性」
2. impact「影响面」
3. rollbackability「可回滚性」

### 2.1 评分口径
- `0` = 低
- `1` = 中
- `2` = 高

### 2.2 建议判定
- 总分 `0~1` → L1
- 总分 `2~3` → L2
- 总分 `>=4` → L3

### 2.3 直接进入 L3 的触发条件
满足任意一条，直接 L3：
- 涉及核心系统
- 涉及数据一致性
- 涉及分布式状态
- Agent 行为不可预测
- 状态污染明显
- 无法安全回滚
- 生产环境部署或切流量
- 高风险安装或不可逆环境修改

---

## 三、控制职责

Execution Profile Controller 负责：

- 选择当前 execution profile
- 决定必须装配的模块集合
- 决定记录强度
- 决定证据下限
- 决定是否允许 standalone module call「单模块调用」
- 决定是否允许 closing「闭环阶段」成立
- 决定是否允许附加 optional capability modules「可选能力模块」
- 决定 Context Controller / Tool Contract Registry / Memory Layer / Runtime Adapter 的装配强度

---

## 四、装配矩阵

| profile | 必装模块 | 可选模块 | 闭环要求 |
|---|---|---|---|
| L1 | Kernel + Context + Record + 至少一个 Run Module | Tool Contract + Runtime Adapter + 其余 Run Modules + Debug + 局部 Development / Installation Check | 不得宣称完整闭环 |
| L2 | Kernel + Context + Tool Contract + Record + Run Engine | Closing + Memory Read + Runtime Adapter + Development + Installation + Deployment + Debug | 可进入简化闭环 |
| L3 | Kernel + Context + Tool Contract + Record + Run Engine + Closing | Memory Read/Write + Runtime Adapter + Development + Installation + Deployment + Debug + Regression Executor | 必须完整闭环 |

### 4.1 Regression Asset 条件装配

当 Closing Module 判定 `rule_required = true` 时，`06_REGRESSION_ASSET_MODULE.md` 从可选模块升级为条件必装模块。

要求：
- 必须创建或更新 regression rule asset「回归规则资产」
- 必须返回 `rule_uid`、规则物理落点、结构化写入结果与回读结果
- 在规则资产回读成功前，不得宣称 L3 完整闭环

`07_REGRESSION_EXECUTOR_MODULE.md` 仅在需要执行 active rule「激活规则」或周期性回归任务时装配，不作为每次 Closing 的默认必装模块。

### 4.2 Context / Tool / Memory / Runtime 装配边界

- `02A_CONTEXT_CONTROLLER_MODULE.md`：L1 / L2 / L3 均应装配，至少完成当前 objective、证据指针与过期假设裁剪。
- `02B_TOOL_CONTRACT_REGISTRY.md`：L2 / L3 必装；L1 在调用工具时按需装配。
- `03A_MEMORY_LAYER_MODULE.md`：L2 可只读装配；L3 在 Closing 后可写入长期 memory。
- `11_RUNTIME_ADAPTER_MODULE.md`：当任务需要文件、命令、浏览器、数据库、日志、CI、部署或外部系统适配时装配。

这些模块均不构成新的 workflow_state，也不得替代 Step Orchestrator 推进流程。

---

## 五、optional capability modules 装配建议

### 5.1 Development Module「开发模块」
建议在以下情况装配：
- 需要产出 patch「补丁」/ diff「差异」/ 配置修改
- 需要 build「构建」/ compile「编译」/ package「打包」
- Fixing Module 需要实现性变更支撑

### 5.2 Installation Module「安装模块」
建议在以下情况装配：
- 需要安装依赖、组件、二进制、服务
- 需要准备环境、校验前置条件、执行安装回滚

### 5.3 Deployment Module「部署模块」
建议在以下情况装配：
- 需要把变更切入运行环境
- 需要做 rollout「发布推进」/ health gate「健康门」/ rollback「回滚」

### 5.4 Debug Module「调试模块」
建议在以下情况装配：
- 需要低副作用探针
- 需要 trace「链路捕获」/ dump「转储」/ safe instrumentation「安全插桩」
- 需要增强 Observing / Reproducing / Isolating / Attributing / Verifying 证据

---

## 六、输出格式

每次判断必须输出：

```md
- execution_profile: L1 | L2 | L3
- reason: <原因>
- trigger: <触发条件>
- required_modules: <必须装配模块>
- optional_modules: <可选附加模块>
- next_action: <下一步>
```
