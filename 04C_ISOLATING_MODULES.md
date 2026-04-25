# 04C. Isolating Modules「隔离模块组」

> 对应 workflow_state = `isolating`
> 目标：缩小问题边界，控制变量，识别最小差异集。

---

## 一、模块清单

### 1.1 Variable Control Module「变量控制模块」
职责：
- 一次只改一个变量
- 固定其他输入、路径与上下文

### 1.2 Minimal Difference Finder「最小差异发现模块」
职责：
- 找出最小差异变量集
- 将可疑变量压缩到最小集合

### 1.3 Interference Elimination Module「干扰排除模块」
职责：
- 排除无关变量
- 标记仍未排除的干扰项

### 1.4 Boundary Convergence Evaluator「边界收敛评估模块」
职责：
- 判断边界是否收敛
- 判断是否存在可重复影响变量

---

## 二、退出条件

- 变量边界已明显收敛
- 已排除主要干扰变量
- 至少存在一个可重复影响变量
- Record Gate 已通过

---

## 三、最小输出

- candidate variable set
- excluded variables
- current minimal boundary
- next step = `attributing`
