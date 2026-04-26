# 13. Minimal Runner Module「最小运行器模块」

> 作用：提供 Harness v4 的最小本地可执行路径，跑通 schema 校验、artifact 写入与 readback「回读」。
> 原则：Minimal Runner 只验证结构与产物可回读，不替代 Step Orchestrator、Context Gate、Record Gate 或业务判断。

---

## 一、定位

Minimal Runner 是开发期 / 本地执行辅助模块，不构成新的 workflow_state「流程状态」。

它负责：
- 加载 `schemas/*.schema.json`
- 校验 JSON object「对象」是否符合对应 schema
- 写入本地 artifact「产物」
- 回读 artifact 并确认其可定位、可解析
- 为后续 runner / executor / governance 自动化提供最小路径

它不负责：
- 推进 workflow_state
- 自动选择 execution_profile
- 自动调用真实业务工具
- 自动判定根因或闭环
- 替代 Record Gate

---

## 二、当前实现

当前最小实现位于：

```text
runner/harness_runner.py
```

示例输入位于：

```text
examples/execution_plan.valid.json
examples/step_snapshot.valid.json
```

本地运行产物默认写入：

```text
artifacts/runner/
```

`artifacts/` 为本地临时运行产物目录，不进入版本库。

---

## 三、命令接口

### 3.1 列出 schema

```bash
python3 runner/harness_runner.py list-schemas
```

### 3.2 校验对象

```bash
python3 runner/harness_runner.py validate \
  --schema execution_plan \
  --input examples/execution_plan.valid.json
```

成功时输出：

```json
{"result": "pass", "schema": "execution_plan", "input": "examples/execution_plan.valid.json"}
```

失败时输出：

```json
{"result": "fail", "error": "<validation error>"}
```

### 3.3 校验并写入 artifact

```bash
python3 runner/harness_runner.py run \
  --schema execution_plan \
  --input examples/execution_plan.valid.json
```

执行顺序：

```text
load schema -> load input -> validate -> write artifact -> readback artifact
```

---

## 四、支持的 JSON Schema 子集

当前 runner 只实现本仓库 schema 已使用的子集：

- `$ref` to `common.schema.json#/$defs/...`
- `type`
- `required`
- `properties`
- `additionalProperties: false`
- `enum`
- `const`
- `oneOf`
- `minLength`
- `minimum`
- `pattern`
- `items`
- `minItems`
- `contains`

当前 runner 不声明为通用 JSON Schema 引擎。

若后续 schema 使用更复杂关键字，必须先扩展 runner 或改用正式 JSON Schema validator。

---

## 五、输出与回读

runner 写入的 artifact 至少包含：

- `schema`
- `written_at`
- `data`

readback「回读」至少确认：

- artifact 文件可读取
- JSON 可解析
- `schema / written_at / data` 三个字段存在

readback 通过不等于 Record Gate 通过。  
它只证明 artifact 可定位、可解析、可作为 evidence pointer 的候选来源。

---

## 六、退出码

- `0`：校验 / 写入 / 回读成功
- `1`：校验失败、JSON 解析失败、文件读写失败或 readback 失败

---

## 七、禁止事项

- 不得用 runner 校验通过冒充完整 run 成功
- 不得用 artifact readback 通过冒充 Record Gate 通过
- 不得让 runner 自动推进 workflow_state
- 不得把 `artifacts/` 临时产物当作长期闭环资产
- 不得把当前 runner 视为完整 JSON Schema 引擎
