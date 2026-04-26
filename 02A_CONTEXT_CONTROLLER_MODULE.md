# 02A. Context Controller Module「上下文控制器模块」

> 作用：负责每次 run、step 切换、standalone module call、上下文压缩与恢复时的上下文装配、裁剪、回读与防漂移。
> 原则：上下文不是越多越好；进入模型的内容必须有来源、优先级、时效性与证据边界。

---

## 一、定位

Context Controller 是横切 controller「控制器」，不构成新的 workflow_state「流程状态」。

它负责：
- 决定本次调用应注入哪些上下文
- 决定哪些信息只保留 pointer「指针」而不全文注入
- 控制上下文压缩、恢复与摘要回读
- 防止旧结论、过期假设、污染记忆进入当前决策
- 将上下文装配结果写入 Record & Evidence Module

它不负责：
- 推进 workflow_state
- 直接执行工具
- 直接生成 regression rule
- 替代 Record Gate

---

## 二、上下文来源层级

### 2.1 必须优先注入
- 当前 `execution_profile`
- 当前 `workflow_state`
- 当前 step objective「步骤目标」
- 当前 stop_conditions「停止条件」
- 最近一次通过回读的 Step Snapshot
- 本轮需要验证的 active hypothesis「活动假设」
- 与当前 step 直接相关的 evidence pointer

### 2.2 条件注入
- 历史 narrative 摘要
- regression rule 摘要
- long-term memory「长期记忆」
- tool contract「工具契约」
- runtime adapter「运行适配器」能力说明
- 相关代码 / 配置 / 日志片段

### 2.3 默认不全文注入
- 大段日志
- 大型 diff
- 完整数据库导出
- 长工具输出
- 过期 plan
- 未回读的中间推测

以上内容应以 pointer / artifact 方式挂载，只有在当前 step 必须使用时才局部展开。

---

## 三、上下文装配优先级

上下文冲突时，按以下顺序裁决：

1. primary record db「主记录库」
2. 当前已回读 Step Snapshot
3. 当前 running note / narrative
4. 当前工具输出与 artifact
5. long-term memory
6. 未验证的人类备注或模型推测

若 long-term memory 与当前证据冲突：
- 必须以当前证据为准
- 必须记录 memory_conflict「记忆冲突」
- 不得直接用历史记忆覆盖当前事实

---

## 四、上下文装配模式

### 4.1 `run_bootstrap`
用于 run 初始化。

必须装配：
- Kernel 口径
- execution profile 判定
- 任务目标
- 初始 evidence pointer
- 约束与停止条件

### 4.2 `step_transition`
用于 workflow_state 推进或回退。

必须装配：
- 上一步 Step Snapshot
- 上一步 readback_status
- 当前 step 进入条件
- 当前 step evidence_needed
- next / rollback 方向

### 4.3 `module_call`
用于 standalone module call 或 capability module call。

必须装配：
- `module_name`
- `module_mode`
- 调用目标
- 相关 tool contract
- 预期 artifact / evidence pointer

### 4.4 `compression_recovery`
用于上下文压缩、恢复、长任务续跑。

必须装配：
- 最近一次可信 summary
- 未完成 checklist
- open hypothesis
- open risk / blocker
- 最近一次 Record Gate 结果

---

## 五、Context Gate「上下文出口守卫」

每次上下文装配完成后，必须通过 Context Gate。

必须同时满足：
- 当前 objective 已明确
- 当前 workflow_state / module_mode 已明确
- 注入内容均有来源或 pointer
- 过期假设已标记
- 未验证内容已标记为 tentative「暂定」
- 与当前目标无关的大段材料未全文注入
- 上下文装配结果已写入记录

不满足任意一项：
- 不得进入高风险工具调用
- 不得推进 workflow_state
- 必须回到 Context Controller 重新装配

---

## 六、输出模板

```md
## Context Assembly Snapshot
- run_uid:
- issue_uid:
- assembly_mode:
- workflow_state:
- module_name:
- module_mode:
- objective:
- injected_context:
- pointer_only_context:
- excluded_context:
- stale_or_tentative_items:
- memory_conflicts:
- context_gate_result:
- readback_status:
```

---

## 七、禁止事项

- 不得把未回读摘要当作权威上下文
- 不得把历史 memory 当作当前事实
- 不得在上下文中混入无来源结论
- 不得因为上下文压缩丢失 open checklist / rollback 条件
- 不得用全文日志挤占当前 step 的关键证据
