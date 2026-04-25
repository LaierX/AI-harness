# 10. Changelog v4.1.0「变更记录」

## 新增
- 新增 `04G_DEVELOPMENT_MODULE.md`
- 新增 `04H_INSTALLATION_MODULE.md`
- 新增 `04I_DEPLOYMENT_MODULE.md`
- 新增 `04J_DEBUG_MODULE.md`

## 更新
- `00_INDEX.md`：新增 optional capability modules 入口与目录清单
- `README.md`：新增四类能力模块说明
- `02_EXECUTION_PROFILE_CONTROLLER.md`：新增四类模块的装配建议与装配矩阵
- `03_RECORD_AND_EVIDENCE_MODULE.md`：将四类模块纳入 Record Gate
- `04_RUN_ENGINE_ENTRY.md`：将四类模块纳入 Run Engine 的 optional capability layer
- `09_TEMPLATES.md`：新增 Capability Module Snapshot 模板

## 设计原则
- 不新增新的 workflow_state
- development / installation / deployment / debug 为 capability modules，不替代主流程步骤
- 所有 capability modules 退出前仍必须通过 Record Gate
