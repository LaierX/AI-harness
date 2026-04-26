# 05. Closing Module「闭环模块」

> 作用：负责 Step 7 的收束、三层落点、闭环判定与长期资产交付。
> 原则：Closing Module 负责收束，不替代前 1~6 步记录；前 1~6 的过程记录必须由 Record Module 持续写入。

---

## 一、定位

`closing` 是 workflow_state「流程状态」，表示进入闭环阶段。  
`closed` 是 lifecycle_state「生命周期结果态」，表示对象已完成并冻结。

因此：
- Step 7 保持为 `closing`
- 当闭环判定完成后，issue 才能标记为 `closed`

Closing Module 只负责：
- 闭环门控
- 三层落点收束
- 是否需要生成 regression rule「回归规则」的判定
- 规则交付结果的回读确认

Closing Module 不负责：
- 定义 regression rule 的 schema「结构定义」
- 维护规则资产表结构
- 定义规则版本治理字段
- 执行规则本体

以上职责统一由 `06_REGRESSION_ASSET_MODULE.md` 与 `07_REGRESSION_EXECUTOR_MODULE.md` 承接。

---

## 二、三层落点

闭环必须同步评估并写入以下落点：

1. primary record db「主记录库」
2. running note / narrative「主过程文档 / 叙事文档」
3. regression / monitoring assets「回归 / 监控资产」，如适用

同时应维护一份 human-readable mirror「人类可读镜像」：
- 默认落点：`/Users/laier/Documents/obsidian/Laier/00-AI/项目/`
- 用途：方便人工快速查看当前项目、问题与闭环摘要
- 约束：镜像不替代以上三层正式落点，也不作为 evidence pointer 的唯一来源

---

## 三、闭环判定

### 3.1 L2 简化闭环
至少满足：
- running note 已完成收束
- 有可追踪的结构化记录
- 已显式评估是否需要生成 regression rule
- 已写入或记录 human-readable mirror 的补写计划

### 3.2 L3 完整闭环
必须全部满足：
- 主记录已写入
- narrative 已写入
- 三处落点均已回读验证
- human-readable mirror 已写入，并记录路径
- 关闭输出已生成
- lifecycle_state 已可标记为 `closed`

若本次问题经 Closing 判定为需要生成 regression rule，则还必须满足：
- 规则资产已创建
- 规则归属已明确
- 规则与 `source_issue_uid` 已建立关联
- 规则记录已回读

---

## 四、规则判定职责

### 4.1 Closing 只做判定，不定义资产结构
Closing Module 在 Step 7 中只回答以下问题：

```text
该问题是否需要生成 regression rule？
```

判定输出必须至少包含：
- `rule_required` = true / false
- `rule_reason`
- `rule_scope`（如需要）
- `rule_owner`（如需要）
- `rule_handoff_target` = `06_REGRESSION_ASSET_MODULE`

### 4.2 若判定为需要生成规则
Closing Module 必须触发规则资产交付，并等待以下结果返回：
- `rule_uid`
- 规则物理落点
- 结构化记录写入结果
- 回读结果

在以上结果全部返回前，不得宣称完整闭环完成。

---

## 五、Closing 输出

闭环输出至少包含：
- 主记录库路径
- 主过程文档路径
- 人类可读镜像路径
- 当前 workflow_state
- lifecycle_state
- `rule_required`
- 规则位置（如有）
- 关闭摘要

---

## 六、禁止事项

- 不得把 Step 7 当作前 1~6 的唯一记录阶段
- 不得只写 summary 而不写主记录
- 不得未回读即宣称闭环完成
- 不得把 `closing` 直接改成 `closed` 作为 Step 名称
- 不得在 Closing Module 中维护规则 schema 或规则版本治理定义
