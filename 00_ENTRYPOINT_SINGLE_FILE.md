# 🧠 Harness v4 模块化控制规范（可执行版）

> 目标：构建一套可由 Agent「智能体」直接执行、可模块装配、可审计、可回放、可闭环的 Harness v4 规范。  
> 定位：本文件为 v4 的主入口「entrypoint 总入口」+ 可执行规范「executable spec 可执行规范」。  
> 原则：不推翻 v3，而是在 v3 已有的总则、等级、状态机、Step 7、回归规则与执行器基础上，升级为模块化体系。

---

# 一、v4 的核心变化

v4 相比 v3 的核心变化不是“多几份文档”，而是把 Harness 从“按步骤阅读的规范”，升级为“按模块装配的系统”。

v4 采用两层结构：

1. **workflow「流程层」**  
   保留问题处理的一阶顺序：
   `observing「观察」 → reproducing「复现」 → isolating「隔离」 → attributing「归因」 → fixing「修复」 → verifying「验证」 → closing「闭环」`

2. **module「模块层」**  
   将每一步拆成可复用能力模块；模块可以单独调用，但单独调用不等于流程推进。

## 1.1 v4 的总原则

- 先确认问题存在，再确认问题稳定，再确认问题独立，最后确认解释唯一。
- 日志不是事实，事实必须由独立证据集合支撑。
- module「模块」可以单独运行；workflow state「流程状态」只能由 orchestrator「编排器」推进。
- 不记录，不算完成；不回读，不算退出。
- closing「闭环阶段」是流程状态；closed「已完成」是生命周期结果态。
- 回归规则属于长期能力，不属于 Step 1~6 主流程本体。

---

# 二、v4 的总模块图

```text
Harness v4
├── Kernel Module
├── Execution Profile Controller
├── Record & Evidence Module
├── Run Engine
│   ├── Step Orchestrator
│   ├── Observing Module Group
│   ├── Reproducing Module Group
│   ├── Isolating Module Group
│   ├── Attributing Module Group
│   ├── Fixing Module Group
│   ├── Verifying Module Group
│   └── Optional Capability Modules
│       ├── Development Module
│       ├── Installation Module
│       ├── Deployment Module
│       └── Debug Module
├── Closing Module
├── Regression Asset Module
├── Regression Executor Module
└── Governance Module
```

## 2.1 模块边界原则

- **Kernel Module「内核模块」**：只放全局唯一口径。
- **Controller「控制器」**：只负责判定、装配、门控，不直接做业务动作。
- **Engine「执行引擎」**：负责本次 run「运行」内的具体动作。
- **Asset Module「资产模块」**：负责长期对象结构，例如 rule「规则」、artifact「产物」、record「记录」。
- **Executor Module「执行器模块」**：负责把长期资产跑起来。
- **Governance Module「治理模块」**：负责版本、patch「补丁」、反审、Cron「定时任务」治理。

---

# 三、Kernel Module「内核模块」

Kernel Module 只定义全局唯一、不可漂移的口径。

## 3.1 对象边界

### 3.1.1 Harness
Harness 是统一控制与决策中枢，负责观察、复现、隔离、归因、修复、验证、闭环与长期治理。

### 3.1.2 Target System「被管控对象」
Target System 指被 Harness 监督、排障、验证、优化或治理的任意对象，包括：
- 服务
- Agent
- 模块
- 子系统
- profile「配置实例」
- 实例
- 外部依赖

### 3.1.3 Control Root「控制根」
承载控制体系总入口、全局装配、路由与控制平面状态的目录或目录树根。

### 3.1.4 Target Root「目标根」
某个被管控对象、角色、profile、实例或服务的根目录。

### 3.1.5 Self-governance「自监督」
当 Harness 监督控制根本身时，必须显式标记为 self-governance，不得与普通 target「目标」混写。

## 3.2 权威顺序

统一权威顺序如下：

1. primary record db「主记录库」
2. running note / narrative「过程主文档」
3. runtime logs / temporary outputs「运行时日志与临时输出」

若三者不一致：
- 必须以 primary record db 为准
- 必须记录差异
- 差异必须可回读

## 3.3 统一命名口径

### 3.3.1 标识符
- `run_uid`：运行业务主标识
- `issue_uid`：问题业务主标识
- `rule_uid`：规则业务主标识
- `source_issue_uid`：规则来源问题标识
- `id`：数据库内部自增主键

禁止混用：
- 不允许用 `run_id` 表示业务主标识
- 不允许用 `rule_id` 表示业务主标识
- `issue_uid` 在规则语境中如表示来源问题，必须写作 `source_issue_uid`

## 3.4 统一状态口径

### 3.4.1 workflow_state「流程状态」
必须使用：
- `observing`
- `reproducing`
- `isolating`
- `attributing`
- `fixing`
- `verifying`
- `closing`

### 3.4.2 lifecycle_state「生命周期结果态」
建议使用：
- `open`
- `investigating`
- `fixing`
- `verifying`
- `closed`

说明：
- `closing` 是流程态，不是最终结果态。
- `closed` 是结果态，不是 Step 名称。

## 3.5 统一结果口径

### 3.5.1 checks.result
只允许：
- `pass`
- `fail`
- `unknown`

### 3.5.2 regression_rule_runs.result
只允许：
- `pass`
- `fail`
- `error`
- `skipped`

禁止将两者合并为同一字段或同一枚举。

---

# 四、Execution Profile Controller「执行档位控制器」

v4 保留 L1 / L2 / L3，但语义改为 execution profile「执行档位」，而不是简单表示“跑几步”。

## 4.1 三档定义

### L1：Probe Profile「探针档」
适用：快速判断、单点核查、低风险探测、独立模块调用。

要求：
- 可只装配少量模块
- 不强制完整落库
- 必须有最小记录
- 必须至少有一条有效证据
- 不得伪装成完整闭环

### L2：Standard Profile「标准档」
适用：一般排障、一般修复验证、常规变更检查。

要求：
- 必须有完整 plan「执行计划」与 checklist「检查清单」
- 必须有 running note
- 必须可追踪
- 可进入简化闭环

### L3：Closure Profile「闭环档」
适用：生产级闭环、长期维护、自动化执行、关键链路。

要求：
- 必须强制落库
- 必须强 schema「强结构」
- 必须可审计
- 必须可回放
- 必须完成完整闭环

## 4.2 档位判断维度

必须评估：
- uncertainty「不确定性」
- impact「影响面」
- rollbackability「可回滚性」

### 评分口径
- `0` = 低
- `1` = 中
- `2` = 高

### 建议判定
- 总分 `0~1` → L1
- 总分 `2~3` → L2
- 总分 `>=4` → L3

### 直接进入 L3 的触发条件
满足任意一条，直接 L3：
- 涉及核心系统
- 涉及数据一致性
- 涉及分布式状态
- Agent 行为不可预测
- 无法安全回滚
- 状态污染明显

## 4.3 档位的真正作用

execution profile 负责决定：
- 当前 run 必须装配哪些模块
- 记录强度到什么级别
- 证据门槛有多高
- 是否必须落库
- 是否必须回读
- 是否允许 standalone module call「独立模块调用」

## 4.4 升级规则

### L1 → L2
满足任意一条：
- 现象不稳定
- 需要交叉验证
- 影响范围不清
- 单模块 probe 无法收敛

### L2 → L3
满足任意一条：
- 存在多个竞争根因
- 修复影响未知
- 涉及多个系统 / 多 Agent
- 需要完整闭环与长期治理

### 降级规则
- 禁止从高档位降级到低档位

---

# 五、Record & Evidence Module「记录与证据模块」

这是 v4 的横切强制模块。所有 step module「步骤模块」和 standalone module call 在退出前都必须经过该模块。

## 5.1 记录原则

- 每一步完成时都必须记录相关重点
- 记录的是“步骤重点摘要”，不是全量流水
- 大段日志、完整 diff、长输出必须以 pointer「指针」或 artifact「产物」方式引用
- 不记录，不算完成
- 不回读，不算退出

## 5.2 四个记录子模块

### 5.2.1 Plan Writer「计划写入器」
每个 run 在进入正式执行前必须创建 Execution Plan「执行计划」。

最少字段：
- `run_uid`
- `issue_uid`
- `target`
- `execution_profile`
- `current_step`
- `objective`
- `hypothesis`
- `constraints`
- `evidence_needed`
- `stop_conditions`
- `next_step`

### 5.2.2 Step Snapshot Writer「步骤快照写入器」
每进入一个 step，必须在同一份 running note 中追加一条 Step Snapshot「步骤快照」。

最少字段：
- `step`
- `objective`
- `action_summary`
- `key_evidence`
- `evidence_pointer`
- `decision`
- `next_or_rollback`
- `readback_status`

### 5.2.3 Checklist Writer「清单写入器」
每一步退出前必须更新 checklist。

最少检查项：
- [ ] 目标已明确
- [ ] 输入已确认
- [ ] 风险已评估
- [ ] 证据路径已确定
- [ ] 当前步输出已写入 running note
- [ ] 当前步结果已回读验证
- [ ] 退出条件已评估
- [ ] 回退条件已评估

### 5.2.4 Evidence Pointer Writer「证据指针写入器」
负责将原始证据绑定为 pointer / artifact，而不是直接把原始长内容写入主文档。

支持：
- `log_pointer`
- `command_output_pointer`
- `file_snapshot_pointer`
- `diff_pointer`
- `db_result_pointer`
- `image_pointer`
- `manual_note_pointer`

## 5.3 Record Gate「记录出口守卫」

任何 step module 或 standalone module call 在退出前必须通过 Record Gate。

### 必须同时满足
- Step Snapshot 已写
- Checklist 已更新
- 至少一个 evidence pointer 已绑定
- 当前结论已写
- next / rollback 已写
- 当前记录已回读成功

不满足任意一项：
- 当前模块不得标记完成
- workflow_state 不得推进

## 5.4 running note「运行主文档」规则

- 每个任务必须且仅有一个主过程文档
- 运行期名称为 running note
- 闭环后的语义角色为 narrative「叙事记录」
- 不得再创建新的“主 narrative”替代原 running note
- Step 1~6 的每一步输出必须在产生时同步追加写入同一份 running note
- Step 7 继续在同一份文档中完成收束与总结

## 5.5 默认记录粒度

每一步只要求记录：
- 当前步骤目标
- 本步关键动作摘要
- 本步关键证据摘要与 pointer
- 本步结论
- 下一步或回退方向

默认不直接全文写入：
- 大段命令输出
- 全量日志
- 大型 diff
- 重复中间过程
- 完整截图内容

---

# 六、Run Engine「运行引擎」

Run Engine 负责本次问题处理的主流程，不负责长期回归治理。

## 6.1 Step Orchestrator「步骤编排器」

Step Orchestrator 是唯一允许推进 workflow_state 的组件。

职责：
- 选择当前 step
- 判断进入条件
- 判断退出条件
- 控制回退
- 调度对应 module group
- 调用 Record Gate

### 强规则
- module 可以单独运行
- module 不得自行修改 workflow_state
- 只有 Step Orchestrator 可以把状态从一个 step 推到下一个 step

## 6.2 standalone module call「独立模块调用」

v4 允许单独调用模块，例如：
- 单独做一次复现
- 单独做一次 live verification「在线验证」
- 单独做一次 rollback assessment「回滚评估」

但必须满足：
- 结果只能记为 `partial` / `probe` / `assist`
- 不得宣称某个 step 已整体完成
- 不得自动推进 workflow_state
- 仍必须经过 Record Gate

---

# 七、Observing Module Group「观察模块组」

## 7.1 目标
建立客观事实，完成任务初始化。

## 7.2 子模块

### 7.2.1 Bootstrap Module「初始化模块」
职责：
- 生成 `run_uid`
- 生成 `issue_uid`
- 创建 running note
- 初始化最小 record「记录」
- 回读初始化结果

### 7.2.2 Evidence Intake Module「证据摄取模块」
职责：
- 收集日志、状态、指标、配置、文档、结构图
- 标记证据来源
- 去除明显噪音

### 7.2.3 Fact Normalize Module「事实归一模块」
职责：
- 从观测中提取事实清单
- 区分“现象”“推测”“已证事实”

### 7.2.4 Scope Seed Module「范围播种模块」
职责：
- 给出初步异常范围
- 给出待复现对象

## 7.3 退出条件

### L1
- 至少一条有效证据
- 异常可被简洁复述

### L2 / L3
- 至少两条独立证据
- 目标明确
- 异常可复述

---

# 八、Reproducing Module Group「复现模块组」

## 8.1 目标
确认问题稳定存在。

## 8.2 子模块

### 8.2.1 Replay Runner「重放执行器」
同一路径重复执行，确认复现稳定性。

### 8.2.2 Cross-Path Reproducer「交叉路径复现器」
不同入口 / 不同路径交叉复现。

### 8.2.3 Contamination Check「污染检查器」
检查 memory / session / cache / 进程残留污染。

### 8.2.4 Repro Rate Evaluator「复现率评估器」
计算复现成功率与路径一致性。

## 8.3 退出条件

### L1
- 单一路径重复成立
- 主要污染已排查

### L2 / L3
- 复现成功率建议 ≥ 80%
- 至少两个路径成立
- 污染已控制

---

# 九、Isolating Module Group「隔离模块组」

## 9.1 目标
缩小问题范围。

## 9.2 子模块

### 9.2.1 Variable Control Module「变量控制模块」
一次只改一个变量。

### 9.2.2 Minimal Difference Finder「最小差异查找器」
识别最小差异集。

### 9.2.3 Interference Elimination Module「干扰剔除模块」
排除无关变量与噪音来源。

### 9.2.4 Boundary Convergence Evaluator「边界收敛评估器」
判断问题边界是否收敛到可定位层级。

## 9.3 退出条件
- 变量边界收敛
- 存在可重复影响变量

---

# 十、Attributing Module Group「归因模块组」

## 10.1 目标
找到唯一成立的解释。

## 10.2 子模块

### 10.2.1 Hypothesis Registry「假设登记器」
维护候选解释与竞争解释。

### 10.2.2 Causal Test Module「因果测试模块」
验证：改变关键变量，问题消失；恢复关键变量，问题复现。

### 10.2.3 Alternative Rejection Module「备选排除模块」
排除其他竞争解释。

### 10.2.4 Root Cause Selector「根因选择器」
输出唯一成立解释。

## 10.3 退出条件
- 当前问题边界内，候选解释仅剩一个
- 至少两个证据来源支持同一解释
- 关键变量变化可导致问题消失 / 恢复

---

# 十一、Fixing Module Group「修复模块组」

## 11.1 目标
提出并执行最小有效修复。

## 11.2 子模块

### 11.2.1 Fix Strategy Planner「修复策略规划器」
评估候选修复路径。

### 11.2.2 Fix Type Classifier「修复类型分类器」
必须区分：
- `root_fix`：根因修复
- `defensive_fix`：防御修复

### 11.2.3 Fix Executor「修复执行器」
执行修复动作，并记录变更。

### 11.2.4 Rollback Risk Evaluator「回滚风险评估器」
评估回滚条件、残留污染、可逆性。

## 11.3 输出要求
- 修复方案
- 修复类型
- 风险说明
- 回滚方案
- 变更证据

---

# 十二、Verifying Module Group「验证模块组」

## 12.1 目标
确认本次修复有效，且未引入明显副作用。

## 12.2 子模块

### 12.2.1 Live Verification Module「在线验证模块」
在真实层级或真实路径验证修复效果。

### 12.2.2 Clean Environment Verification Module「洁净环境验证模块」
在相对干净环境验证可重复性。

### 12.2.3 History Replay Verification Module「历史路径回放验证模块」
复用历史问题路径确认问题不再出现。

### 12.2.4 Cross-Path Verification Module「交叉路径验证模块」
用其他入口或其他路径交叉确认。

### 12.2.5 Side-effect Check「副作用检查模块」
确认修复未明显破坏其他链路。

## 12.3 退出条件
### L1
- 当前目标路径通过
- 未发现明显新增问题

### L2 / L3
- 主路径通过
- 至少一个交叉路径通过
- 未发现明显副作用

---


# 十二点五、Optional Capability Modules「可选能力模块」

> 这四类模块不单独构成新的 workflow_state「流程状态」，但可以被 Step Orchestrator「步骤编排器」或 Step Module Group「步骤模块组」按需调用。

## 12.5.1 Development Module「开发模块」
- 负责 change implementation「变更实现」、build「构建」、artifact「产物」输出
- 通常支撑 Fixing Module，不直接等于修复完成

## 12.5.2 Installation Module「安装模块」
- 负责 prerequisite check「前置依赖检查」、安装执行、安装验证与安装回退
- 安装完成不等于部署完成

## 12.5.3 Deployment Module「部署模块」
- 负责 rollout strategy「发布策略」、deploy execution「部署执行」、health gate「健康门」与 rollback「回退」
- 不替代 Closing Module 做闭环判定

## 12.5.4 Debug Module「调试模块」
- 负责 low-impact probe「低副作用探针」、trace「链路捕获」、dump「状态转储」、safe instrumentation「安全插桩」
- 只增强证据与诊断，不直接等于修复

### 通用硬规则
- 单独调用时必须标记 `module_mode`
- 退出前必须经过 Record Gate「记录出口守卫」
- 不得自动推进 workflow_state

# 十三、Rollback Router「回退路由器」

Rollback Router 是共享控制模块，不单独代表一个 step。

职责：
- 判断当前失败应回退到哪个 step
- 记录失败原因
- 记录失败证据
- 记录重新进入条件

## 13.1 回退原则
- 回退必须显式记录
- 回退不是失败掩盖，而是流程控制
- 回退后必须写新的 Step Snapshot

### 建议路由
- reproducing 失败 → 回到 observing
- isolating 无法收敛 → 回到 reproducing
- attributing 竞争解释未排尽 → 回到 isolating
- fixing 风险过高或不可执行 → 回到 attributing
- verifying 失败 → 回到 fixing 或 reproducing
- closing 发现记录不完整 → 回到 verifying / fixing / attributing（按缺口来源决定）

---

# 十四、Closing Module「闭环模块」

Closing Module 只负责 Step 7，不负责长期规则执行。

## 14.1 目标
把本次 run 收束成长期可追踪资产。

## 14.2 三层落点
闭环必须同时评估并写入以下三层：
1. primary record db
2. running note / narrative
3. regression handoff「回归交接」

## 14.3 关键语义
- `closing`：流程态，表示正在做闭环收束
- `closed`：结果态，表示闭环已完成且资产已固定

## 14.4 L2 简化闭环
至少满足：
- running note 已完成收束
- 有可追踪结构化记录
- 已显式评估是否需要生成回归规则

## 14.5 L3 完整闭环
只有以下条件全部满足，才允许写 `closed`：
- 主记录库已写入
- Narrative 已写入
- Closing 输出已生成
- 三处落点均已回读验证
- 如评估结果为需要生成回归规则，则规则资产已创建并完成回读验证

## 14.6 Step 7 输出必须包含
- 主记录库路径
- 主过程文档路径
- workflow_state
- lifecycle_state
- 是否生成回归规则
- 回归规则位置（如有）
- closing summary「闭环摘要」

---

# 十五、Regression Asset Module「回归规则资产模块」

## 15.1 定义
回归规则是问题闭环后形成的长期防复发资产。

## 15.2 作用
- 不属于 Step 1~6 主流程
- 不替代 Step 6 验证
- 承接 Step 7 的长期输出

## 15.3 四层结构
- definition layer「定义层」
- execution layer「执行层」
- result layer「结果层」
- governance layer「治理层」

## 15.4 作用域
必须使用：
- `target`
- `project`
- `control_plane`
- `global`

## 15.5 最小规则结构
至少包含：
- `rule_uid`
- `source_issue_uid`
- `scope`
- `target`
- `trigger_condition`
- `expected_result`
- `verification_action`
- `executor_type`
- `severity`
- `status`
- `owner`
- `created_at`
- `last_verified_at`

## 15.6 规则生成原则
每个 issue 在 closing 阶段必须评估：

```text
该问题是否需要生成回归规则？
```

### 必须优先考虑生成规则的情况
- 可复现问题
- 配置类错误
- 状态污染问题
- 依赖问题
- Agent 行为异常
- 多次重复问题

---

# 十六、Regression Executor Module「回归规则执行器模块」

## 16.1 定位
属于 Harness 的长期运行子系统，不属于 Step 1~7 主流程本体。

## 16.2 最小闭环
第一版必须先跑通：

```text
read rule → run rule → save evidence → write result → fail handoff
```

## 16.3 组成模块
- Rule Loader「规则加载器」
- Rule Planner「规则规划器」
- Rule Dispatcher「规则分发器」
- Rule Workers「规则执行器集合」
- Evidence Collector「证据收集器」
- Result Writer「结果回写器」

## 16.4 fail handoff「失败交接」
当规则执行结果为 `fail`：
- 必须写 `regression_rule_runs`
- 必须保存 evidence pointer 与 artifact
- 必须优先通过 `source_issue_uid` 或 fingerprint「指纹」复用 issue
- 必须触发新的 v4 run 或 handoff record
- 不得默认直接自动修复

---

# 十七、Governance Module「治理模块」

## 17.1 作用
负责规范自身的版本、patch、反审与长期治理。

## 17.2 责任范围
- 版本入口与索引
- patch 生命周期
- 规范反审
- Cron 治理任务
- 模块变更历史

## 17.3 治理原则
- patch 不能长期替代正式规范
- 关键接口一旦稳定，必须回收进正式模块规范
- 周期性反审的是“规范缺口”，不是具体实例排障

---

# 十八、v4 推荐目录结构

```text
/harness-v4/
  00-entry/
    Harness v4 模块化控制规范（可执行版）.md

  01-kernel/
    kernel-spec.md

  02-controllers/
    execution-profile-controller.md
    rollback-router.md
    state-transition-guard.md

  03-record/
    record-and-evidence-module.md
    running-note-template.md
    step-snapshot-template.md
    checklist-template.md

  04-run-engine/
    observing-group.md
    reproducing-group.md
    isolating-group.md
    attributing-group.md
    fixing-group.md
    verifying-group.md
    development-module.md
    installation-module.md
    deployment-module.md
    debug-module.md

  05-closing/
    closing-module.md

  06-regression/
    regression-asset-module.md
    regression-executor-module.md

  07-governance/
    governance-module.md
    version-index.md
```

---

# 十九、v4 的最小数据库口径

> 这里给最小统一口径，不在本文件展开全部 DDL「数据定义语言」。

## 19.1 主记录库最少对象
- `runs`
- `issues`
- `issue_events`
- `checks`
- `actions`
- `artifacts`

## 19.2 回归规则最少对象
- `regression_rules`
- `regression_rule_runs`
- `regression_rule_artifacts`

## 19.3 字段口径要求
- 业务主标识统一用 `*_uid`
- 数据库内部主键统一用 `id`
- 不允许出现同义漂移字段，例如 `run_id` 兼作业务主标识

---

# 二十、模板

## 20.1 Execution Plan 模板

```md
# Execution Plan

- run_uid: <run_uid>
- issue_uid: <issue_uid>
- target: <target>
- execution_profile: <L1|L2|L3>
- current_step: <observing|reproducing|isolating|attributing|fixing|verifying|closing>
- objective: <本轮目标>
- hypothesis: <当前假设>
- constraints: <禁止事项 / 风险边界>
- evidence_needed: <至少需要哪些证据>
- stop_conditions: <何时必须暂停并回看>
- next_step: <下一步>
```

## 20.2 Step Snapshot 模板

```md
## Step Snapshot
- step: <step>
- objective: <本步目标>
- action_summary: <关键动作摘要>
- key_evidence: <关键证据摘要 + pointer>
- evidence_pointer: <证据指针>
- decision: <本步结论>
- next_or_rollback: <下一步或回退方向>
- readback_status: <回读状态>
```

## 20.3 Checklist 模板

```md
## Step Checklist
- [ ] 目标已明确
- [ ] 输入已确认
- [ ] 风险已评估
- [ ] 证据路径已确定
- [ ] 当前步输出已写入 running note
- [ ] 当前步结果已回读验证
- [ ] 退出条件已明确
- [ ] 回退条件已明确
```

## 20.4 Closing Summary 模板

```md
# Closing Summary
- run_uid: <run_uid>
- issue_uid: <issue_uid>
- workflow_state: closing
- lifecycle_state: closed
- primary_record_db: <path>
- narrative_path: <path>
- rule_required: <true|false>
- rule_reason: <原因>
- rule_location: <path or none>
- close_summary: <结论与剩余风险>
- readback_status: <回读状态>
```

---

# 二十一、v4 的强制规则（必须执行）

1. 任何正式 run 必须先生成 Execution Plan。
2. 任何 step 退出前必须通过 Record Gate。
3. module 可以独立调用，但独立调用不得自动推进 workflow_state。
4. Step Orchestrator 是唯一允许推进 workflow_state 的组件。
5. L1 / L2 / L3 是 execution profile，不是流程长度别名。
6. closing 是流程态，closed 是结果态。
7. 回归规则必须在 closing 阶段显式评估是否生成。
8. 回归执行器 fail 时必须 handoff，不得默认自动修复。
9. primary record db 仍是最终事实来源。
10. patch 不得长期替代正式模块规范。

---

# 二十二、推荐落地顺序

## Phase 1「阶段一」
先落地以下 4 个核心模块：
- Kernel Module
- Execution Profile Controller
- Record & Evidence Module
- Run Engine / Step Orchestrator

## Phase 2「阶段二」
补齐 6 组 step module：
- Observing
- Reproducing
- Isolating
- Attributing
- Fixing
- Verifying

## Phase 3「阶段三」
接入：
- Closing Module
- Regression Asset Module
- Regression Executor Module

## Phase 4「阶段四」
补齐 Governance Module 与规范反审 Cron。

---

# 二十三、最终结论

Harness v4 不再是“只能顺序阅读的一组步骤文档”，而是一套：

- 有统一内核口径
- 有执行档位控制
- 有横切记录模块
- 有可装配运行引擎
- 有闭环收束模块
- 有长期回归能力
- 有治理与反审能力

的模块化控制体系。

v4 的关键不是取消步骤，而是：

> **保留 workflow「流程」，模块化 capability「能力」，强化 record「记录」，分离 closing「闭环」与 closed「已完成」，让 Agent 能按模块装配执行。**
