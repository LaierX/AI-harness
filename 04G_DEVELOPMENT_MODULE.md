# 04G. Development Module「开发模块」

> 定位：为 Harness v4 提供可追踪的 change implementation「变更实现」能力。
> 原则：Development Module 负责实现变更，不直接推进 workflow_state；它通常支撑 Fixing Module，也可被独立调用。

---

## 一、模块职责

Development Module 负责：
- 准备 workspace「工作区」
- 规划变更范围
- 生成 patch / diff / branch「补丁 / 差异 / 分支」
- 执行 build / compile / package「构建 / 编译 / 打包」
- 进行 local validation「本地验证」
- 输出 artifact「产物」与变更摘要

Development Module 不负责：
- 宣称问题已修复
- 直接推进到 `verifying`
- 替代 Deployment Module 进行上线
- 绕过 Record Gate

---

## 二、模块清单

### 2.1 Workspace Init Module「工作区初始化模块」
职责：
- 准备代码或配置工作区
- 明确基线版本
- 记录当前分支 / 快照 / 版本号

### 2.2 Change Plan Module「变更计划模块」
职责：
- 说明为什么改
- 说明改哪些对象
- 说明不改哪些对象
- 说明风险边界

### 2.3 Patch Preparation Module「补丁准备模块」
职责：
- 生成 patch / diff / 变更列表
- 记录受影响文件 / 配置项
- 标记是否可回滚

### 2.4 Build Module「构建模块」
职责：
- 执行 build / compile / package
- 记录构建输入、输出与结果
- 绑定 build log pointer

### 2.5 Local Validation Module「本地验证模块」
职责：
- 对构建结果做最小本地验证
- 确认产物可被后续 Installation / Deployment 消费

### 2.6 Artifact Packaging Module「产物打包模块」
职责：
- 输出可交付 artifact
- 记录版本、checksum、位置

---

## 三、进入条件

- 需要代码或配置变更才能继续
- Fixing Module 已给出明确变更方向，或独立 change task 已成立
- execution_profile 与风险边界已明确

---

## 四、推荐 module_mode

- `change_execution`：实际执行代码、配置或构建变更
- `assist`：为 Fixing Module 提供变更方案、diff 分析或构建辅助
- `standalone_check`：独立检查变更可行性或产物完整性
- `in_workflow`：作为当前 workflow_state 内的支撑模块被调用

---

## 五、退出条件

- 变更摘要已生成
- 至少一个 patch / diff / artifact pointer 已绑定
- build 结果已记录
- local validation 结果已记录
- Record Gate 已通过

---

## 六、最小输出

- change summary
- affected objects
- patch / diff pointer
- build result
- validation result
- artifact pointer
- next step recommendation

---

## 七、禁止事项

- 不得把“构建成功”直接当成“修复完成”
- 不得未记录 patch / diff 就宣称已完成开发
- 不得把 Development Module 当作 Deployment Module 使用
- 不得绕过回滚与风险说明
