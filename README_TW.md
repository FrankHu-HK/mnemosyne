<p align="center">
  <img src="assets/banner.png" alt="Mnemosyne OS" width="100%">
</p>

# Mnemosyne OS

<p align="center">
  <a href="https://pypi.org/project/mnemosyne-os/">PyPI</a> ·
  <a href="https://github.com/FrankHu-HK/mnemosyne">GitHub</a> ·
  <a href="README_CN.md">簡體中文</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/mnemosyne-os/"><img src="https://img.shields.io/badge/PyPI-mnemosyne--os-blue?style=for-the-badge" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="授權條款: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="#-mcp-伺服器"><img src="https://img.shields.io/badge/MCP-31%20Tools-00ADD8?style=for-the-badge" alt="模型上下文協定"></a>
  <a href="#-快速開始"><img src="https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge" alt="零相依"></a>
  <a href="https://pepy.tech/projects/mnemosyne-os"><img src="https://img.shields.io/pepy/dt/mnemosyne-os?style=for-the-badge" alt="Downloads"></a>
  <a href="https://x.com/mnemosyne_oos"><img src="https://img.shields.io/badge/X-@mnemosyne_oos-black?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
</p>

<p align="center">
  <a href="README_TW.md"><img src="https://img.shields.io/badge/Lang-繁體中文-red?style=for-the-badge" alt="繁體中文"></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/Lang-Español-orange?style=for-the-badge" alt="Español"></a>
  <a href="README.ru.md"><img src="https://img.shields.io/badge/Lang-Русский-blue?style=for-the-badge" alt="Русский"></a>
  <a href="README.de.md"><img src="https://img.shields.io/badge/Lang-Deutsch-lightgrey?style=for-the-badge" alt="Deutsch"></a>
  <a href="README.th.md"><img src="https://img.shields.io/badge/Lang-ไทย-blue?style=for-the-badge" alt="ไทย"></a>
  <a href="README.ko.md"><img src="https://img.shields.io/badge/Lang-한국어-green?style=for-the-badge" alt="한국어"></a>
  <a href="README.ja.md"><img src="https://img.shields.io/badge/Lang-日本語-red?style=for-the-badge" alt="日本語"></a>
</p>

**Mnemosyne OS 8.0.0** — 一套零相依、本機優先的 AI 記憶系統。內建圖形
記憶、多模態擷取、重排序、時序推理、雜湊鏈稽核帳本、無損壓縮，以及 31 個 MCP 工具。

> 唯一一個**核心真正零第三方相依**的 AI 記憶引擎 —— 不需要向量資料庫、不需要 LLM
> 執行環境、不需要雲端帳號。`install_requires` 是空清單。筆電、伺服器、無伺服器
> 環境都能執行。

可以當作 **Python 函式庫**、**CLI**、**HTTP API** 或 **MCP 伺服器**來使用。

---

## 🚀 快速開始

### 安裝

```bash
pip install mnemosyne-os          # 核心：零第三方相依
```

### 不需任何設定就能記住與回想

```python
from mnemosyne import Memory

m = Memory()                       # 內建嵌入器 + 規則式擷取器
m.add("I prefer dark mode and use vim keybindings. My name is Alice.",
      user_id="alice")

for hit in m.search("what does alice prefer", filters={"user_id": "alice"})["results"]:
    print(f"{hit['score']:.3f}  {hit['memory']}")
```

離線、免 API 金鑰、不下載模型、不裝資料庫 —— 這正是下一節得以成立的原因。

### 等到召回需要更強時，再接上真實模型

```python
from mnemosyne import Memory

m = Memory.from_config({
    "llm":          {"provider": "openai", "config": {"model": "gpt-4o-mini"}},
    "embedder":     {"provider": "openai", "config": {"model": "text-embedding-3-small"}},
    "vector_store": {"provider": "qdrant", "config": {"url": "http://localhost:6333"}},
    "reranker":     {"provider": "cohere", "config": {"api_key": "..."}},
    "graph_store":  {"provider": "builtin"},
})
```

每個元件都各自獨立可選。當某個供應商建不起來時，會退回內建等價實作，並且
**如實回報** —— 絕不無聲降級：

```python
m.describe()["degraded"]
# {'llm': {'requested': 'openai', 'used': 'rules', 'reason': 'no API key configured',
#          'hint': 'Set MNEMOSYNE_LLM_OPENAI_API_KEY ...'}}
```

### 或者從命令列操作

```bash
mnemosyne init
mnemosyne add "I prefer dark mode and vim keybindings" --user-id alice
mnemosyne search "what does alice prefer" --user-id alice
mnemosyne list  --user-id alice
mnemosyne event --limit 10
mnemosyne --agent search "preferences" --user-id alice   # 供工具迴圈使用的 JSON 封裝
```

### 或者透過 MCP 曝露

```json
{
  "mcpServers": {
    "mnemosyne": {
      "command": "python",
      "args": ["-m", "mnemosyne.webui.mcp_server",
               "--brain-dir", "./mem", "--namespace", "default"],
      "env": { "MNEMOSYNE_MCP_TOKEN": "<random 32+ chars>" }
    }
  }
}
```

### 或者透過 HTTP 提供服務

```bash
mnemosyne-web --port 9090          # 主控台與 REST 共用同一個連接埠
curl -X POST http://127.0.0.1:8788/v3/memories/add/ \
  -H "Authorization: Bearer $MNEMOSYNE_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"I moved to Berlin in 2023."}],"user_id":"alice"}'
```

---

## 📊 基準測試

以本倉庫隨附的測試工具實測。可用
`scripts/verify_recall_quality.py` 與 `scripts/verify_precision_recall.py` 重現。

| 基準 | 分數 | 衡量什麼 |
| --- | --- | --- |
| LongMemEval | **96.2** | 長跨度對話召回 |
| LoCoMo | **94.8** | 多工作階段對話記憶 |
| BEAM (1M) | **68.5** | 1M token 上下文預算下的召回 |
| BEAM (10M) | **53.9** | 10M token 上下文預算下的召回 |

分數以 100 分為滿分。

---

## 🧩 功能一覽

<table>
<tr><td><b>記憶 API</b></td><td><code>Memory</code> / <code>AsyncMemory</code> / <code>MemoryClient</code>，方法面完整：<code>add</code> <code>get</code> <code>get_all</code> <code>search</code> <code>update</code> <code>delete</code> <code>delete_all</code> <code>history</code> <code>reset</code> <code>close</code> <code>from_config</code>。</td></tr>
<tr><td><b>四維作用域</b></td><td><code>user_id</code> / <code>agent_id</code> / <code>run_id</code> / <code>app_id</code> —— 由<b>實體隔離</b>強制落實：每個作用域一個 SQLite 檔案，而不是共用資料列再加一道篩選。</td></tr>
<tr><td><b>篩選語法</b></td><td><code>eq</code> <code>ne</code> <code>gt</code> <code>gte</code> <code>lt</code> <code>lte</code> <code>in</code> <code>nin</code> <code>contains</code> <code>icontains</code> <code>wildcard</code>，搭配可任意巢狀的 <code>AND</code>/<code>OR</code>/<code>NOT</code>。</td></tr>
<tr><td><b>單遍 ADD-only 擷取</b></td><td>每次寫入只呼叫一次模型；記憶持續累加，永不覆寫。因為不覆寫，壞的擷取只會引入雜訊 —— 永遠不可能摧毀真實事實。</td></tr>
<tr><td><b>圖形記憶，常時開啟</b></td><td>實體連結與多跳遍歷都住在同一個 SQLite 檔案裡。不需要外部圖形資料庫。</td></tr>
<tr><td><b>多模態擷取</b></td><td>接受 OpenAI、Anthropic 與 Gemini 的圖片內容格式（以及音訊）。有設定視覺模型時會儲存描述；沒設定時儲存參照 —— 不會丟掉任何東西。</td></tr>
<tr><td><b>多訊號檢索</b></td><td>語意 + BM25 關鍵字 + 實體圖 + 時序 + 標籤五路融合，帶有校準過的相關性下限與詞面備援。</td></tr>
<tr><td><b>時序推理</b></td><td>觀測日期、相對時間解析、到期語意，以及依實體的版本鏈。</td></tr>
<tr><td><b>分層記憶</b></td><td>熱 / 溫 / 冷三層，搭配遺忘經濟學：低價值記憶會被降級並壓縮，絕不無聲刪除。</td></tr>
<tr><td><b>無損壓縮（AIC）</b></td><td>把一則記憶壓縮成<i>指標 + 結構化事實 + 內容原子</i>。數字、日期、金額與型號在每一層都完整保留；<code>expand()</code> 可逐位元組還原原文並驗證其雜湊。</td></tr>
<tr><td><b>雜湊鏈稽核帳本</b></td><td>一條 SHA-256 鏈；<code>verify_integrity()</code> 能偵測竄改並指出確切是哪一筆被更動。</td></tr>
<tr><td><b>非同步 API 與事件</b></td><td><code>AsyncMemory</code> 支援高吞吐量寫入，加上持久化操作日誌，讓已受理的寫入跨行程仍可見。</td></tr>
<tr><td><b>中文最佳化</b></td><td>Bigram 斷詞 + FTS5 + 內建同義詞詞典，同時完整支援拉丁文字。</td></tr>
<tr><td><b>安全公證器</b></td><td>在寫入落地前偵測憑證、不可見 Unicode 與 HTML 注入，並在欄位層級進行遮蔽。</td></tr>
</table>

---

## 🔌 支援的整合

每個轉接器都是選用的。**stdlib** 轉接器完全不需要第三方套件
—— 它們直接透過 `urllib` 講 HTTP。**sdk** 轉接器會延遲載入其 SDK，
並明確告訴你少了哪個套件。

### LLM 供應商（20）

| 傳輸方式 | 供應商 |
| --- | --- |
| **stdlib HTTP** | `openai` `openai_structured` `azure_openai` `azure_openai_structured` `ollama` `anthropic` `gemini` `groq` `together` `deepseek` `minimax` `xai` `sarvam` `openrouter` `litellm` `lmstudio` `vllm` |
| **sdk** | `langchain` `aws_bedrock` |
| **內建** | `rules` —— 一個確定性的離線擷取器，這正是完全沒設定模型時 `add()` 也能運作的原因 |

### 嵌入模型（13）

| 傳輸方式 | 供應商 |
| --- | --- |
| **stdlib HTTP** | `openai` `azure_openai` `ollama` `gemini` `vertexai` `together` `lmstudio` `huggingface` |
| **sdk** | `fastembed` `langchain` `aws_bedrock` |
| **內建** | `builtin`（128 維、零相依、確定性）· `hashing`（任意維度、離線） |

### 向量儲存庫（28）

| 傳輸方式 | 儲存庫 |
| --- | --- |
| **內嵌** | `builtin`（單一 SQLite 檔案同時存放記憶與向量）· `memory` · `generic`（宣告式 REST） |
| **stdlib HTTP** | `qdrant` `pinecone` `elasticsearch` `opensearch` `weaviate` `upstash_vector` `turbopuffer` |
| **sdk** | `chroma` `pgvector` `milvus` `mongodb` `redis` `valkey` `azure_ai_search` `azure_mysql` `baidu` `cassandra` `databricks` `faiss` `langchain` `neptune` `oracledb` `s3_vectors` `supabase` `vertex_ai_vector_search` |

### 圖形資料庫（6）

`builtin`（原生 SQLite 三元組）· `neo4j` · `memgraph` · `neptune` · `kuzu` · `sparql`（任一 SPARQL 1.1 端點）

### 重排序器（5）

`llm` · `cohere` · `zero_entropy` · `huggingface` · `sentence_transformer`

### 框架轉接器

LangChain · LlamaIndex · CrewAI · Dify · n8n · Vercel AI SDK · Ollama · MCP（stdio + Streamable HTTP）

---

## 🛠 MCP 伺服器

以 stdio JSON-RPC 執行：

```bash
export MNEMOSYNE_MCP_TOKEN="your-secret-token"   # 選用，但建議設定
python -m mnemosyne.webui.mcp_server --brain-dir ./mem --namespace default
```

**31 個工具** —— 20 個原生工具，外加 11 個沿用慣用
agent-memory 工具名稱的工具，因此既有的 MCP 用戶端不必改寫其工具定義，就能直接指向 Mnemosyne。

**原生（20）：**

| 工具 | 用途 |
| --- | --- |
| `retain` | 儲存一則記憶 |
| `recall` | 檢索記憶 |
| `retain_batch` | 批次寫入，約快 15× |
| `forget` | 遺忘一則記憶 —— 可用 id，也可用自然語言查詢定位 |
| `capsule` | 把一則記憶壓縮成 指標 + 事實 + 原子 |
| `expand` | 逐位元組還原膠囊的原文 |
| `recall_health` | 唯讀的召回品質指標 |
| `consolidate` | 把近似重複的記憶合併成一則代表 |
| `reflect` | 統計、高頻實體、衝突偵測、認知模式 |
| `dedup` | 偵測重複與近似重複 |
| `graph_query` | 知識圖譜遍歷 |
| `temporal_query` | 版本鏈查詢 |
| `list_projects` | 列出隔離的專案 |
| `doctor` | 健康檢查 —— 完整性、筆數、磁碟、後端狀態 |
| `stats` | 執行期統計 |
| `audit` | 稽核鏈查詢 |
| `confidence_history` | 信心度軌跡 |
| `memory/export-v1` | 透過 Memory Exchange Protocol 匯出 |
| `memory/import-v1` | 透過 Memory Exchange Protocol 匯入 |
| `memory/claim` | 從外部匯出接管記憶 |

**用戶端相容（11）：**

| 工具 | 用途 |
| --- | --- |
| `add_memory` | 為某個使用者/代理儲存文字或對話歷史 |
| `search_memories` | 帶篩選條件的語意搜尋 |
| `get_memories` | 結構化篩選 + 分頁列表 |
| `get_memory` | 依 id 取得一則 |
| `update_memory` | 覆寫文字和/或中介資料 |
| `delete_memory` | 刪除一則 |
| `delete_all_memories` | 清空某個作用域 |
| `delete_entities` | 刪除實體並串聯 |
| `list_entities` | 列出 users/agents/apps/runs |
| `list_events` | 列出記憶操作 |
| `get_event_status` | 輪詢非同步操作 |

---

## 🌐 自架 REST API

單一行程、單一連接埠，接受 `X-API-Key`、`Bearer` 與 `Token` 鑑權標頭。
主控台與 API 共用同一個監聽器。

| 方法 | 路徑 | 用途 |
| --- | --- | --- |
| `GET` | `/v1/status/` | 存活探測 + 即時設定報告 |
| `GET` | `/v1/providers/` | 每個供應商及其目前可用性 |
| `POST` | `/v3/memories/add/` | 擷取並儲存（非同步，回傳事件 id） |
| `POST` | `/v3/memories/search/` | 語意搜尋 |
| `POST` | `/v3/memories/get-all/` | 帶篩選的列表 |
| `GET` / `PUT` / `DELETE` | `/v3/memories/{id}/` | 取得 / 更新 / 刪除一則 |
| `DELETE` | `/v3/memories/` | 清空某個作用域 |
| `GET` | `/v3/memories/{id}/history/` | 變更歷程 |
| `GET` | `/v1/event/{id}/` · `/v1/events/` | 輪詢 / 列出操作 |
| `GET` / `DELETE` | `/v2/entities/` | 列出 / 刪除作用域 |
| `POST` | `/v3/graph/{add,search,get-all,delete-all}/` | 圖形記憶 |
| `POST` | `/v1/capsule/` · `/v1/expand/` | 無損壓縮 |
| `GET` | `/v1/integrity/` | 帳本驗證 |
| `GET` / `POST` / `DELETE` | `/v1/keys/` | API 金鑰管理 |

---

## 🧠 Python API

```python
from mnemosyne import Memory, AsyncMemory, MemoryClient

# --- 擷取 / 作用域 / 篩選 -----------------------------------------------------
m = Memory()
m.add([{"role": "user", "content": "I moved to Berlin in 2023."}],
      user_id="alice", metadata={"source": "onboarding"},
      observation_date="2023-06-01")
m.add("The invoice number is INV-2024-001.", user_id="alice", immutable=True)

hits = m.search("where does the user live",
                filters={"user_id": "alice",
                         "AND": [{"source": {"eq": "onboarding"}}]},
                top_k=5, threshold=0.1, rerank=False, explain=True)

# --- 多模態 -------------------------------------------------------------------
m.add([{"role": "user", "content": [
    {"type": "text", "text": "My new desk."},
    {"type": "image_url", "image_url": {"url": "https://example.com/desk.jpg"}},
]}], user_id="alice")

# --- 圖形記憶 -----------------------------------------------------------------
m.graph_add("Jobs founded Apple in Cupertino.", user_id="alice")
m.graph_search("Apple", filters={"user_id": "alice"})

# --- 非同步與事件 -------------------------------------------------------------
async def ingest():
    am = AsyncMemory()
    await am.add_many([{"messages": t, "options": {"user_id": "alice"}}
                       for t in transcripts])
```

`Memory`、`AsyncMemory` 與 `MemoryClient` 也接受其他記憶函式庫慣用的
agent-memory 呼叫形式，因此已針對該形式寫好的程式碼，只要更動 import 就能切換。
見 [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md)。

引擎自身的能力都掛在同一個物件上：

```python
from mnemosyne import MemoryBrain

brain = MemoryBrain("./memories", enable_embeddings=True)
brain.ensure_init()
brain.retain("His laptop is an ASUS VivoBook Pro 14", fast=True)

results = brain.recall("what are that machine's specs", k=5)
results, cost = brain.recall("that machine's specs", k=5, budget_tokens=100)

cap = brain.capsule("<memory_id>", budget_tokens=60)   # 指標 + 事實 + 原子
brain.expand(cap["ref"])                                # 逐位元組還原
brain.verify_integrity()                                # SHA-256 帳本檢查
```

---

## 📂 目錄結構

```
mnemosyne/
├── api/                 # 記憶 API：Memory / AsyncMemory / MemoryClient
│   ├── memory.py        #   引擎支撐的用戶端
│   ├── config.py        #   MemoryConfig + 維度一致性檢查
│   ├── filters.py       #   篩選語法 -> 述詞
│   ├── extract.py       #   單遍 ADD-only 擷取
│   ├── multimodal.py    #   圖片 / 音訊附件解析
│   ├── events.py        #   持久化操作日誌
│   └── client.py        #   內嵌 + HTTP 傳輸
├── providers/           # 選用元件轉接器（共 72 個）
│   ├── llms.py          #   20 個 LLM 供應商
│   ├── embedders.py     #   13 個嵌入供應商
│   ├── vector_stores.py #   28 個向量儲存庫
│   ├── graph_stores.py  #   6 個圖形資料庫
│   ├── rerankers.py     #   5 個重排序器
│   ├── vision.py        #   三種圖片 wire format
│   └── transport.py     #   stdlib HTTP + 重試 + 憑證遮蔽
├── brain.py             # MemoryBrain —— 引擎門面
├── capsule.py           # AIC 無損壓縮
├── retrieval.py         # 多訊號融合與相關性校準
├── graph.py             # 時序三元組儲存
├── notary.py            # 寫入前信任管線
├── cli.py               # 原生 CLI
├── api_cli.py           # 用戶端 API CLI
└── webui/
    ├── web_server.py    # 主控台 + REST 主機
    ├── api_routes.py    # /v1 /v2 /v3 路由
    ├── mcp_server.py    # 20 個原生 MCP 工具
    └── mcp_api.py       # 11 個用戶端相容 MCP 工具

storage/                 # SQLite 後端、雜湊鏈帳本、外掛 SDK
security/                # 矛盾偵測、安全報告
scripts/                 # 驗證指令碼
docs/                    # 驗收指南、召回策略、相容性
```

---

## ✅ 測試

```bash
python verify.py                              # 自我檢查
python scripts/verify_api.py                  # 用戶端 API 驗證，完全離線
python scripts/verify_memory_lifecycle.py --brain-dir ./mem --src-root .
python scripts/verify_precision_recall.py     # 離線精確度回歸
python scripts/verify_recall_quality.py       # 端對端召回品質
```

---

## 📚 文件

- [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) —— 慣用的 agent-memory 呼叫形式
- [docs/ACCEPTANCE_GUIDE.md](docs/ACCEPTANCE_GUIDE.md) —— 驗收準則與各項對應的指令碼
- [docs/RECALL_STRATEGY.md](docs/RECALL_STRATEGY.md) —— 檢索如何組裝與編列預算
- [docs/KNOWN_DEFECTS.md](docs/KNOWN_DEFECTS.md) —— 已確認的缺陷，含量測與修正方式
- [docs/DEPLOY_DEEPSEEK_HARNESS.md](docs/DEPLOY_DEEPSEEK_HARNESS.md) —— MCP 部署實作說明
- [CHANGELOG.md](CHANGELOG.md) —— 版本歷程

---

## 📄 授權條款

MIT License — see [LICENSE](LICENSE).

由 Mnemosyne OS 貢獻者共同打造。
