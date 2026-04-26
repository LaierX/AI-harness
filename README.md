# Harness v4 模块化规范套件 v4.4.0

本目录为 Harness v4 的模块化规范套件。

## 执行入口
- `00_INDEX.md`

## 总版 / 参考版
- `00_ENTRYPOINT_SINGLE_FILE.md`（仅用于整体对照与阅读，不作为执行依据）

## 新增能力模块
- `02A_CONTEXT_CONTROLLER_MODULE.md`
- `02B_TOOL_CONTRACT_REGISTRY.md`
- `03A_MEMORY_LAYER_MODULE.md`
- `04G_DEVELOPMENT_MODULE.md`
- `04H_INSTALLATION_MODULE.md`
- `04I_DEPLOYMENT_MODULE.md`
- `04J_DEBUG_MODULE.md`
- `11_RUNTIME_ADAPTER_MODULE.md`
- `12_SCHEMAS_MODULE.md`
- `13_MINIMAL_RUNNER_MODULE.md`
- `runner/`
- `examples/`
- `schemas/`

## 当前版本说明
- `v4.1.0`：新增 development / installation / deployment / debug 四类 optional capability modules
- `v4.1.1`：收口字段、模板、回归资产装配与 module_mode 口径
- `v4.2.0`：新增 context / tool contract / memory / runtime adapter 四类横切模块
- `v4.2.1`：收紧横切模块边界、门控顺序、副作用约束、memory 写入条件与 pointer 回读口径
- `v4.3.0`：新增 JSON Schema 机器校验层与 schema 模块
- `v4.4.0`：新增 minimal runner，跑通 schema validation / artifact write / readback

## 说明
- `README.md` 仅供人类快速查看，不作为执行体权威入口
- 执行体必须从 `00_INDEX.md` 开始装配模块
- 若说明文件与索引文件不一致，以 `00_INDEX.md` 为准
