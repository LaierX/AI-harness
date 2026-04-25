# 04A. Observing Modules「观察模块组」

> 对应 workflow_state = `observing`
> 目标：建立客观事实，完成任务初始化，形成初步边界。

---

## 一、模块清单

### 1.1 Bootstrap Module「引导初始化模块」
职责：
- 生成 `run_uid / issue_uid`
- 创建主过程文档
- 写入文档首部元数据
- 初始化最小记录（L3 强制）

### 1.2 Evidence Intake Module「证据接入模块」
职责：
- 收集日志、状态、指标、配置、文档
- 标记证据来源
- 建立初始证据集合

### 1.3 Fact Normalize Module「事实归一模块」
职责：
- 将观测转换为事实清单
- 将日志描述转换为可验证陈述
- 去除情绪化或推测性表述

### 1.4 Scope Seed Module「范围种子模块」
职责：
- 产出初步异常范围
- 明确当前 target
- 明确本轮 objective「目标」

---

## 二、Bootstrap 原子序列「atomic bootstrap sequence」

### 2.1 L3 强制原子初始化顺序
在 L3 下，Bootstrap Module 必须按以下顺序一次性完成，不得乱序：
1. 生成 `run_uid / issue_uid`（仅内存态）
2. 创建主过程文档
3. 写入文档首部元数据
4. 初始化最小记录
5. 回读主过程文档
6. 回读最小记录

仅当以上 1~6 全部成功，任务才算正式进入 `observing`。

### 2.2 失败即停
若原子序列任一步失败：
- 不得进入后续模块
- 不得进入 `reproducing`
- 必须记录 `bootstrap_failed`
- 必须进入暂停或失败处理

### 2.3 禁止重复初始化
同一 `run_uid` 在同一轮任务中不得重复执行 Bootstrap Module。
若检测到重复初始化请求，必须：
- 拒绝重复执行
- 记录 `bootstrap_duplicate_attempt`
- 保留第一次初始化结果作为权威结果

### 2.4 半成品与 orphan「孤儿态」处理
若初始化只完成部分步骤，则必须：
- 标记为 `orphan artifact` 或 `half-initialized state`
- 记录当前已落地对象
- 记录未完成步骤
- 记录清理或回收动作

禁止把半成品当成正式进入 `observing` 的依据。

---

## 三、退出条件

- 问题可被客观复述
- 至少形成一组有效事实
- 当前目标已明确
- Record Gate 已通过

### 3.1 推荐证据下限
- L1：至少 1 条有效证据
- L2 / L3：至少 2 条独立证据

---

## 四、最小输出

- facts
- evidence list
- initial scope
- bootstrap result
- next step = `reproducing`
