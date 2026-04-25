# 06. Regression Asset Module「回归资产模块」

> 作用：定义回归规则的结构、作用域、执行结果与治理属性。
> 原则：本模块只定义 rule「规则」资产本体，不负责执行实现；是否需要生成规则，由 Closing Module 判定。

---

## 一、系统定位

Regression Rule「回归规则」是问题闭环后的长期资产，用于防止相同问题在未来再次发生。

它不是当前 run 内的回退规则，也不是 Step 1~6 的过程检查结果。

Regression Asset Module 负责：
- 规则资产定义
- 规则最小字段要求
- 规则结构化落库口径
- 规则 scope「作用域」
- 规则版本与治理属性

Regression Asset Module 不负责：
- 判定某个问题是否必须生成规则
- 判定闭环是否成立
- 执行规则本体
- 推进主流程状态

---

## 二、与 Closing 的接口边界

### 2.1 判定归 Closing，资产归 06
- `05_CLOSING_MODULE.md` 负责：
  - 判定是否需要规则
  - 输出 `rule_required`
  - 交付规则创建请求
- `06_REGRESSION_ASSET_MODULE.md` 负责：
  - 定义规则结构
  - 写入规则资产
  - 维护规则 schema
  - 维护规则治理属性

### 2.2 资产创建输入
若 Closing 判定 `rule_required = true`，则传入至少以下字段：
- `source_issue_uid`
- `target`
- `rule_scope`
- `rule_reason`
- `owner`
- `trigger_condition`
- `expected_result`
- `verification_action`

---

## 三、四层结构

### 3.1 Definition Layer「定义层」
描述规则是什么：
- `rule_uid`
- `rule_name`
- `scope`
- `target`
- `source_issue_uid`
- `trigger_condition`
- `expected_result`
- `verification_action`
- `severity`
- `status`
- `owner`

### 3.2 Execution Layer「执行层」
描述规则如何执行：
- `executor_type`
- `executor_config`
- `schedule`
- `timeout_sec`
- `retry_policy`
- `cooldown_sec`

### 3.3 Result Layer「结果层」
描述规则跑出了什么：
- `executed_at`
- `result`
- `evidence_pointer`
- `summary`
- `next_action`

### 3.4 Governance Layer「治理层」
描述规则如何演进：
- `version`
- `supersedes_rule_uid`
- `disabled_reason`
- `false_positive_count`
- `last_verified_at`
- `valid_from / valid_to`

---

## 四、scope「作用域」

必须使用以下枚举之一：
- `target`
- `project`
- `control_plane`
- `global`

---

## 五、status「规则状态」

必须使用以下枚举之一：
- `draft`
- `active`
- `disabled`
- `superseded`

说明：
- `draft` 表示规则资产已创建但尚未进入自动执行范围。
- `active` 表示规则可被 Regression Executor 读取与执行。
- `disabled` 表示规则被暂停，必须写明 `disabled_reason`。
- `superseded` 表示规则已被其他 `rule_uid` 替代，必须写明 `supersedes_rule_uid` 或替代关系。

Regression Executor 默认只读取 `active` 状态的规则。

---

## 六、生成时机

每个问题在 Closing Module 中都必须评估：

```text
该问题是否需要生成 regression rule？
```

本模块不做该判定，只承接已判定为 `rule_required = true` 的创建请求。

推荐必须生成的情况：
- 可复现问题
- 配置类错误
- 状态污染问题
- 依赖问题
- Agent 行为异常
- 多次重复问题

---

## 七、最小字段要求

### regression_rules
- `rule_uid`
- `rule_name`
- `scope`
- `target`
- `source_issue_uid`
- `trigger_condition`
- `expected_result`
- `verification_action`
- `executor_type`
- `severity`
- `status`
- `created_at`
- `updated_at`

### regression_rule_runs
- `rule_uid`
- `run_uid`
- `target`
- `executed_at`
- `result`
- `evidence_pointer`
- `summary`
- `next_action`

### regression_rule_artifacts
- `rule_uid`
- `run_uid`
- `kind`
- `path`
- `checksum`
- `created_at`

---

## 八、结构化落库职责

规则资产层必须负责：
- 生成或校验 `rule_uid`
- 将规则写入结构化记录
- 维护规则字段口径一致性
- 维护版本与 supersede「替代」关系
- 返回规则物理落点与写入结果

Closing Module 不得越权定义以上结构。

---

## 九、禁止事项

- 不得把 `run_id` 混入规则资产层作为业务主标识
- 不得把 `checks.result` 与 `regression_rule_runs.result` 混为一体
- 不得让规则资产只停留在 narrative 而没有结构化记录
- 不得由 Regression Asset Module 单独判定闭环是否成立
