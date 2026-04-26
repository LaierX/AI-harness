# 09. Templates「模板集」

> 作用：提供可直接复制使用的 plan「计划」、step snapshot「步骤快照」、closing summary「闭环摘要」与 capability module「能力模块」模板。
> 说明：本文件是人类可读模板入口；机器校验入口见 `12_SCHEMAS_MODULE.md` 与 `schemas/*.schema.json`。

---

## 一、Execution Plan「执行计划」模板

```md
# Execution Plan

- run_uid:
- issue_uid:
- target:
- execution_profile:
- current_step:
- objective:
- hypothesis:
- constraints:
- evidence_needed:
- stop_conditions:
- next_step:
```

---

## 二、Step Checklist「步骤清单」模板

```md
# Step Checklist

## 当前步骤
- [ ] 目标已明确
- [ ] 输入已确认
- [ ] 风险已评估
- [ ] 证据采集路径已确定
- [ ] 当前步输出已写入 running note
- [ ] 当前步结果已回读验证
- [ ] 退出条件已满足
- [ ] 回退条件已明确
```

---

## 三、Step Snapshot「步骤快照」模板

```md
## Step Snapshot
- step:
- objective:
- action_summary:
- key_evidence:
- evidence_pointer:
- decision:
- next_or_rollback:
- readback_status:
```

---

## 四、Capability Module Snapshot「能力模块快照」模板

```md
## Capability Module Snapshot
- step:
- module_name:
- module_mode:
- objective:
- action_summary:
- key_evidence:
- evidence_pointer:
- artifact_or_log_pointer:
- risk_note:
- decision:
- next_or_rollback:
- readback_status:
```

---

## 五、Closing Summary「闭环摘要」模板

```md
# Closing Summary
- run_uid:
- issue_uid:
- workflow_state: closing
- lifecycle_state:
- primary_record_db:
- narrative_path:
- rule_required:
- rule_reason:
- rule_location:
- close_summary:
- readback_status:
```

---

## 六、Regression Rule「回归规则」最小模板

```md
# Regression Rule

- rule_uid:
- rule_name:
- scope:
- target:
- source_issue_uid:
- trigger_condition:
- expected_result:
- verification_action:
- executor_type:
- severity:
- status:
- owner:
- created_at:
- updated_at:
```

---

## 七、Governance Review Checklist「治理反审清单」模板

```md
# Governance Review Checklist

- review_uid:
- review_scope:
- evidence_range:
- naming_drift_checked:
- workflow_lifecycle_state_checked:
- record_gate_bypass_checked:
- regression_asset_executor_checked:
- narrative_db_consistency_checked:
- context_assembly_checked:
- tool_contract_checked:
- memory_layer_checked:
- runtime_adapter_checked:
- spec_gap:
- context_gap:
- tool_contract_gap:
- memory_gap:
- runtime_adapter_gap:
- recommended_version:
- recommended_patch_target:
- readback_status:
```

---

## 八、Context Assembly Snapshot「上下文装配快照」模板

```md
## Context Assembly Snapshot
- run_uid:
- issue_uid:
- assembly_mode:
- workflow_state:
- module_name:
- module_mode:
- objective:
- injected_context:
- pointer_only_context:
- excluded_context:
- stale_or_tentative_items:
- memory_conflicts:
- gate_sequence:
- context_gate_result:
- readback_status:
```

---

## 九、Tool Contract「工具契约」模板

```md
## Tool Contract
- tool_uid:
- tool_name:
- tool_type:
- owner_module:
- input_schema:
- output_schema:
- side_effect_level:
- minimum_execution_profile:
- timeout_policy:
- retry_policy:
- failure_modes:
- rollback_hint:
- evidence_output:
- artifact_output:
- readback_method:
```

---

## 十、Tool Call Snapshot「工具调用快照」模板

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
- profile_check_result:
- context_gate_result:
- artifact_or_log_pointer:
- evidence_pointer:
- failure_type:
- exit_code:
- retry_count:
- decision:
- readback_status:
```

---

## 十一、Memory Entry「记忆条目」模板

```md
## Memory Entry
- memory_uid:
- memory_type:
- status:
- source_run_uid:
- source_issue_uid:
- source_pointer:
- summary:
- applicability:
- confidence:
- freshness:
- invalidation_condition:
- write_trigger:
- review_after:
- owner:
- created_at:
- updated_at:
```

---

## 十二、Runtime Adapter Capability「运行适配器能力」模板

```md
## Runtime Adapter Capability
- adapter_uid:
- adapter_name:
- adapter_type:
- supported_tool_types:
- pointer_scheme:
- artifact_root:
- environment_scope:
- pointer_minimum_fields:
- failure_surface:
- readback_method:
```

---

## 十三、Evidence Pointer「证据指针」模板

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

---

## 十四、Runtime Adapter Snapshot「运行适配器快照」模板

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
