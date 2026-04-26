# 04X. Rollback Router Module「回退路由模块」

> 定位：Rollback Router 是 Run Engine 内的共享控制模块，不单独代表 workflow_state。
> 原则：回退是显式流程控制；所有回退决策必须可记录、可回读、可重新进入。

---

## 一、职责

Rollback Router 负责：

- 判断当前失败应回退到哪个 workflow_state
- 统一记录 failure_reason、failure_evidence 与 retry_condition
- 为 Step Orchestrator 提供唯一 rollback route
- 防止各 step module 自行定义互相冲突的回退路径

Rollback Router 不负责：
- 直接推进 workflow_state
- 直接执行修复、部署或清理动作
- 替代 Record Gate / Context Gate / Tool Contract

---

## 二、输入

每次进入 rollback 判定时，至少输入：

- `run_uid`
- `issue_uid`
- `current_workflow_state`
- `execution_profile`
- `failure_type`
- `failure_reason`
- `failure_evidence_pointer`
- `last_step_snapshot`
- `record_gate_result`
- `context_gate_result`（如适用）
- `tool_call_snapshot`（如适用）
- `rollback_hint`（如适用）

L3 下还必须输入：
- 对应 schema 校验结果（如该对象有 schema）
- 失败前最后一次可回读 artifact / log pointer
- contamination_assessment「污染评估」

---

## 三、全局回退表

| current_workflow_state | 触发条件 | rollback_to | 重新进入条件 |
|---|---|---|---|
| `observing` | bootstrap 失败、证据接入失败、issue matching 无法判定 | `observing` | 清理 half-initialized / orphan artifact，补足 evidence pointer，重新执行 Bootstrap 原子序列 |
| `reproducing` | 无法稳定复现、复现证据不足、复现路径污染 | `observing` | 补充事实、范围、环境状态与可复现输入 |
| `isolating` | 变量边界无法收敛、干扰变量未排除、隔离动作污染目标 | `reproducing` | 重新确认可复现路径与最小复现条件 |
| `attributing` | 竞争解释未排尽、候选根因证据不足、解释依赖未验证假设 | `isolating` | 补充分离变量、对照组或负证据 |
| `fixing` | 修复风险过高、修复不可执行、rollback_hint 缺失、变更验证前失败 | `attributing` | 重新确认根因、变更边界、回退路径与副作用等级 |
| `verifying` | 原问题仍存在、验证路径不可信、修复引入新异常 | `fixing` | 若修复假设仍成立则回到 fixing；若复现链路失真则回到 reproducing |
| `closing` | 记录不完整、证据不可回读、schema drift、回归资产缺失 | `verifying` | 按缺口来源可进一步回到 fixing / attributing；补齐三层落点后重新 closing |

---

## 四、决策规则

- 所有 step failure 在推进前必须经过 Rollback Router。
- Step module 可以提出 `rollback_hint`，但最终路由以本模块全局表为准。
- 若 `rollback_hint` 与全局回退表冲突，必须记录 `rollback_route_conflict`，并由 Step Orchestrator 选择更保守路线。
- 若 failure 同时命中多个路由，选择离当前 step 更早、证据补强更多的路线。
- 若失败由 Runtime Adapter、工具环境或外部系统造成，只能先记录为运行环境证据，不得直接写成目标系统根因。
- 若存在 contamination_assessment = `contaminated`，必须先回到能重新建立干净输入的最早 step。

---

## 五、最小输出

```md
## Rollback Route Decision
- run_uid:
- issue_uid:
- current_workflow_state:
- failure_type:
- failure_reason:
- failure_evidence_pointer:
- rollback_to:
- route_reason:
- retry_condition:
- cleanup_or_containment:
- next_or_rollback:
- readback_status:
```

---

## 六、退出条件

Rollback Router 退出前必须满足：

- 已选择唯一 `rollback_to`
- 已说明为什么不是继续推进
- 已记录失败证据 pointer
- 已记录重新进入条件
- 已写入 Step Snapshot 或 Capability Module Snapshot
- Record Gate 已通过

L3 下还必须满足：
- rollback route decision 已通过对应结构化记录或模板校验
- 相关 evidence pointer 已回读
- contamination_assessment 已写入
