# 04H. Installation Module「安装模块」

> 定位：为 Harness v4 提供环境准备、组件安装、安装验证与安装回退能力。
> 原则：Installation Module 负责把目标组件正确装入环境；安装完成不等于部署完成。

---

## 一、模块职责

Installation Module 负责：
- prerequisite check「前置依赖检查」
- environment preparation「环境准备」
- install execution「安装执行」
- post-install verification「安装后验证」
- install rollback「安装回退」

Installation Module 不负责：
- 直接切流量或上线
- 替代 Deployment Module 做发布策略
- 替代 Closing Module 做闭环判定

---

## 二、模块清单

### 2.1 Prerequisite Check Module「前置依赖检查模块」
职责：
- 检查系统依赖、权限、空间、版本、网络等前置条件
- 输出 prerequisite result

### 2.2 Environment Preparation Module「环境准备模块」
职责：
- 准备目标目录、用户、权限、配置基线
- 记录环境修改动作

### 2.3 Install Executor Module「安装执行模块」
职责：
- 安装包、二进制、服务、依赖或配置
- 记录安装日志与结果

### 2.4 Install Verification Module「安装验证模块」
职责：
- 验证安装对象存在且可被调用
- 验证版本、路径、依赖解析结果

### 2.5 Install Rollback Module「安装回退模块」
职责：
- 说明如何回退安装动作
- 必要时执行回退并记录结果

---

## 三、进入条件

- 目标对象尚未就绪或需要重装 / 升级 / 补装
- Development artifact 或外部安装源已明确
- execution_profile 与环境风险边界已明确

---

## 四、推荐 module_mode

- `standalone_check`：仅做安装前置条件、版本、路径或依赖检查
- `assist`：为 Fixing / Verifying / Deployment 提供环境准备或安装验证
- `change_execution`：执行会改变环境状态的安装、升级、补装或重装动作

---

## 五、退出条件

- prerequisite result 已记录
- install log pointer 已绑定
- installed object / version 已确认
- install verification 已记录
- Record Gate 已通过

---

## 六、最小输出

- install target
- prerequisite result
- environment preparation note
- install log pointer
- installed version / path
- post-install result
- rollback note
- next step recommendation

---

## 七、禁止事项

- 不得把“安装成功”直接当成“部署成功”
- 不得跳过 prerequisite check 就做高风险安装
- 不得未记录安装日志就宣称安装完成
- 不得未说明回退路径就做不可逆安装修改
