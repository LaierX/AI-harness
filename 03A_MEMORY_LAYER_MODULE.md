# 03A. Memory Layer Module「记忆层模块」

> 作用：把一次 run 的经验、长期事实、操作程序与防复发规则分层沉淀，并在后续上下文装配时可控复用。
> 原则：memory「记忆」不是证据本身；记忆只能辅助决策，不能覆盖当前证据与主记录库。

---

## 一、定位

Memory Layer 是长期资产模块，不构成新的 workflow_state「流程状态」。

它负责：
- 定义 memory 的类型、写入条件与读取边界
- 从 closed run 中提炼可复用经验
- 为 Context Controller 提供可注入摘要
- 标记 memory 的来源、时效性、置信度与废弃条件
- 发现记忆与当前证据冲突时触发记录

它不负责：
- 替代 primary record db
- 替代 running note / narrative
- 替代 Regression Asset Module
- 自动推进 workflow_state

---

## 二、记忆分层

### 2.1 Episodic Memory「事件记忆」
记录某一次 run 发生过什么。

来源：
- closed run
- Step Snapshot
- Closing Summary

用途：
- 帮助理解历史上下文
- 支撑相似问题检索

### 2.2 Semantic Memory「语义记忆」
记录长期稳定事实。

示例：
- 系统边界
- 模块职责
- 已确认的架构约束
- 用户偏好或团队约定

用途：
- 辅助 Context Controller 装配背景
- 降低重复解释成本

### 2.3 Procedural Memory「程序记忆」
记录“类似问题应该怎么处理”。

示例：
- 排障路径
- 验证顺序
- 常用工具组合
- 回退检查清单

用途：
- 为 Execution Profile Controller 与 Run Engine 提供建议
- 不得替代当前 evidence_needed

### 2.4 Regression Memory「回归记忆」
记录防复发资产的摘要。

来源：
- Regression Asset Module
- Regression Executor Module

用途：
- 提醒当前问题是否已有 active rule
- 提供历史 fail / pass 摘要

Regression Memory 不替代 regression rule 本体。

---

## 三、写入条件

### 3.1 可写入 memory
满足以下条件才允许写入：
- 对应 run 已完成 Closing
- lifecycle_state 已标记为 `closed`
- 关键结论已回读
- 来源 pointer 明确
- memory 类型已明确
- 置信度可说明
- 废弃条件或复审条件明确
- 与当前 regression rule / governance 资产的关系已说明，如适用

### 3.2 写入触发点

长期 memory 只能在以下触发点写入：
- Closing Module 完成后
- Governance Module 反审确认后
- Regression Executor 产生稳定的长期结果后

在 Observing / Reproducing / Isolating / Attributing / Fixing / Verifying 过程中，只允许写入临时 note 或 Step Snapshot，不得直接写入长期 memory。

### 3.3 不得写入 memory
以下内容不得沉淀为长期 memory：
- 未验证假设
- 临时猜测
- 无来源结论
- 已被当前 run 推翻的历史判断
- 含敏感或不可复用的一次性内容

---

## 四、读取规则

读取 memory 时必须输出：
- memory_uid
- memory_type
- status
- source_run_uid
- source_issue_uid
- source_pointer
- confidence
- freshness
- applicability
- decision_impact

若 memory 仅为低置信参考：
- 必须标记为 tentative
- 不得进入当前结论字段

若 memory 状态为 `needs_review` 或 `deprecated`：
- 默认不得注入为 active context
- 如必须引用，只能作为历史冲突或反审材料使用

---

## 五、冲突处理

当 memory 与当前证据冲突时：
- 当前证据优先
- 记录 `memory_conflict`
- 标记 memory 为 `needs_review`
- 若冲突影响长期规则，交由 Governance Module 反审

---

## 六、状态枚举

memory status「记忆状态」建议使用：
- `active`
- `tentative`
- `needs_review`
- `deprecated`

### 6.1 置信度口径

memory confidence「记忆置信度」建议使用：
- `high`：来自已闭环 run，且有多证据支撑
- `medium`：来自已闭环 run，但适用范围有限
- `low`：仅可作为参考，必须标记 tentative

### 6.2 新鲜度口径

memory freshness「记忆新鲜度」建议使用：
- `current`：仍与当前系统状态一致
- `aging`：可能受版本、配置或环境变化影响
- `stale`：已过期或必须复审

---

## 七、输出模板

```md
## Memory Entry
- memory_uid:
- memory_type:
- status:
- source_run_uid:
- source_issue_uid:
- source_pointer:
- summary:
- applicability:
- confidence:
- freshness:
- invalidation_condition:
- owner:
- created_at:
- updated_at:
```

```md
## Memory Read Snapshot
- run_uid:
- issue_uid:
- requested_context:
- memory_used:
- memory_rejected:
- memory_conflicts:
- decision_impact:
- readback_status:
```

---

## 八、禁止事项

- 不得把 memory 当作 primary record db
- 不得把 tentative memory 注入为事实
- 不得从未闭环 run 直接沉淀长期记忆
- 不得用 memory 跳过当前复现、隔离或验证
- 不得让 regression memory 替代 regression rule 执行结果
