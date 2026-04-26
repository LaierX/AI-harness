# 02B. Tool Contract Registry「工具契约注册表」

> 作用：统一描述 Harness 可调用工具的输入、输出、副作用、失败处理、证据落点与回读要求。
> 原则：工具不是自由文本动作；每次工具调用都必须有契约、边界、产物与可审计记录。

---

## 一、定位

Tool Contract Registry 是横切 controller / asset「控制与资产」模块，不构成新的 workflow_state「流程状态」。

它负责：
- 登记工具能力与调用边界
- 定义工具输入输出 schema「结构」
- 定义副作用等级
- 定义失败、重试、超时与回滚提示
- 定义 artifact / evidence pointer 落点
- 为 Context Controller 提供可注入的工具摘要

它不负责：
- 直接选择 workflow_state
- 替代 Step Orchestrator
- 替代 Runtime Adapter 执行真实调用
- 替代 Record Gate

---

## 二、工具分类

### 2.1 `read_only`
只读工具，例如：
- 文件读取
- 日志查询
- 指标查询
- 数据库只读查询
- 页面截图

### 2.2 `local_write`
本地写入工具，例如：
- 文件修改
- patch 应用
- 本地构建产物生成
- 本地缓存更新

### 2.3 `environment_change`
环境变更工具，例如：
- 依赖安装
- 服务启动 / 停止
- 配置写入
- 数据迁移预演

### 2.4 `external_call`
外部调用工具，例如：
- 网络请求
- 第三方 API
- 远程仓库操作
- 外部系统查询

### 2.5 `release_action`
发布类工具，例如：
- deploy「部署」
- rollout「发布推进」
- traffic switch「切流量」
- rollback「回滚」

---

## 三、副作用等级

必须为每个工具声明 `side_effect_level`：

- `none`：无副作用
- `low`：本地或临时副作用，容易清理
- `medium`：可能影响环境状态，需要记录和回退说明
- `high`：可能影响运行服务、数据或外部系统

`side_effect_level = high` 的工具调用必须：
- 使用 L3 execution profile
- 明确 rollback_hint
- 明确 health_check 或 verification_action
- 产出 artifact_or_log_pointer

---

## 四、工具契约字段

每个工具契约至少包含：

- `tool_uid`
- `tool_name`
- `tool_type`
- `owner_module`
- `input_schema`
- `output_schema`
- `side_effect_level`
- `timeout_policy`
- `retry_policy`
- `failure_modes`
- `rollback_hint`
- `evidence_output`
- `artifact_output`
- `readback_method`

---

## 五、工具调用规则

每次正式工具调用必须：
- 绑定 `run_uid`
- 绑定当前 `workflow_state` 或 `module_mode`
- 引用一个已登记 tool contract
- 写入调用目标与输入摘要
- 保存输出摘要与 artifact pointer
- 保存失败模式与退出码，如适用
- 通过 Record Gate 回读

工具输出不得直接等于事实结论。  
事实结论必须由对应 step module 或 capability module 消化后写入 Step Snapshot。

---

## 六、失败处理

工具失败时必须记录：
- failure_type
- failure_scope
- retry_allowed
- retry_count
- partial_artifact
- rollback_or_cleanup_hint
- next_or_rollback

若失败发生在 L2 / L3：
- 不得静默忽略
- 不得直接推进 workflow_state
- 必须进入对应 step 的 failure handling 或 rollback router

---

## 七、输出模板

```md
## Tool Contract
- tool_uid:
- tool_name:
- tool_type:
- owner_module:
- input_schema:
- output_schema:
- side_effect_level:
- timeout_policy:
- retry_policy:
- failure_modes:
- rollback_hint:
- evidence_output:
- artifact_output:
- readback_method:
```

```md
## Tool Call Snapshot
- run_uid:
- issue_uid:
- workflow_state:
- module_name:
- module_mode:
- tool_uid:
- tool_name:
- input_summary:
- output_summary:
- side_effect_level:
- artifact_or_log_pointer:
- evidence_pointer:
- failure_type:
- retry_count:
- decision:
- readback_status:
```

---

## 八、禁止事项

- 不得调用未登记工具执行正式 L2 / L3 任务
- 不得把工具输出直接冒充 step 结论
- 不得丢弃失败工具调用的 partial artifact
- 不得在高副作用工具调用后跳过验证
- 不得用自然语言描述替代 tool contract 字段
