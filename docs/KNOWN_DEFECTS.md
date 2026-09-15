# 已知缺陷与修复记录（截至 7.0.2）

本文记录 Mnemosyne 记忆栈在真实部署过程中**实测确认**的缺陷：症状 → 根因 →
实测数据 → 修法。代码位置精确到行。

> **标注约定**：`[实测]` 是跑出来的数据，`[代码]` 是读源码得到的结论，
> `[推理]` 是推导出来的判断。三类不要混用。
>
> **编号说明**：编号沿用内部的连续编号，其中 **F4 不在本文** ——
> 它属于外部宿主配置加载器的语义问题（不是 Mnemosyne 的缺陷），故不在此列。
> 保留原编号是为了让其他文档的交叉引用继续成立。

## 状态总览

| 编号 | 状态 | 一句话症状 | 一句话根因 |
|---|---|---|---|
| **F1** | ✅ 已修（7.0.1） | 经 MCP 写入的记忆，语义召回没有增益；向量库里没有它的向量 | MCP 写入固定走 `fast` 分支，而唯一的 `embed_engine.add()` 调用在 `else` 分支 |
| **F1b** | ✅ 已修（7.0.1） | 经 `retain_batch` 写入的记忆永远不进向量索引 | `retain_batch` **两个分支**都只把 embedding 写进记录，从不调用 `add()` |
| **F2** | ✅ 已修（部署侧） | 多个命名空间的向量混进同一个集合 | `MNEMOSYNE_QDRANT_COLLECTION` 环境变量**优先于**按命名空间派生集合 |
| **F3** | ⏳ 在案（已给缓解手段） | 新命名空间首次写入/读取卡约 6.5 秒 | 首次触达触发建 Qdrant 集合（Windows 上约 6 秒） |
| **F5** | ⏳ 在案 | 用 reindex 补过向量的记忆，语义召回永远排不上来 | 补齐脚本**只 upsert Qdrant，不回填 SQLite** 的 `embedding`，而 `vec_scores` 只在 SQLite 那份非空时才算 |
| **F6** | ✅ 已修（7.0.2，见 D5） | 无关查询也返回高分；一切"分数阈值"规则失效 | 最终分是加权和，`n_time×0.20 + conf×0.10` 构成对所有记录近似恒定的底 → 相关/无关首条分差仅 **0.010** |
| **F7** | ✅ 已修（7.0.1） | `retain` 传了 `confidence` 也不生效，落库恒为 0.7 | Notary 评估段**无条件**覆盖调用方传入的值 |
| **F8** | ✅ 已修（7.0.1） | `retain_batch` 逐项的 `tags`/`confidence`/`importance` 全部丢失 | 接口把批量元组第三元素写死成 `{}` |
| **F9** | ✅ 已修（7.0.1） | 拿到 `recall` 结果也**无法遗忘或更正** | 返回项里没有 `memory_id`，也没有 `verification` |
| **F9-b** | ✅ **已修（7.0.2，实测确证）** | `recall` 回传的 `superseded_by` 恒为 `null` | 检索层轻量记录白名单漏列该列，输出侧 `.get()` 静默取缺省值 |
| **F10** | ✅ 已修（7.0.1） | 以 `--namespace X` 启动，工具报告仍写 `namespace: "default"` | 代码写的是 `ns or "default"`，而 `ns` 只取自单次请求入参 |
| **F11** | ✅ 已修（7.0.1） | `forget` 之后记录仍可能被召回 | 检索缓存以存储文件指纹（mtime+size）判失效，而 SQLite 走 **WAL**：UPDATE 先落 `-wal`，主库 mtime 可能不变 |

## 7.0.2 轮次新确证缺陷（D1–D7）

这一轮的排查方式是"**从最终目标反推**"：目标是"精准记忆 / 精准召回 / 极短上下文下的精确
压缩"，于是逐项追问"7.0.1 的机制**在结构上**能否达成它"。以下都是由此挖出的、7.0.1
**结构上不可能达成**的项 —— 它们不是"参数没调好"，而是机制本身错了。

| 编号 | 状态 | 一句话症状 | 一句话根因 |
|---|---|---|---|
| **D1** | ✅ 已修（7.0.2） | `graph_query("用户")` **恒为空**；5 路融合里权重 0.10 的图通道长期空转 | 抽取器把 `用户的显卡是 RTX 4090` 的主语抽成 `用户的显卡`（`的`.isalnum() 为真）→ 图节点永远不是 `用户` |
| **D2** | ✅ 已修（7.0.2） | 取完结果 A 后再发一次无关查询 B，A 手里的置信带被**静默改写** | `_relevance_band` 挂在**跨调用共享**的检索索引记录 dict 上 |
| **D3** | ✅ 已修（7.0.2） | `budget_tokens=40` 实际塞进 150+ token 的中文；胶囊降级路径永不触发 | 无分词器时兜底用「4 字符 ≈ 1 token」（英文经验值），中文被低估 3~4 倍 |
| **D4** | ✅ 已修（7.0.2） | 长会话"越聊越偏"，正确答案从 rank1 掉到 rank3 | `access_boost` 是**加性**且上限 +0.20（与整路权重同量级），而计数对"进入结果列表"无条件累加 |
| **D5** | ✅ 已修（7.0.2） | 无关查询 top1 融合分**高于**相关查询 | 五路各自 `x/max(x)` 归一化 → 最高分恒为 1.0 → **分数没有绝对含义**；且旧行为无论如何填满 k 条 |
| **D6** | ✅ 已修（7.0.2） | 同一条偏好被反复重述 → 库里堆多条 0.98+ 重复；Top-K 被同事实变体塞满 | 写入侧无语义去重（只有事后 `dedup`） |
| **D7** | ✅ 已修（7.0.2） | 熔断窗口内的向量写入被**静默丢弃**，那批记忆永久失去语义索引且无人察觉 | 插件 `add()` 裸 `return`（返回 None），调用方无法区分"成功 / 真失败 / 被丢弃"；`doctor` 也不暴露插件统计 |

### 实测证据摘要（本轮）

| 项 | 实测数据 |
|---|---|
| D1 | 修前 `graph_query('用户')` → `[]`；修后 → 10 个邻居节点；`用户的显卡是 RTX 4090` → `用户 --is_a--> RTX 4090 (qualifier=显卡)` |
| D2 | 修前：相关查询返回的 3 条在无关查询之后全部变成 `band=low / _relevance=0.0`；修后保持 `high/medium/medium` |
| D3 | 修前：66 字符中文记忆按旧口径算 **16** token；修后按 CJK 口径算 **40+**，`budget_tokens=40` 真实触发降级 |
| D4 | 修前对照实验：仅因"先前问过 6 个无关问题"，干扰项 +0.12（= 6 × 0.02，与公式逐位吻合） |
| D5 | 修前：无关查询 top1 **1.0200** > 相关查询 **0.6922**；修后阈值标定：相关簇 cosine min **0.5222** / 无关簇 max **0.4064** → 下限取 **0.45** |
| D6 | 修前 `dedup` 报出 5 对 0.98~0.986 重复；修后写入侧收口，且**原子不同绝不合并** |
| D7 | 修后 `doctor()["vector_backend"]["breakers"]` 可直接读出剩余熔断时间与分类丢弃数 |

### D5 的修法与边界（为什么做成显式参数而不是全局阈值）

引入相关性下限后，**目标定位**（`forget` / 更正 / `dedup`）必须绕开它 ——
用户的描述天然含糊（"把那个 bge 维度的事忘掉"），若套用回答问题的阈值，
返回空就等于"无法遗忘"。安全性不靠阈值，而靠：① 所有目标解析都先走 `dry_run`
把候选报给用户确认；② 报告里带 `score` + `confidence_band` + 语义相似度原值。
因此下限做成 `retrieve(..., apply_floor=)` 显式参数，并写进查询缓存键避免两种结果互相污染。

### D6 的边界（宁可漏合并，绝不误合并）

语义去重必须叠加**原子守恒硬约束**：凡"改一个字就是另一个事实"的片段
（数字 / 日期 / 金额 / 型号 / URL / 邮箱 / 引号内原话）**不同者，相似度再高也不合并**。
否则 `用户的年假是 5 天` 会把 `用户的年假是 15 天` 吃掉 —— 数据没丢，但**事实被改错**，
而且用户与审计都看不出发生了什么。这是"记忆系统越用越不准"的最恶劣形态。

> 若在**未打过这些修复**的版本上验证，各缺陷的判别步骤仍然适用。
> 请把本文当作「如何识别这些缺陷」，而不是「当前一定存在这些缺陷」。

---

## F1 —— MCP 写入路径永不索引向量

### 事实

`mnemosyne/webui/mcp_server.py` 硬编码 `fast=True`：

```python
mid = b.retain(content, mtype=mtype, fast=True, project=project, **kwargs)
```

`mnemosyne/brain.py` 的 `fast=True` 分支把向量置空：

```python
if fast:
    record = _build_record(content, mtype=mtype, skip_detailed=True, **kwargs)
    record["embedding"] = None       # 向量被置空
    record["graph_edges"] = []
```

而 `embed_engine.add()` 的调用**只存在于 `else` 分支**：

```python
if self.embed_engine and self.enable_embeddings:
    record["embedding"] = self.embed_engine.encode(content)
    if record.get("embedding") and hasattr(self.embed_engine, "add"):
        self.embed_engine.add(record["id"], record["embedding"])
```

`retain()` 自己的 docstring 也写明了：`fast=True 跳过实体抽取/图/向量/冲突检测`。

### 实测量化

同一进程、同一插件、同一向量集合，各写 3 条：

```
retain(..., fast=True)      # MCP 等价路径
  向量库落库 0/3    SQLite embedding 字段 [False, False, False]

retain(...)                 # CLI / Python SDK 路径（默认 fast=False）
  向量库落库 3/3    SQLite embedding 字段 [True, True, True]
```

### 影响

只用 MCP 的客户端写入的**每条**记忆都不进向量库。召回仍能命中（内置 FTS5
候选池够用），所以**症状是安静的**；丢掉的恰恰是引入外部向量后端的全部理由 ——
`retrieval.py` 的 Path2a「突破 FTS top-K 候选池的语义召回」。

### 兜底手段（独立于修复）

补齐脚本可从 SQLite 权威存储找出向量库里缺失的向量并补齐（只增不删，默认 dry-run）。
**Mnemosyne 本就把 embedding 存在自己的 SQLite 里**，所以向量库不是向量的唯一存储，
事后补齐总是可行。这使 F1 变成可运营的问题，而不是数据损失。

### 修法（7.0.1 已实施）

**注意：只写向量索引是不够的。** 打分链路决定了这一点：

```python
# retrieval.py —— 向量分只在 embedding 非空时计算
if rec.get("embedding"):
    vec_scores[i] = self.embed_engine.similarity(q_vec, rec["embedding"])

# retrieval.py —— 语义后端下向量是主导信号
if _semantic_backend:          # = hasattr(embed_engine, "search")
    vec_weight = 0.55 if n_vec > 0.5 else 0.40
```

若只把向量写进向量库而让 `record["embedding"]` 保持 `None`，被召回的候选会以
`n_vec = 0` 参与评分，而它占的是**权重最高**的那一路 —— 等于白召回。

**正确修法 = 一次 `encode()`，同时喂给 SQLite 与向量后端。**
复用既有的 `encode()` + `add()` 两调用协议，不需要给插件新增任何 API。

---

## F1b —— `retain_batch()` 两个分支都从不索引向量

与 F1 同源但是**独立**的一处：

```python
# 旧 brain.py retain_batch()
if fast:
    rec["embedding"] = None
elif self.embed_engine and self.enable_embeddings:
    rec["embedding"] = self.embed_engine.encode(content)
    # ← 到此为止：算出来了，却从没调用 add()
```

结果：**经 `retain_batch` 写入的记忆，在 `fast=True` 和 `fast=False` 下都不进向量索引。**
受影响的入口：MCP 的 `retain_batch` 与 Python SDK 的 `retain_batch`。

修法与 F1 相同（在同一处补 `add()`），7.0.1 已一并修复。

---

## F2 —— `MNEMOSYNE_QDRANT_COLLECTION` 把所有命名空间钉死成一个集合

### 事实

`mnemosyne_plugins/qdrant_backend/plugin.py` —— **环境变量优先**：

```python
self.collection = os.environ.get("MNEMOSYNE_QDRANT_COLLECTION") or \
    self._derive_collection(brain)
```

一旦设了该变量，`_derive_collection()`（按命名空间派生）**永不执行**。

该集合内的 `search()` **不带命名空间过滤**，会把其他命名空间的 `memory_id` 一并返回。

### 严重度：不是内容泄漏

`retrieval.py` 会把外来 id 直接丢弃：

```python
id_to_idx_full = {r["id"]: i for i, r in enumerate(records)}   # 本命名空间的记录
existing = set(candidate_indices)
for _mid, _sim in self.embed_engine.search(q_vec, top_k=candidate_n):
    _i = id_to_idx_full.get(_mid)
    if _i is not None and _i not in existing:   # 不属于本空间 → 丢弃
        candidate_indices.append(_i)
```

**真实代价只是 Path2a 的候选槽被外来 id 稀释**，削弱语义召回增益。
定级时不要夸大成安全事件。

### 与其他发现的耦合

在 F1 未修时实际影响为**零** —— 因为写入路径根本不写向量，集合恒为空。
**F1 一旦修复，写入立刻发生，F2 从「零影响」变成「实际稀释」。两者必须同批处理。**

### 修法

**不要设置 `MNEMOSYNE_QDRANT_COLLECTION`。** 让插件按命名空间派生集合名
（`mnemosyne_<namespace>`）即可；默认派生结果与手动设置同名的场景下，
那一行既冗余又有害。

---

## F3 —— 新命名空间的首次触达阻塞约 6.4 秒，建出的集合却永远是空的

### 事实

召回 → `retrieval.py` 调 `embed_engine.search()` → 插件调 `_ensure_collection()`
→ GET 集合 → 404 → `_create_collection()`。插件自身 docstring 已写明：
**Windows 上创建集合约 6 秒**（Qdrant 1.19.1，冷存储）。

### 实测

```
recall #1: 6419 ms   ← 冷
recall #2:   21 ms
recall #3:    3 ms
recall #4:    2 ms

collection before: absent (404)
collection after : present, points=0     ← 一个点都没有
```

比值 **277~305×**。两次独立运行分别得到 6419 ms 与 6111 ms 的冷启动值。

### 影响

每个**新命名空间**（新 Agent、新项目）的首次触达被阻塞 6+ 秒。

修 F1 之前：触发点是首次 `recall`，且建出的集合因 F1 **永远是空的** —— 开销买不到任何东西。
修 F1 之后：**触发点转移到首次写入**（写入路径现在也会 upsert 向量，因而也去 ensure 集合），
集合会真的被用起来，但 6.5 秒的等待仍在。

两次实测的首触位置不同，值一致：

```
修 F1 前：  首次 recall 冷 6419 / 6111 / 7276 / 7576 ms   热 3~22 ms
修 F1 后：  首次 write  冷 6961 ms                        热 215 ms
```

### 判据（怎么确认你遇到的是 F3 而不是别的慢）

```python
{'collection_ready': True, 'collection_ms': 6052.3, 'embed_ok': True, 'embed_dim': 1024}
```

`warmup()` 返回的 `collection_ms` 就是建集合的真实成本 —— 约 6 秒，
且只在集合不存在时付一次。

### 修法

不需要改代码。在创建命名空间时调用插件**已有的** `warmup()` 预建集合即可，
实测有效。修 F1 后集合不再为空，因此这次预建的成果会被真正使用。

---

## F5 —— 补齐脚本补了向量库，但不回填 SQLite 的 `embedding`

### 事实

补齐脚本自己声明 *"never touches SQLite"* —— 它只 upsert 向量库，
**不写回 `memories.embedding`**。

而 `retrieval.py` 只在 `record["embedding"]` 非空时才计算 `vec_scores[i]`：

```python
for i in candidate_indices:
    rec = records[i]
    if rec.get("embedding"):                       # ← 为空则向量分恒为 0
        vec_scores[i] = self.embed_engine.similarity(q_vec, rec["embedding"])
```

### 实测（`dsh` 命名空间，5 条记录）

| 项 | 值 |
|---|---|
| 带 SQLite embedding | **3 / 5** |
| `embedding = NULL` 的 2 条 | 正是被补齐脚本补进向量库的那两条 |
| 这 2 条的召回分数 | **任何查询下都恒为 0.4052**（垫底常数） |
| 另 3 条 | 0.63 ~ 0.83 |

### 影响

补齐脚本**恢复了向量库的覆盖面，但没有恢复这些记录的检索排序能力**。
它们能被 Path2a 当候选捞出来，然后在权重最高的一路（`vec_weight = 0.55`）上得 0 分。

> **结论：补齐脚本是「让向量库完整」的工具，不是「让召回变好」的工具。**
> 别把它当成 F1 修复的完整替代。

### 修法（建议）

给补齐脚本加一个 `--backfill-sqlite`：把向量库里已存在的向量写回
`memories.embedding`（float32 BLOB，4×1024 = 4096 B）。

---

## F6 —— 召回分**无绝对标度**，任何「分数阈值」规则都会失效

### 事实

打分是一个加权和，其中 **`n_time×0.20` 与 `conf×0.10` 是对所有记录近似恒定的底**，
`× (0.6 + 0.4×importance)` 又整体缩放一次。结果是分数的**绝对高度被抬起来且被压缩**：

```python
total = ( n_bm25*0.12 + n_vec*0.55 + n_graph*0.10 + n_time*0.20 + conf*0.10 ) \
        * (0.6 + 0.4*imp) + access_boost + ngram_boost + syn_equiv
```

### 实测

| 查询 | 相关性 | 首条分数 | 正确目标排名 |
|---|---|---|---|
| 我用什么语言跟你沟通 | 高 | **0.8332** | **第 1 名** ✅ |
| 如何烤舒芙蕾蛋糕 | 无 | **0.8232** | 未命中 |
| 我的显卡是什么型号 | 无 | **0.8232** | 未命中 |

- 相关与不相关的**首条分差只有 0.0100**
- `k=1` 时，三个不同查询里有两个返回**同一条**记忆
- `[实测]` 完全无关的查询仍返回满 5 条，分数 0.76~0.82
- `[实测]` 未装载向量插件时，所有条目塌到 **0.4052** 这个常数底

`[实测]` 对照组：向量层原始余弦是**正常有区分度的** —— 相关 0.660 / 无关 0.303。
所以区分度是在**最终加权和**里被稀释掉的，不是嵌入模型的问题。

### 影响

**排序可用于挑选，分数不可用于过滤。**

任何 `score > 0.6` / `confidence > 0.6` 形式的规则都不会产生预期行为 ——
无关查询的分数同样在 0.6 以上。

### 正确的用法

1. 用**相对排名**取前 N（N=3 足够）
2. **由模型判断**"这几条到底相不相关"，而不是让阈值替它判断
3. 不要向模型暴露"分数很高所以一定相关"的暗示

> 这一条是**行为特性，不是可修复的缺陷**：加权和本身是设计选择。
> 记录在此，是为了防止后续再次写出基于绝对阈值的规则。

---

## F7 —— `retain` 的显式 `confidence` 被静默丢弃

### 事实

`mnemosyne/brain.py` 的 `retain()` 在 Notary 评估段**无条件**赋值：

```python
assessment = self.notary.assess(record, original_content, local_candidates)
record["confidence"] = assessment["confidence"]   # ← 覆盖一切调用方输入
record["flags"] = assessment["flags"]
```

`_build_record()` 明明接受 `confidence`，MCP 的 `retain` handler 也把它放进
kwargs 白名单 —— **但到了 `retain()` 里就被这一行盖掉。**

### 实测

```
retain(content=..., confidence=0.95)  →  工具返回 confidence: 0.7
```

0.7 正是 Notary 启发式打分的落点，所以库里 5/5 条全 0.7 ——
曾经被误解为"记忆可信度就是 0.7"，其实是**入参从未生效**。

CLI 同样中招：`mnemosyne retain --confidence` 最终也汇入同一个 `retain()`。

### 影响

"写入时必须设定 `confidence`"这一条规则**完全无效**。
更隐蔽的是它**不报错**：工具返回里照旧有 `confidence` 字段，只是值不是你给的那个。

### 修法（7.0.1 已实施）

在 `retain()` 开头取出调用方意图，Notary 评估后再还原；Notary 的原始判断
留在 `meta["notary_confidence"]`，信息不丢：

```python
_explicit_confidence = kwargs.pop("confidence", None)
...
if _explicit_confidence is not None:
    record["meta"]["notary_confidence"] = record.get("confidence")
    record["confidence"] = max(0.0, min(1.0, float(_explicit_confidence)))
```

---

## F8 —— `retain_batch` 丢弃逐项的 `tags` / `confidence` / `importance`

### 事实

`mnemosyne/webui/mcp_server.py`：

```python
batch = [(it["content"], it.get("mtype","semantic"), {}) for it in items]
#                                               ^^^ 元数据写死成空 dict
b.retain_batch(batch, fast=True)
```

而 `brain.retain_batch` 是支持第三元素为 kwargs 的
（`kwargs = item[2] if len(item) > 2 else {}`）。
所以**能力在，接口把它掐掉了**。

### 判据

```python
retain_batch(items=[{"content": ..., "tags": ["项目"], "confidence": 0.9}])
# schema 里没有 tags/confidence → 传进去也被忽略
# 库内该条 tags='[]'、confidence=默认值
```

### 修法（7.0.1 已实施）

schema 补 `tags` / `confidence` / `importance`，handler 逐项透传，并在返回里报告
`with_tags` / `with_confidence` 计数（便于一眼看出有没有真的传下去）。

---

## F9 —— `recall` 不回传 `memory_id`，也不回传 `verification`

### 事实

`recall` handler 的返回项只有：
`score / content / type / created_at / version / confidence / flags`。

### 影响（这条是"遗忘/更正规则不可执行"的直接原因）

- **没有 `memory_id`** → 即使 `forget`、`retain(supersedes=)` 都存在，
  调用方也**拿不到可以传进去的目标标识**。"先 recall 找到旧记忆，再更正/遗忘"
  这条流程在第一步就断了。
- **没有 `verification`** → 更正后的旧记忆在库里是 `verification=superseded`，
  检索层只是**降权**（×0.3）而非删除。回传里看不到这个字段，
  模型会把**已被取代的旧说法当成当前事实**引用。

### 修法（7.0.1 已实施）

返回项补 `memory_id` / `tags` / `verification` / `superseded_by`。

> 注意这里的设计取舍：**不要**为了"避免引用旧说法"而在服务端把 superseded 记录
> 直接过滤掉 —— 那会丢掉版本历史。正确做法是把状态**告诉模型**，由它判断。

### 勘误（F9-b，7.0.1 发布后修复）

7.0.1 上线后实测：`memory_id` / `verification` 正常，但
**`superseded_by` 恒为 `null`、`version` 恒为 `1`、`flags` 恒为 `[]`**。

根因不在 MCP 层（那里写的是 `r[1].get("superseded_by")`，写法没错），
而在**检索层的轻量记录白名单** —— `mnemosyne/retrieval.py` 的
`_RECORD_KEYS` / `_LIGHT_COLUMNS`。为了让内存里只留"检索融合所需字段"，
这两份白名单没有收录上述字段；而 MCP 的 `recall` 投影**直接读同一份 dict**，
于是 `.get()` 一律拿到缺省值，**全程没有任何报错**。

```python
# 实测（7.0.1 首发）
DB 直查   : superseded_by = "fedc038e27f5b7be"   # 库里有值
recall 返回: superseded_by = None                 # 输出侧看不到
```

修法：把 `version` / `superseded_by` / `flags` 并入两份白名单并在文件里写明
两处必须同步。三个字段都是小标量（`None` / `int` / 短列表），而占内存大头的是
`content`（本来就在清单里），所以内存影响可忽略。
验收脚本增加第 21 项断言兜底。

### ✅ 7.0.2 实测确证：已修

```python
# 实测（7.0.2，真实 Qdrant + BGE-M3 向量栈）
库内旧记录 : verification="superseded"  superseded_by="cda3111582163f2d"
recall 返回: band=high  ver=superseded  sup="cda3111582163f2d"   # ← 已带出
```

**注意一个容易误判的现象**：7.0.2 引入相关性下限后，验收脚本里那条
"用**无关查询**召回被取代记录、检查 `superseded_by`"的断言会**报 FAIL，
但缺陷其实已经修好** —— 因为被取代的记录与那个无关查询本就无关，
**被下限正确剔除了**（那正是下限的目的）。7.0.1 之所以能通过，只是因为
"无论如何都填满 k 条"。

因此 7.0.2 把这条断言改为用**与目标内容相关**的查询来验证投影本身，
并新增一条独立断言专门验证"无关查询受下限约束"。两者解耦，互不掩盖。
判别口诀：**"字段投影"要用相关查询验；"下限生效"要用无关查询验。**

> 教训：**"轻量投影"与"对外输出"共用同一份 dict 时，少一个键就是静默的数据丢失。**
> 今后每新增一个对外字段，都要同时检查这两份白名单；
> 反过来，凡是"字段在库里明明有值、工具返回却是 null"的现象，先查这里。

---

## F10 —— 工具的 `namespace` 报告恒为 `"default"`

### 事实

`mcp_server.py` 里 8 处写成：

```python
"namespace": ns or "default"
```

其中 `ns = _get_ns(arguments)` —— **只取自单次请求的 `arguments.get("namespace")`**。
请求里没写 `namespace` 时（正常情况，客户端用的是启动参数 `--namespace`），
就回落成**字面量 `"default"`**，而不是生效的默认命名空间。

### 实测

以 `--namespace memlife_test` 启动，写入确实落进了
`data/namespaces/memlife_test/`，但工具的返回里写的是 `"namespace": "default"`。

### 影响

不是数据问题（数据落在正确的命名空间），是**报告失真**：
调用方会把错误的归属告诉用户；多 Agent 场景下排查"这条写哪去了"会被误导。

### 修法（7.0.1 已实施）

`ns or "default"` → `ns or _default_namespace`（8 处）。
其中 `_default_namespace = args.namespace or "default"`，
所以未指定 `--namespace` 时行为完全不变，零回归风险。

---

## F11 —— `forget` 后记录仍可能被召回：检索缓存的失效判据在 WAL 下会漏判

### 事实

- 检索缓存的失效判据是 store 文件的 **`(mtime_ns, size)`**（`retrieval.py`）。
- SQLite 后端以 `PRAGMA journal_mode=WAL` 打开（`sqlite_backend.py`）。
- 在 WAL 下，`UPDATE` 先写 `-wal` 与 `-shm`，**主库 `memory.db` 的 mtime 可能不变**
  （要到 checkpoint 才合并）。

### 后果

`forget` 把 `status` 改成 `deleted` 之后，若只依赖指纹判失效，
`_cached_records` 里那份**旧副本**仍然有效 → 被遗忘的记忆**继续被召回**。
F1~F6 里没有一条能覆盖它：这是"改了库但缓存不知道"的经典形态。

### 修法（7.0.1 已实施）

`brain._invalidate_retrieval_index()` 显式置空指纹并清查询缓存，
在 `forget()` 与 `_mark_superseded()` 之后调用：

```python
self.retrieval._indexed_fingerprint = None
self.retrieval._query_cache.clear()
```

### 判据（怎么确认你遇到的是 F11）

遗忘一条记忆，随后立刻用它的原话 `recall`：

- 它**还在**结果里 → F11（缓存未失效），或下游自己又缓存了一层
- 它**不在了** → 正常

> 任何"直接改库"的新代码路径，都要问一句：**索引/缓存怎么知道？**
> 遗忘的两道保险意义不同：`status` 负责"检索层排除"，
> `confidence=0` 负责"撤回语义"。只做前者的实现在 WAL 下还会漏判。

---

## 附：这组缺陷合起来意味着什么

F7 / F8 / F9 单独看都是"少一个字段"的小问题，但它们**同向叠加**，
共同造成了同一个结论：

> **改造前，MCP 面上的「写入—更正—遗忘」闭环是不可执行的。**
> 写 `confidence` 不生效（F7）、批量写标签不生效（F8）、
> 拿到结果却没有 id 可用来指定目标（F9）、
> 而"遗忘"这件事**压根没有工具**（7.0.0 的 13 个工具里没有任何删除类工具，
> `memory/claim` 是 import-and-merge，不是删除）。

所以判断一个记忆栈是否"规则可执行"，**不能只看工具有没有名字**，
要看**参数是否生效、返回是否够用、闭环是否接通**。
这正是 [`scripts/verify_memory_lifecycle.py`](../scripts/verify_memory_lifecycle.py) 存在的理由。
