# 验收指南

对**已部署**的 Mnemosyne 记忆栈做事实驱动的验收。判据全部可复现，
每一步都说明"为什么这么验"，以及"怎么区分失败与已知未修的发现"。

本文不重复部署步骤。

---

## 0. 五条核心原则

1. **从真实配置里复读，不要硬编码副本。**
   验收脚本应当读客户端/宿主**实际使用的**那份 MCP 配置，再按它的流程重建子进程。
   否则验的是"另一套命令"。

2. **不写生产数据。** 把 `--brain-dir` 指向临时目录，或使用**一次性命名空间**；
   临时环境里摘除一切会把数据导向生产集合的变量。生产路径本身仍可作为
   **只读断言**。

3. **在能观测的地方观测。** 若某性质在某条路径上结构性不可观测，
   不要硬断言它 —— 换一条能观测的路径，并把路径差异如实打印出来。

4. **区分"失败"与"已知未修的发现"。** 两者都要显式输出。
   把发现伪装成通过、把发现伪装成失败，同样有害。

5. **★ 区分「配置正确」与「配置生效」。**
   从配置文件里复读内容、再自己拉起服务，只能证明
   「**如果**宿主加载了它就能工作」，**不能**证明「宿主**确实**加载了它」。
   生效性必须用**宿主自己的解析工具**验证（例如多数宿主提供的
   `--dump-config` / `--print-config` 之类与启动共用同一套解析代码的入口）。
   > 这条是踩坑后写下的：一次看起来"全部通过"的验收，
   > 掩盖了宿主其实**一个工具都没加载**的事实 —— 因为验收脚本复现的是
   > "配置里的内容"，而它天然对"宿主到底加载了什么"免疫。

---

## 1. 握手与工具面

- `initialize` 应返回 `serverInfo.name == "mnemosyne-memory"`。
- `tools/list` 在 **7.0.1 上应为 14 个工具**。核对其中存在：
  - `doctor`（完整性检查的 MCP 入口）
  - `forget`（7.0.1 新增；若缺失，说明"用户说忘记 X"这条流程**没有任何工具可调**）
- `retain` 的 schema 应含 `tags` / `confidence` / `importance` / `supersedes`。
- `retain_batch` 的 `items` 逐项 schema 应含 `tags` / `confidence` / `importance`。
- `recall` 的返回项应含 `memory_id` / `verification` / `tags` / `superseded_by`。
  注意 `superseded_by` 要**取到实际值**：未被取代的记录本来就是 `null`
  （值为 `None` 时该键不落进 dict，这是设计使然），
  但**被取代的那条必须指向取代它的新记忆 id**。
  7.0.1 首发版本该字段恒为 `null`（检索层轻量记录白名单漏列此字段，
  输出侧 `.get()` 静默拿到缺省值），已在 7.0.1 勘误中修复。

> **不存在** `verify_integrity` 工具 —— 完整性校验是 CLI 子命令
> （`mnemosyne --dir <brain> verify-integrity`）。把两者混为一谈会造成假失败。

---

## 2. 子进程环境必须逐键对齐

MCP 客户端通常会对**继承的环境变量**做筛选，再合并配置里显式声明的 `env`。
有的客户端会剔除键名匹配 `/KEY|PASSWORD|SECRET|TOKEN/i` 的变量，
或剔除带特定前缀的变量。

**两个推论**：

- **只靠继承环境配置 MCP 服务是不可靠的** —— 任何名字里带 `TOKEN` / `KEY`
  的变量都可能静默消失。必需的配置要写进配置行声明的 `env`。
- **反过来更容易犯的错：自己起 MCP 时把 `env` 忘了。**
  `[实测]` 踩过这个坑：手写子进程时没有带 `MNEMOSYNE_PLUGINS=qdrant_backend`，
  于是向量插件根本没加载，**所有条目分数塌到 `0.4052` 这个常数底**，
  看起来像"召回完全没有区分度" —— 其实是**测量装置的缺陷**，不是产品缺陷。

> **判定方法**：若所有结果的分数完全相同、或只差 0.00x，
> **先怀疑环境，再怀疑产品。**

---

## 3. 读写与冷/热延迟

写入用 `retain`，读取用 `recall`。**必须分别测冷热**：

| 指标 | 稳态预算 | 说明 |
|---|---|---|
| 写入 | < 500 ms | |
| 热召回 | < 1000 ms | 稳态预算 |
| 冷召回 | 无预算，但**必须记录** | 新命名空间的首次触达要付建集合成本（Windows 上约 6 s），见 F3 |

只测一次召回会把 6 秒的冷启动当成"召回慢"，或者把预热过的机器当成达标 —— 两者都错。

注意**冷启动的触发点取决于修复状态**：修 F1 之前是首次 `recall`；
修好之后转移到首次**写入**（写入路径也会 upsert 向量、因而也去 ensure 集合）。
所以写入的首次延迟同样要单独记录，不要直接对首次写入套用 500 ms 稳态预算。

---

## 4. 命名空间隔离 —— 必须分两层验

**召回层**（经接口）：A 区 `recall` 看不到 B 区内容，B 区看得到自己的。这是必要条件。

**向量层**（直接库调用）：若写入路径未索引向量（F1），
在接口层测向量隔离是**结构性不可能**的。改用直接库调用 `fast=False`，
以决定性判据验证：

> 拿 B 区自己的措辞去查 A 区。若两区共享同一个集合，
> B 的 `memory_id` **必然**是最近邻。

```
own_id_present      = True    ← 证明 fast=False 确实索引了
foreign_id_present  = False   ← 证明集合分离且不穿透
```

注意：即使集合被共享，**也不是内容泄漏** —— `retrieval.py` 会把不属于本命名空间的
id 直接丢弃，代价只是 Path2a 的候选槽被稀释。报告时要如实分级，不要夸大成安全事件。

---

## 5. 完整性与审计

| 用途 | 入口 |
|---|---|
| 健康/完整性 | MCP `doctor`，或 CLI `verify-integrity` |
| 审计轨迹 | MCP `audit`（传 `memory_id`） |
| 置信度轨迹 | MCP `confidence_history` |
| 统计 | MCP `stats` |

查向量库里的点：**不要**用 `match: {text: ...}` 这类过滤 ——
未建索引的 payload 字段上的过滤永远不匹配，会造成假失败。
正确做法是 scroll 出点再比对 payload 里的 `memory_id`。

---

## 6. 协议卫生与清理

- stdout **只能**有 JSON-RPC 行；任何 `Traceback` 都是缺陷。
- 清理：删掉测试用的向量集合（**404 视为已删除**，不要当失败）、
  删掉临时 brain 目录、确认生产 brain 目录里没有残留的测试命名空间。

---

## 7. 记忆生命周期闭环（写入 → 更正 → 遗忘）

只要你在给客户端写**写入/更正/遗忘**类规则，这一步就必须做：
**规则写了不等于工具支持。**

用 [`scripts/verify_memory_lifecycle.py`](../scripts/verify_memory_lifecycle.py)：

```bash
<python> scripts/verify_memory_lifecycle.py \
  --python <python> --brain-dir <brain> --src-root <源码根> --namespace memlife_verify
```

它覆盖 21 项断言，四条核心判据是：

| 判据 | 怎么看 |
|---|---|
| `retain(confidence=0.95)` 落库就是 **0.95** | 实际写 0.7 → 命中 F7（Notary 覆盖） |
| `recall` 返回项含 **`memory_id`** | 没有 id，"遗忘/更正"无从定位（F9） |
| `forget` 后目标 **`confidence=0.0` 且 `status=deleted`**，且**再召回不再出现** | 只有 `status` 变了、`confidence` 没动 → 旧实现 |
| 工具的 `namespace` 报告 == 启动时的 `--namespace` | 恒报 `default` → 命中 F10 |

另外两条容易漏的：

- `retain_batch` 的**逐项** `tags` / `confidence` 必须生效（F8：原实现把元数据写死成 `{}`）。
- 更正必须走 `retain(supersedes=<旧id>)`，随后旧记忆应为 `verification=superseded`
  且 `recall` 能**读到**这个字段 —— 读不到的话，模型会把被取代的旧说法当现状引用。
- 同一条旧记忆经 `recall` 回传的 **`superseded_by` 必须等于新记忆 id**。
  这和第 156 行的 `memory_id` 是两件事：`memory_id` 验的是"能不能定位到目标"，
  `superseded_by` 验的是"能不能顺链条走到新说法"。7.0.1 首发时后者恒为 `null`。

> **不要只看 `status=deleted` 就收工。** 遗忘的两道保险意义不同：
> `status` 负责"检索层排除"，`confidence=0` 负责"撤回语义"。
> 只做前者的实现在 WAL 模式下还有第三个坑 —— 检索缓存以文件指纹（mtime+size）失效，
> 而 WAL 的 UPDATE 未必改主库 mtime，所以必须显式让检索索引失效（F11）。

---

## 附：验收时容易踩的假失败

| 假失败 | 真相 |
|---|---|
| 调用 MCP 工具 `verify_integrity` 报"工具不存在" | 它是 **CLI 子命令**；MCP 对应工具是 `doctor` |
| 断言"每个命名空间一个集合"在接口路径上失败 | 在**未修 F1/F2** 的版本上该断言**结构性不可能**成立。要稳妥地在向量层测，直接用库调用 `fast=False` |
| 用 `match: {text: ...}` 过滤查不到点 | 未建索引的 payload 字段，这样的过滤永远不匹配；应 scroll 后比对 `memory_id` |
| 删除不存在的集合返回 `false`，判为失败 | 清理流程里 **404 应视为成功**（本就已删除） |
| 测出"召回完全没有区分度"（分数全挤在一起） | **十有八九是子进程环境漏了向量插件。** 插件不加载 → 向量一路全 0 → 所有条目塌到 0.4052 常数底。**测之前先把子进程环境与配置逐键对齐** |
| 测出的延迟是 6 秒级 | 那是 F3 冷启动（首次触达建集合），不是稳态延迟。先预热再测 |
| `retain_batch` 返回成功，但库里 `tags='[]'` | 逐项元数据被丢弃（F8）。7.0.1 起已修，返回里会报告 `with_tags` / `with_confidence` 计数 |

---

## 附：Windows 运维注意事项

- PowerShell 执行策略常为 `Restricted`，需
  `powershell -ExecutionPolicy Bypass -File <script>.ps1`。
- PowerShell 5.1 的 `Start-Process` 对**大小写重复的环境键**会抛异常
  （Windows 环境变量大小写不敏感）—— 传环境前先去重。
- `System.Net.Http.HttpClient` 在 PS 5.1 里**未默认加载**，健康探测会全部假失败；
  改用 `[System.Net.WebRequest]` 并显式 `$request.Proxy = $null`。
- 若设了 `HTTP_PROXY`，访问 localhost 也会被劫持（死端口返回 502 而非连接拒绝）。
  插件侧应**无条件绕过 localhost 代理**；脚本侧同样要显式禁用代理。

---

## 相关文档

- [KNOWN_DEFECTS.md](KNOWN_DEFECTS.md) —— 各缺陷的精确代码位置、实测数据、修法
- [RECALL_STRATEGY.md](RECALL_STRATEGY.md) —— 召回机制、接口边界、每轮召回的代价
- [scripts/verify_memory_lifecycle.py](../scripts/verify_memory_lifecycle.py) —— 生命周期闭环验收脚本
