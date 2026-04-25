# 04I. Deployment Module「部署模块」

> 定位：为 Harness v4 提供 release rollout「发布推进」、health gate「健康门」、deployment rollback「部署回滚」能力。
> 原则：Deployment Module 负责把变更切入运行环境；它必须受健康门与回退策略约束。

---

## 一、模块职责

Deployment Module 负责：
- deployment plan「部署计划」
- rollout strategy「发布策略」
- deploy execution「部署执行」
- health gate evaluation「健康门评估」
- deployment verification「部署验证」
- deployment rollback「部署回滚」

Deployment Module 不负责：
- 替代 Installation Module 做安装准备
- 替代 Closing Module 做闭环判定
- 自动修复所有发布失败

---

## 二、模块清单

### 2.1 Deployment Plan Module「部署计划模块」
职责：
- 明确 deployment unit「发布单元」
- 明确目标环境、窗口、责任人、回滚边界

### 2.2 Rollout Strategy Module「发布策略模块」
职责：
- 选择一次性发布、分批发布、灰度发布等策略
- 记录流量切换或范围扩大规则

### 2.3 Deploy Executor Module「部署执行模块」
职责：
- 执行实际部署动作
- 记录 deploy log 与结果

### 2.4 Health Gate Module「健康门模块」
职责：
- 评估关键健康指标
- 判断是否允许继续 rollout 或必须 rollback

### 2.5 Deployment Verification Module「部署验证模块」
职责：
- 在目标环境验证功能与健康状态
- 确认部署结果与预期一致

### 2.6 Deployment Rollback Module「部署回退模块」
职责：
- 明确 rollback trigger「回退触发条件」
- 必要时执行回退并记录结果

---

## 三、进入条件

- 目标变更已具备可部署对象
- 安装或产物准备已完成
- 目标环境与健康门标准已明确
- execution_profile 与发布风险边界已明确

---

## 四、退出条件

- deploy plan 已记录
- deploy log pointer 已绑定
- health gate 结果已记录
- deployment verification 已记录
- rollback path 已明确
- Record Gate 已通过

---

## 五、推荐 module_mode

Deployment Module 常用：
- `release_execution`：执行正式发布、灰度、切流量或回滚
- `in_workflow`：作为 Fixing / Verifying 流程中的部署支撑
- `assist`：只提供发布计划、健康门或回滚策略建议

---

## 六、最小输出

- deployment unit
- rollout strategy
- deploy log pointer
- health result
- verification summary
- rollback trigger status
- deployment summary
- next step recommendation

---

## 七、禁止事项

- 不得未定义 health gate 就推进部署
- 不得把“执行完 deploy 命令”当作部署完成
- 不得未说明 rollback path 就做高风险发布
- 不得绕过 Record Gate 后直接宣称上线成功
