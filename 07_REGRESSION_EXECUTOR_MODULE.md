# 07. Regression Executor Module「回归执行器模块」

> 作用：把 active rule「激活规则」读出来、跑起来、收证据、写结果、失败时触发 handoff「移交」。
> 原则：执行器属于 Harness，但不等于 Harness；不替代主流程，不直接做复杂归因与自动修复。

---

## 一、系统边界

执行器负责：
- 读取 `status = active` 的 rule
- 生成执行计划
- 分发到对应 worker「执行单元」
- 收集证据
- 写回结果
- fail 时触发新的 run 或复用 issue

执行器不负责：
- 推进 Step 1~6 主流程
- 替代 Closing 判定
- 执行 `draft` / `disabled` / `superseded` 状态的规则
- 自动修改规范
- 高风险自动修复

---

## 二、模块结构

```text
Regression Executor
├── Rule Loader
├── Rule Planner
├── Rule Dispatcher
├── Rule Workers
├── Evidence Collector
└── Result Writer
```

---

## 三、状态机

必须使用：
- `queued`
- `planning`
- `running`
- `collecting_evidence`
- `writing_result`
- `done`
- `failed`

异常时：
- 超时
- 证据收集失败
- 结果写回失败
- handoff 写入失败

都必须进入 `failed`，不得静默成功。

---

## 四、fail 后标准路径

默认策略：

```text
rule fail
→ collect and bind evidence
→ write regression_rule_runs
→ save evidence/artifact
→ try source_issue_uid / fingerprint match
→ reuse issue or create new issue
→ trigger new run or write handoff
```

### 4.1 强制要求
- `evidence_pointer` 必写
- 结果写回必须在证据绑定之后
- 不得直接进入自动修复
- 不得只保留 pass / fail 而没有证据
- handoff 或新 run 触发结果必须可回读

### 4.2 顺序约束
fail path「失败路径」必须按以下顺序执行，禁止乱序：
1. 收集原始证据
2. 生成并绑定 `evidence_pointer`
3. 写 `regression_rule_runs`
4. 保存 `regression_rule_artifacts`（如有）
5. 执行 issue 复用判定
6. 触发 `new run` 或写 `handoff`

若任一步失败：
- 当前执行必须进入 `failed`
- 必须保留已完成步骤的可回读痕迹
- 不得把后续步骤标记为成功

### 4.3 issue 复用优先级
issue 复用必须按以下优先级判断：
1. `source_issue_uid` 精确命中
2. `fingerprint` 命中
3. 均未命中时，创建新 issue

禁止跳过以上优先级直接新建 issue。

### 4.4 new run / handoff 触发边界
- 若已有可复用 issue，默认触发 `new run` 并把本次 fail 绑定到该 issue
- 若无可复用 issue，创建新 issue 后触发 `new run`
- 若当前环境禁止立即起 run，则必须写 `handoff record`，不得静默结束
- `handoff record` 至少包含：`rule_uid`、`target`、`executed_at`、`result`、`evidence_pointer`、`issue_uid`（如有）、`next_action`

---

## 五、最小闭环目标

第一版执行器只要求跑通：

```text
rule active
→ executor run
→ evidence saved
→ result written
→ fail handoff
```
