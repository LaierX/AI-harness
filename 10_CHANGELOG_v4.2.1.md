# 10. Changelog v4.2.1「变更记录」

## 版本定位
- 本版本为 v4.2.0 后的 patch release「补丁版本」。
- 目标是收紧 Context / Tool / Memory / Runtime 四类横切模块的边界、门控顺序与可回读要求。
- 不新增 workflow_state「流程状态」。
- 不新增独立权限模块。

## 更新
- `02A_CONTEXT_CONTROLLER_MODULE.md`：明确 Context Gate 与 Record Gate 的先后关系，补充 context_input / output / decision_scope 字段。
- `02B_TOOL_CONTRACT_REGISTRY.md`：收紧 tool_type 与 side_effect_level 的关系，补充正式调用前置条件与高副作用工具调用约束。
- `03A_MEMORY_LAYER_MODULE.md`：补充 memory 写入触发、读取注入等级、review cadence 与 Memory Write Candidate 模板。
- `11_RUNTIME_ADAPTER_MODULE.md`：补充 pointer 最小字段、稳定性等级与回读失败处理。
- `03_RECORD_AND_EVIDENCE_MODULE.md`：明确 Context Gate 是前置门，Record Gate 是出口门。
- `04_RUN_ENGINE_ENTRY.md`：补充工具调用链路顺序。
- `09_TEMPLATES.md`：同步 Context / Tool / Memory / Runtime 的新增字段。
- `README.md` 与 `00_INDEX.md`：版本推进到 `v4.2.1`，同步目录清单与硬规则。
- `00_ENTRYPOINT_SINGLE_FILE.md`：同步参考总版中的 v4.2.1 关键约束。

## 设计原则
- Context Gate 解决“能不能带着这组上下文继续判断或调用工具”。
- Record Gate 解决“当前 step / module 能不能退出”。
- Tool Contract 只定义契约，不替代 Runtime Adapter 执行真实动作。
- Memory 只沉淀已闭环且已回读的经验，不沉淀未验证假设。
- Runtime pointer 必须可定位、可回读、可复核。
