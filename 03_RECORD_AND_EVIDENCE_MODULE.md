# 03. Record & Evidence Module「记录与证据模块」

> 作用：作为 Harness v4 的横切强制模块，负责在每一步完成时记录重点、绑定证据、回读结果。
> 核心规则：不记录，不算完成；不回读，不算退出。

---

## 一、模块定位

本模块不属于 Step 7 专属模块，而属于所有 run 过程的公共强制模块。

所有 Step Module「步骤模块」与 standalone module call「独立模块调用」结束时，都必须经过 Record Gate「记录出口守卫」。

这同样适用于：
- Context Controller Module
- Tool Contract Registry / Tool Call
- Development Module「开发模块」
- Installation Module「安装模块」
- Deployment Module「部署模块」
- Debug Module「调试模块」
- Memory Layer Module
- Runtime Adapter Module

---

## 二、四个子模块

### 2.1 Plan Writer「计划写入器」
负责写入：
- `run_uid`
- `issue_uid`
- `target`
- `execution_profile`
- `current_step`
- `objective`
- `hypothesis`
- `constraints`
- `evidence_needed`
- `stop_conditions`
- `next_step`

### 2.2 Step Snapshot Writer「步骤快照写入器」
每一步至少记录：
- `step`
- `objective`
- `action_summary`
- `key_evidence`
- `evidence_pointer`
- `decision`
- `next_or_rollback`
- `readback_status`

### 2.3 Checklist Writer「清单写入器」
至少维护：
- 当前步骤目标已明确
- 输入已确认
- 风险已评估
- 当前步输出已写入 running note
- 当前步结果已回读验证
- 退出条件已确认
- 回退条件已确认

### 2.4 Evidence Pointer Writer「证据指针写入器」
负责把以下内容转成 pointer「指针」或 artifact「产物」引用：
- 命令输出
- 日志片段
- 文件快照
- diff「差异」
- SQL 结果
- 截图摘要
- build output「构建输出」
- install log「安装日志」
- deploy log「部署日志」
- trace / dump / probe output「链路 / 转储 / 探针输出」

---

## 三、记录粒度

默认采用重点摘要，不采用全量流水。

### 3.1 必记内容
- 当前步骤目标
- 关键动作摘要
- 关键证据摘要与 pointer
- 本步结论
- 下一步或回退方向

### 3.2 默认不全文写入
- 大段命令输出
- 全量日志
- 大型 diff
- 完整截图内容
- 重复性中间过程

---

## 四、Record Gate「记录出口守卫」

任何步骤或模块要退出，必须同时满足：

1. Step Snapshot 已写入
2. Checklist 已更新
3. 至少一个 evidence pointer 已绑定
4. 当前结论已写入
5. next / rollback 已写入
6. 当前记录已回读成功

只要有一项未完成：
- 当前步骤不得退出
- workflow_state 不得推进
- standalone module call 不得标记完成

---

## 五、记录主文档规则

- 每个任务必须且仅有一个主过程文档
- 运行期名称为 running note
- 闭环后语义角色为 narrative
- 不允许再创建新的“主 narrative”替代它

### 5.1 capability record「能力调用记录」附加规则
当调用 Development / Installation / Deployment / Debug 模块时，Step Snapshot 中应额外记录：
- `module_name`
- `module_mode`
- `risk_note`
- `evidence_pointer`
- `artifact_or_log_pointer`

### 5.2 context / tool / memory / adapter record「横切模块记录」附加规则
当调用 Context Controller / Tool Contract Registry / Memory Layer / Runtime Adapter 时，应额外记录：
- `module_name`
- `assembly_mode` 或 `module_mode`
- `tool_uid` / `adapter_uid` / `memory_uid`，如适用
- `pointer_only_context`，如适用
- `artifact_or_log_pointer`
- `evidence_pointer`
- `readback_status`

---

## 六、最小输出模板

```md
## Step Snapshot
- step:
- module_name:
- module_mode:
- objective:
- action_summary:
- key_evidence:
- evidence_pointer:
- decision:
- next_or_rollback:
- readback_status:
```
