# 01. Kernel Module「内核模块」

> 作用：定义全局唯一、不可漂移的对象边界、权威顺序、状态口径、命名口径。
> 原则：凡属于“全系统必须一致”的内容，只能放在本模块。

---

## 一、对象边界

### 1.1 Harness
Harness 是统一控制与决策中枢，负责对 Target System「被管控对象」进行观察、复现、隔离、归因、修复、验证、闭环与长期治理。

### 1.2 Target System「被管控对象」
Target System 指被 Harness 监督、排障、验证、优化或治理的任意对象，包括但不限于：
- 服务
- Agent「智能体」
- 模块
- 子系统
- profile「配置实例」
- 实例
- 外部依赖

### 1.3 Control Root「控制根」
承载控制体系总入口、全局装配、路由与控制平面状态的目录或目录树根。

### 1.4 Target Root「目标根」
某个被管控对象、角色、profile、实例或服务的根目录。

### 1.5 Self-governance「自监督」
当 Harness 监督控制根本身时，必须显式标记为 self-governance；不得与普通 target 监督混写。

---

## 二、权威顺序

统一权威顺序如下：

1. primary record db「主记录库」
2. running note / narrative「过程主文档」
3. runtime logs / temporary outputs「运行时日志与临时输出」

若三者不一致：
- 必须以 primary record db 为准
- 必须记录差异
- 差异必须可回读

---

## 三、统一命名口径

### 3.1 业务主标识
- `run_uid`
- `issue_uid`
- `rule_uid`
- `source_issue_uid`

### 3.2 数据库内部主键
- `id`

### 3.3 禁止事项
- 不允许用 `run_id` 表示业务主标识
- 不允许用 `rule_id` 表示业务主标识
- 在规则语境中，如表示来源问题，必须使用 `source_issue_uid`

---

## 四、统一状态口径

### 4.1 workflow_state「流程状态」
必须使用：
- `observing`
- `reproducing`
- `isolating`
- `attributing`
- `fixing`
- `verifying`
- `closing`

### 4.2 lifecycle_state「生命周期结果态」
建议使用：
- `open`
- `investigating`
- `fixing`
- `verifying`
- `closed`

说明：
- `closing` 是流程态
- `closed` 是结果态
- 不得把 `closed` 当作 Step 名称

---

## 五、统一结果口径

### 5.1 checks.result
只允许：
- `pass`
- `fail`
- `unknown`

### 5.2 regression_rule_runs.result
只允许：
- `pass`
- `fail`
- `error`
- `skipped`

禁止将两者合并为同一字段或同一枚举。

---

## 六、统一第一性原则

- 先确认问题存在，再确认问题稳定，再确认问题独立，最后确认解释唯一。
- 日志不是事实，事实必须由独立证据集合支撑。
- 不能跳步、不能伪闭环、不能用单模块成功冒充完整 run「运行」成功。
