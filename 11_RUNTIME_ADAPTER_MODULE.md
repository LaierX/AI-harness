# 11. Runtime Adapter Module「运行时适配器模块」

> 作用：把 Harness 规范映射到具体运行环境中的文件、命令、浏览器、数据库、日志、CI、部署与外部系统。
> 原则：Runtime Adapter 只适配执行环境，不改变 Harness 的状态机、记录口径与闭环规则。

---

## 一、定位

Runtime Adapter 是运行环境适配层，不构成新的 workflow_state「流程状态」。

它负责：
- 暴露当前环境可用能力
- 将 tool contract 映射到具体执行器
- 统一 artifact / evidence pointer 格式
- 抽象不同运行环境的路径、日志、截图、命令输出与外部链接
- 为 Tool Contract Registry 提供执行端信息

它不负责：
- 决定执行档位
- 推进 workflow_state
- 直接判定根因
- 替代工具契约
- 替代 Record Gate

---

## 二、适配器类型

### 2.1 File Adapter「文件适配器」
负责：
- 文件读取
- 文件快照
- diff 产物
- patch 产物
- 目录索引

### 2.2 Shell Adapter「命令适配器」
负责：
- 命令执行
- stdout / stderr 摘要
- exit code 记录
- command_output_pointer 生成

### 2.3 Browser / UI Adapter「浏览器与界面适配器」
负责：
- 页面导航
- 截图
- DOM / accessibility 摘要
- UI 操作证据

### 2.4 Data Adapter「数据适配器」
负责：
- 数据库只读查询
- 迁移状态检查
- 数据快照 pointer
- 查询结果摘要

### 2.5 Observability Adapter「可观测性适配器」
负责：
- logs「日志」
- metrics「指标」
- traces「链路」
- dumps「转储」

### 2.6 CI / Release Adapter「持续集成与发布适配器」
负责：
- build / test / package
- release status
- rollout / rollback 日志
- health gate 结果

### 2.7 Adapter Boundary「适配边界」

一个 adapter 只能描述当前运行环境能如何执行或回读，不得把运行环境限制上升为 Harness 全局限制。

当同一 tool contract 可映射到多个 adapter 时，必须由 Tool Contract Registry 或调用模块记录选择依据。

---

## 三、能力声明

每个 adapter 必须声明：
- `adapter_uid`
- `adapter_name`
- `adapter_type`
- `supported_tool_types`
- `pointer_scheme`
- `artifact_root`
- `environment_scope`
- `failure_surface`
- `readback_method`

---

## 四、Pointer Scheme「指针格式」

Runtime Adapter 必须输出可回读 pointer。

建议类型：
- `file://local-path-or-artifact-id`
- `log://source/query/time-range`
- `cmd://run_uid/command_uid`
- `db://connection/query_uid`
- `trace://trace_uid`
- `image://artifact_uid`
- `ci://pipeline/job_uid`
- `release://environment/release_uid`

pointer 可以是逻辑地址，不要求一定是 URL，但必须能被当前 Harness 环境回读。

### 4.1 最小 pointer 字段

每个 pointer 至少必须能解析出：
- `pointer_type`
- `pointer_value`
- `created_at`
- `producer_adapter_uid`
- `readback_method`

若 pointer 指向时间敏感数据，还必须记录：
- `time_range`
- `query_or_filter`
- `retention_note`

### 4.2 不稳定 pointer「易失指针」

以下 pointer 必须标记为 unstable：
- 临时日志窗口
- 短保留期 trace / metric 查询
- 临时文件
- 需要会话态才能访问的页面或截图
- 外部系统短期 artifact 链接

unstable pointer 用于 L2 / L3 时，必须尽快固化为 stable artifact pointer，否则不得作为长期闭环证据。

### 4.3 Stable Artifact Pointer「稳定产物指针」

stable artifact pointer 必须满足：
- 当前 Harness 环境可回读
- 过期条件明确
- 所属 run / issue 可追踪
- 内容摘要或 checksum 可记录，如适用

---

## 五、适配规则

### 5.1 执行前
必须确认：
- adapter 可用
- tool contract 已登记
- artifact_root 可写或可引用
- readback_method 可执行

### 5.2 执行后
必须产出：
- output_summary
- artifact_or_log_pointer
- evidence_pointer
- readback_status

执行后不得只返回自然语言摘要。若 adapter 无法生成 pointer，必须记录 `pointer_unavailable_reason`，并由调用模块决定是否允许继续。

### 5.3 失败时
必须产出：
- failure_surface
- partial_artifact，如存在
- cleanup_hint
- next_or_rollback

---

## 六、输出模板

```md
## Runtime Adapter Capability
- adapter_uid:
- adapter_name:
- adapter_type:
- supported_tool_types:
- pointer_scheme:
- artifact_root:
- environment_scope:
- failure_surface:
- readback_method:
```

```md
## Evidence Pointer
- pointer_type:
- pointer_value:
- created_at:
- producer_adapter_uid:
- readback_method:
- stability:
- time_range:
- query_or_filter:
- retention_note:
- checksum:
```

```md
## Runtime Adapter Snapshot
- run_uid:
- issue_uid:
- adapter_uid:
- adapter_name:
- tool_uid:
- action_summary:
- output_summary:
- artifact_or_log_pointer:
- evidence_pointer:
- pointer_unavailable_reason:
- failure_surface:
- cleanup_hint:
- readback_status:
```

---

## 七、禁止事项

- 不得让 adapter 改写 workflow_state
- 不得绕过 Tool Contract Registry 直接执行高副作用动作
- 不得生成不可回读 pointer
- 不得把运行环境失败伪装成目标系统结论
- 不得把 adapter 能力差异写成 Kernel 全局规则
