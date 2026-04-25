# 04J. Debug Module「调试模块」

> 定位：为 Harness v4 提供低副作用 probe「探针」、trace「链路捕获」、dump「状态转储」、safe instrumentation「安全插桩」能力。
> 原则：Debug Module 负责增强证据与诊断，不直接等于修复，也不单独构成新的 workflow_state。

---

## 一、模块职责

Debug Module 负责：
- 日志探针
- 状态转储
- 链路捕获
- 污染扫描
- 假设探针
- 安全插桩

Debug Module 不负责：
- 直接宣称问题已修复
- 直接推进到下一个 workflow_state
- 替代 Step Orchestrator 做流程控制
- 绕过 Record Gate

---

## 二、模块清单

### 2.1 Log Probe Module「日志探针模块」
职责：
- 精确抓取相关日志片段
- 标记时间窗、来源与关键字段

### 2.2 State Dump Module「状态转储模块」
职责：
- 导出关键运行状态
- 记录状态快照指针

### 2.3 Trace Capture Module「链路捕获模块」
职责：
- 捕获调用路径、请求链路或执行轨迹
- 输出 trace pointer

### 2.4 Contamination Scan Module「污染扫描模块」
职责：
- 检查 memory / session / cache / process residue「残留」
- 记录污染风险

### 2.5 Hypothesis Probe Module「假设探针模块」
职责：
- 针对某个候选解释做最小副作用探测
- 输出支持 / 反驳证据

### 2.6 Safe Instrumentation Module「安全插桩模块」
职责：
- 在受控边界内增加最小监测点
- 记录插桩位置、持续时间、回收动作

---

## 三、进入条件

- 当前证据不足，或需要更细粒度观测
- 需要低副作用调试支持 Observing / Reproducing / Isolating / Attributing / Verifying
- execution_profile 允许当前级别的调试动作

---

## 四、退出条件

- 调试目标已明确
- 至少一个 debug evidence pointer 已绑定
- 调试结论已记录
- 插桩 / 转储 / 捕获的清理或退出条件已记录
- Record Gate 已通过

---

## 五、最小输出

- debug objective
- probe actions
- evidence pointers
- contamination / trace / dump summary
- debug conclusion
- next action or rollback

---

## 六、推荐 module_mode

- `probe`：低副作用探针、假设探测、临时状态观察
- `assist`：为 Observing / Reproducing / Isolating / Attributing / Verifying 提供证据增强
- `standalone_check`：独立调试核查，不推进 workflow_state

---

## 七、禁止事项

- 不得把调试输出直接当作正式事实而不做归一与校验
- 不得未说明影响范围就做高副作用插桩
- 不得把 Debug Module 结果直接冒充 Step 完成
- 不得保留未清理的长期插桩而不记录
