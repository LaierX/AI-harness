# 04E. Fixing Modules「修复模块组」

> 对应 workflow_state = `fixing`
> 目标：执行可解释、可追踪、可回滚的修复动作。

---

## 一、模块清单

### 1.1 Fix Strategy Planner「修复策略规划模块」
职责：
- 设计修复路径
- 评估影响面
- 识别副作用

### 1.2 Fix Type Classifier「修复类型分类模块」
职责：
- 标记为 `root_fix` 或 `defensive_fix`

### 1.3 Fix Executor「修复执行模块」
职责：
- 执行修复动作
- 记录动作与产物

### 1.4 Rollback Risk Evaluator「回滚风险评估模块」
职责：
- 判断是否可安全回滚
- 识别残留风险

---

## 二、退出条件

- 修复动作已完成
- 修复动作已记录
- 副作用与回滚风险已评估
- Record Gate 已通过

---

## 三、最小输出

- fix plan
- action log
- fix type
- rollback risk note
- next step = `verifying`
