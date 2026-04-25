# 04B. Reproducing Modules「复现模块组」

> 对应 workflow_state = `reproducing`
> 目标：确认问题稳定存在，并识别复现条件与污染风险。

---

## 一、模块清单

### 1.1 Replay Runner「重放执行模块」
职责：
- 以相同输入重复执行
- 记录每次结果
- 计算复现成功率

### 1.2 Cross-path Reproducer「交叉路径复现模块」
职责：
- 通过不同入口、不同路径复现同一问题
- 对比各路径结果

### 1.3 Contamination Check「污染检查模块」
职责：
- 检查 memory / session / cache / 进程残留
- 标记污染风险
- 必要时要求清理后重跑

### 1.4 Repro Rate Evaluator「复现率评估模块」
职责：
- 计算复现成功率
- 判断问题是否稳定
- 判断是否满足进入下一步

---

## 二、退出条件

- 复现条件已明确
- 复现结果可追踪
- 污染风险已记录
- Record Gate 已通过

### 2.1 推荐门槛
- L1：单路径重复成立即可
- L2 / L3：至少双路径或交叉复现成立

---

## 三、最小输出

- reproduction log
- trigger conditions
- contamination note
- repro rate
- next step = `isolating`
