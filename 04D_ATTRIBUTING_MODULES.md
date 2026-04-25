# 04D. Attributing Modules「归因模块组」

> 对应 workflow_state = `attributing`
> 目标：找到当前问题边界内唯一成立的解释。

---

## 一、模块清单

### 1.1 Hypothesis Registry「假设登记模块」
职责：
- 列出候选解释
- 为每个假设绑定需要验证的条件

### 1.2 Causal Test Module「因果测试模块」
职责：
- 改变关键变量，观察问题消失与恢复
- 验证因果关系

### 1.3 Alternative Rejection Module「替代解释排除模块」
职责：
- 排除竞争解释
- 记录被排除原因

### 1.4 Root Cause Selector「根因选择模块」
职责：
- 确定唯一成立的解释
- 生成 root cause「根因」结论

---

## 二、退出条件

- 候选解释收敛到一个
- 至少两个证据来源支持同一解释
- 竞争解释已被排除或记录无法排除原因
- Record Gate 已通过

---

## 三、最小输出

- root cause
- supporting evidence
- rejected alternatives
- next step = `fixing`
