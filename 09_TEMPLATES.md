# 09. Templates「模板集」

> 作用：提供可直接复制使用的 plan「计划」、step snapshot「步骤快照」、closing summary「闭环摘要」与 capability module「能力模块」模板。

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
- spec_gap:
- recommended_version:
- recommended_patch_target:
- readback_status:
```
