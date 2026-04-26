# 10. Changelog v4.2.0「变更记录」

## 版本定位
- 本版本为 v4.1.1 后的 minor release「小版本」。
- 目标是补齐 Agent Harness 的上下文、工具、记忆与运行适配层。
- 不新增 workflow_state「流程状态」。
- 本版本不新增独立权限模块；工具侧仅保留副作用等级、失败处理与回读要求。

## 新增
- `02A_CONTEXT_CONTROLLER_MODULE.md`：定义上下文装配、裁剪、压缩恢复、Context Gate 与防漂移规则。
- `02B_TOOL_CONTRACT_REGISTRY.md`：定义工具分类、输入输出契约、副作用等级、失败处理与证据落点。
- `03A_MEMORY_LAYER_MODULE.md`：定义 episodic / semantic / procedural / regression 四类 memory 及写入、读取、冲突处理规则。
- `11_RUNTIME_ADAPTER_MODULE.md`：定义文件、命令、浏览器、数据、可观测性、CI / 发布等运行环境适配边界。

## 更新
- `README.md`：当前版本推进到 `v4.2.0`，新增模块说明。
- `00_INDEX.md`：更新阅读顺序、模块图、硬规则、目录清单与使用原则。
- `02_EXECUTION_PROFILE_CONTROLLER.md`：补充 Context / Tool / Memory / Runtime 的装配矩阵与边界。
- `03_RECORD_AND_EVIDENCE_MODULE.md`：补充横切模块记录要求。
- `04_RUN_ENGINE_ENTRY.md`：补充 Context Controller 与 Tool Contract Registry 在 Run Engine 中的协作边界。
- `08_GOVERNANCE_MODULE.md`：补充 v4.2 横切模块反审项。
- `09_TEMPLATES.md`：新增 Context Assembly、Tool Contract、Tool Call、Memory Entry 与 Runtime Adapter 模板。
- `00_ENTRYPOINT_SINGLE_FILE.md`：同步参考总版的 v4.2 模块图、章节与强制规则。

## 设计原则
- Context Controller 只控制上下文，不推进 workflow_state。
- Tool Contract Registry 只定义工具契约，不执行真实工具调用。
- Memory Layer 只沉淀已闭环经验，不替代当前证据。
- Runtime Adapter 只适配运行环境，不改变 Harness 状态机。
- Record Gate 仍是所有 step、capability module 与横切模块的统一退出门。
