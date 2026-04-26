# 08. Governance Module「治理模块」

> 作用：负责版本索引、patch 治理、规范反审、Cron 任务、长期改进。
> 原则：治理模块不直接替代运行引擎；它只治理规范与长期系统质量。

---

## 一、职责范围

Governance Module 负责：

- 版本索引
- 规范入口维护
- patch 生命周期管理
- 规范反审
- 周期性 Cron 治理任务
- 规范缺口识别
- v4.x 迭代建议

---

## 二、版本治理规则

- 只有主入口 + 正式模块文件可以作为当前执行依据
- patch 仅用于合并参考，不应长期承担主规范职责
- 若 patch 内含关键约束，必须尽快吸收到正式模块

---

## 三、反审任务

建议周期性执行以下任务：
- 检查字段命名漂移
- 检查流程态与结果态是否混用
- 检查 Record Gate 是否被绕过
- 检查 regression rule 是否只创建未执行
- 检查 narrative 与 db 是否一致
- 检查 context assembly 是否混入过期假设或无来源结论
- 检查 tool call 是否缺少 tool contract / artifact pointer / readback
- 检查 memory 是否从未闭环 run 写入，或与当前证据冲突后未标记
- 检查 runtime adapter 是否生成不可回读 pointer

执行反审时，建议使用 `09_TEMPLATES.md` 中的 Governance Review Checklist「治理反审清单」模板。

---

## 四、建议输出

每次正式反审至少输出：
- 本轮证据范围
- 暴露出的规范缺口
- 为什么它属于规范问题而不是单次实现失误
- 建议进入的 v4.x 版本
- 建议补强位置

### 4.1 v4.2 横切模块反审补充

涉及 Context / Tool / Memory / Runtime 的反审还应输出：
- context_gap
- tool_contract_gap
- memory_gap
- runtime_adapter_gap

---

## 五、禁止事项

- 不得直接把分析结果伪装成“规范已正式更新”
- 不得让 patch 长期替代正式模块
- 不得把某次偶发实现错误直接上升为规范缺陷
