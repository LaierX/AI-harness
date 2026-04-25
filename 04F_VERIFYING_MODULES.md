# 04F. Verifying Modules「验证模块组」

> 对应 workflow_state = `verifying`
> 目标：验证本次修复是否有效，并确认没有明显副作用。

---

## 一、模块清单

### 1.1 Live Verification Module「真实环境验证模块」
职责：
- 在真实运行层级验证修复效果

### 1.2 Clean Environment Verification Module「干净环境验证模块」
职责：
- 在较干净环境复查修复效果
- 排除污染因素

### 1.3 History Replay Verification Module「历史路径回放验证模块」
职责：
- 用历史路径或历史触发条件验证修复

### 1.4 Cross-path Verification Module「交叉路径验证模块」
职责：
- 从多个入口验证修复效果是否一致

### 1.5 Side-effect Check「副作用检查模块」
职责：
- 检查修复是否引入新问题
- 检查关键链路是否保持健康

---

## 二、退出条件

- 原问题已验证消失或明显缓解
- 关键路径复查已完成
- 副作用检查已记录
- Record Gate 已通过

---

## 三、最小输出

- verification summary
- evidence set
- side-effect note
- next step = `closing`
