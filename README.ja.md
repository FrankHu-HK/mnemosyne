<p align="center">
  <img src="assets/banner.png" alt="Mnemosyne OS" width="100%">
</p>

# Mnemosyne OS

<p align="center">
  <a href="https://pypi.org/project/mnemosyne-os/">PyPI</a> ·
  <a href="https://github.com/FrankHu-HK/mnemosyne">GitHub</a> ·
  <a href="README_CN.md">中文</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/mnemosyne-os/"><img src="https://img.shields.io/badge/PyPI-mnemosyne--os-blue?style=for-the-badge" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="ライセンス: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="#-mcp-サーバー"><img src="https://img.shields.io/badge/MCP-31%20Tools-00ADD8?style=for-the-badge" alt="Model Context Protocol"></a>
  <a href="#-クイックスタート"><img src="https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge" alt="依存関係ゼロ"></a>
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

**Mnemosyne OS 8.0.0** —— 依存関係ゼロのローカルファースト AI メモリシステムです。グラフ
メモリ、マルチモーダル取り込み、リランキング、時間推論、ハッシュチェーン監査台帳、
ロスレス圧縮、そして 31 個の MCP ツールを備えています。

> **サードパーティ依存をコアで本当にゼロにしている**唯一の AI メモリエンジンです ——
> ベクターデータベース不要、LLM ランタイム不要、クラウドアカウント不要。
> `install_requires` は空リストです。ノート PC でも、サーバーでも、
> サーバーレス基盤でも同じように動作します。

**Python ライブラリ**としても、**CLI** としても、**HTTP API** としても、**MCP サーバー**としても使えます。

---

## 🚀 クイックスタート

### インストール

```bash
pip install mnemosyne-os          # コア：サードパーティ依存ゼロ
```

### 何も設定せずに記憶して想起する

```python
from mnemosyne import Memory

m = Memory()                       # 組み込みエンベッダー + ルールベース抽出器
m.add("I prefer dark mode and use vim keybindings. My name is Alice.",
      user_id="alice")

for hit in m.search("what does alice prefer", filters={"user_id": "alice"})["results"]:
    print(f"{hit['score']:.3f}  {hit['memory']}")
```

オフラインで、API キーもモデルのダウンロードもデータベースのインストールも不要です。
だからこそ次の節が成り立ちます。

### 想起をもっと強くしたくなったときにだけ、実モデルを接続する

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

各コンポーネントはそれぞれ独立して任意です。プロバイダーを構築できない場合は、組み込みの
同等実装にフォールバックし、**その事実を明示します** —— 黙って劣化することはありません：

```python
m.describe()["degraded"]
# {'llm': {'requested': 'openai', 'used': 'rules', 'reason': 'no API key configured',
#          'hint': 'Set MNEMOSYNE_LLM_OPENAI_API_KEY ...'}}
```

### あるいはコマンドラインから操作する

```bash
mnemosyne init
mnemosyne add "I prefer dark mode and vim keybindings" --user-id alice
mnemosyne search "what does alice prefer" --user-id alice
mnemosyne list  --user-id alice
mnemosyne event --limit 10
mnemosyne --agent search "preferences" --user-id alice   # ツールループ向けの JSON エンベロープ
```

### あるいは MCP として公開する

```json
{
  "mcpServers": {
    "mnemosyne": {
      "command": "python",
      "args": ["-m", "mnemosyne.webui.mcp_server",
               "--brain-dir", "./mem", "--namespace", "default"],
      "env": { "MNEMOSYNE_MCP_TOKEN": "<ランダムな 32 文字以上>" }
    }
  }
}
```

### あるいは HTTP で配信する

```bash
mnemosyne-web --port 9090          # コンソールと REST は同じポートを共有
curl -X POST http://127.0.0.1:8788/v3/memories/add/ \
  -H "Authorization: Bearer $MNEMOSYNE_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"I moved to Berlin in 2023."}],"user_id":"alice"}'
```

---

## 📊 ベンチマーク

本リポジトリに同梱されているハーネスで実測しました。再現は
`scripts/verify_recall_quality.py` と `scripts/verify_precision_recall.py` で行えます。

| ベンチマーク | スコア | 測定対象 |
| --- | --- | --- |
| LongMemEval | **96.2** | 長期にわたる会話の想起 |
| LoCoMo | **94.8** | マルチセッション対話メモリ |
| BEAM (1M) | **68.5** | 1M トークンのコンテキスト予算下での想起 |
| BEAM (10M) | **53.9** | 10M トークンのコンテキスト予算下での想起 |

スコアは 100 点満点です。

---

## 🧩 機能一覧

<table>
<tr><td><b>メモリ API</b></td><td><code>Memory</code> / <code>AsyncMemory</code> / <code>MemoryClient</code>。メソッド面は網羅的です：<code>add</code> <code>get</code> <code>get_all</code> <code>search</code> <code>update</code> <code>delete</code> <code>delete_all</code> <code>history</code> <code>reset</code> <code>close</code> <code>from_config</code>。</td></tr>
<tr><td><b>四次元スコープ</b></td><td><code>user_id</code> / <code>agent_id</code> / <code>run_id</code> / <code>app_id</code> —— <b>物理的な隔離</b>で強制されます。共有行にフィルタをかける方式ではなく、スコープごとに 1 つの SQLite ファイルを使います。</td></tr>
<tr><td><b>フィルタ言語</b></td><td><code>eq</code> <code>ne</code> <code>gt</code> <code>gte</code> <code>lt</code> <code>lte</code> <code>in</code> <code>nin</code> <code>contains</code> <code>icontains</code> <code>wildcard</code> に対応し、<code>AND</code>/<code>OR</code>/<code>NOT</code> を任意にネストできます。</td></tr>
<tr><td><b>単一パスの ADD-only 抽出</b></td><td>書き込み 1 回につきモデル呼び出し 1 回。メモリは蓄積されるだけで、上書きされることはありません。書き換えない設計なので、抽出に失敗しても持ち込まれるのはノイズだけで、実際の事実を壊すことは決してありません。</td></tr>
<tr><td><b>常時オンのグラフメモリ</b></td><td>エンティティのリンクとマルチホップ探索は同じ SQLite ファイル内にあります。外部のグラフデータベースは不要です。</td></tr>
<tr><td><b>マルチモーダル取り込み</b></td><td>OpenAI、Anthropic、Gemini の画像コンテンツ形式（および音声）を受け付けます。ビジョンモデルを構成していれば説明文を保存し、構成していなければ参照を保存します —— 何も捨てません。</td></tr>
<tr><td><b>マルチシグナル検索</b></td><td>セマンティック + BM25 キーワード + エンティティグラフ + 時間 + タグを融合し、キャリブレーション済みの関連度下限と字句フォールバックを備えています。</td></tr>
<tr><td><b>時間推論</b></td><td>観測日、相対時間の解決、有効期限のセマンティクス、そしてエンティティごとのバージョンチェーン。</td></tr>
<tr><td><b>階層メモリ</b></td><td>ホット / ウォーム / コールドの階層と忘却の経済学。価値の低いメモリは降格・圧縮され、黙って削除されることはありません。</td></tr>
<tr><td><b>ロスレス圧縮（AIC）</b></td><td>メモリを <i>ポインタ + 構造化された事実 + コンテンツアトム</i> に圧縮します。数値、日付、金額、型番はどの階層でもそのまま残り、<code>expand()</code> が元のテキストをバイト単位で復元してハッシュを検証します。</td></tr>
<tr><td><b>ハッシュチェーン監査台帳</b></td><td>SHA-256 のチェーンです。<code>verify_integrity()</code> が改ざんを検出し、変更されたエントリを正確に指し示します。</td></tr>
<tr><td><b>非同期 API とイベント</b></td><td>高スループットの書き込み向けの <code>AsyncMemory</code> に加え、永続化された操作ログにより、受理済みの書き込みがプロセスをまたいでも確認できます。</td></tr>
<tr><td><b>中国語最適化</b></td><td>Bigram トークン化 + FTS5 + 組み込みの同義語辞書、さらにラテン文字も完全にサポートします。</td></tr>
<tr><td><b>安全公証人</b></td><td>書き込みが確定する前に認証情報、不可視 Unicode、HTML インジェクションを検出し、フィールド単位でマスクします。</td></tr>
</table>

---

## 🔌 対応インテグレーション

すべてのアダプタは任意です。**stdlib** アダプタはサードパーティパッケージを一切必要としません
—— `urllib` を通じて直接 HTTP を話します。**sdk** アダプタは SDK を遅延インポートし、不足して
いるパッケージを正確に伝えます。

### LLM プロバイダー（20）

| トランスポート | プロバイダー |
| --- | --- |
| **stdlib HTTP** | `openai` `openai_structured` `azure_openai` `azure_openai_structured` `ollama` `anthropic` `gemini` `groq` `together` `deepseek` `minimax` `xai` `sarvam` `openrouter` `litellm` `lmstudio` `vllm` |
| **sdk** | `langchain` `aws_bedrock` |
| **組み込み** | `rules` —— 決定的なオフライン抽出器であり、モデルを一切構成しなくても `add()` が動く理由です |

### エンベッダー（13）

| トランスポート | プロバイダー |
| --- | --- |
| **stdlib HTTP** | `openai` `azure_openai` `ollama` `gemini` `vertexai` `together` `lmstudio` `huggingface` |
| **sdk** | `fastembed` `langchain` `aws_bedrock` |
| **組み込み** | `builtin`（128 次元、依存関係ゼロ、決定的）· `hashing`（任意の次元、オフライン） |

### ベクターストア（28）

| トランスポート | ストア |
| --- | --- |
| **組み込み** | `builtin`（1 つの SQLite ファイルがメモリとベクターの両方を保持）· `memory` · `generic`（宣言的 REST） |
| **stdlib HTTP** | `qdrant` `pinecone` `elasticsearch` `opensearch` `weaviate` `upstash_vector` `turbopuffer` |
| **sdk** | `chroma` `pgvector` `milvus` `mongodb` `redis` `valkey` `azure_ai_search` `azure_mysql` `baidu` `cassandra` `databricks` `faiss` `langchain` `neptune` `oracledb` `s3_vectors` `supabase` `vertex_ai_vector_search` |

### グラフストア（6）

`builtin`（ネイティブな SQLite トリプル）· `neo4j` · `memgraph` · `neptune` · `kuzu` · `sparql`（任意の SPARQL 1.1 エンドポイント）

### リランカー（5）

`llm` · `cohere` · `zero_entropy` · `huggingface` · `sentence_transformer`

### フレームワークアダプタ

LangChain · LlamaIndex · CrewAI · Dify · n8n · Vercel AI SDK · Ollama · MCP（stdio + Streamable HTTP）

---

## 🛠 MCP サーバー

stdio JSON-RPC で動作します：

```bash
export MNEMOSYNE_MCP_TOKEN="your-secret-token"   # 任意ですが推奨
python -m mnemosyne.webui.mcp_server --brain-dir ./mem --namespace default
```

**31 個のツール** —— 20 個のネイティブツールと、それに加えて慣例的な
エージェントメモリのツール名を再利用する 11 個のツールです。これにより、既存の MCP
クライアントはツール定義を書き換えることなく、そのまま mnemosyne に向けられます。

**ネイティブ（20）：**

| ツール | 用途 |
| --- | --- |
| `retain` | メモリを 1 件保存 |
| `recall` | メモリを検索 |
| `retain_batch` | 一括書き込み、約 15× 高速 |
| `forget` | メモリを忘れる —— id 指定、または自然言語クエリで特定して実行 |
| `capsule` | メモリをポインタ + 事実 + アトムに圧縮 |
| `expand` | カプセルの原文をバイト単位で復元 |
| `recall_health` | 読み取り専用の想起品質メトリクス |
| `consolidate` | ほぼ重複するメモリを 1 つの代表に統合 |
| `reflect` | 統計、頻出エンティティ、競合検出、認知パターン |
| `dedup` | 重複とほぼ重複を検出 |
| `graph_query` | ナレッジグラフの探索 |
| `temporal_query` | バージョンチェーンのクエリ |
| `list_projects` | 隔離されたプロジェクトの一覧 |
| `doctor` | ヘルスチェック —— 整合性、件数、ディスク、バックエンド状態 |
| `stats` | 実行時統計 |
| `audit` | 監査チェーンのクエリ |
| `confidence_history` | 信頼度の推移 |
| `memory/export-v1` | Memory Exchange Protocol によるエクスポート |
| `memory/import-v1` | Memory Exchange Protocol によるインポート |
| `memory/claim` | 外部エクスポートからメモリを引き継ぐ |

**クライアント互換（11）：**

| ツール | 用途 |
| --- | --- |
| `add_memory` | ユーザー／エージェントのテキストまたは会話履歴を保存 |
| `search_memories` | フィルタ付きのセマンティック検索 |
| `get_memories` | 構造化フィルタ + ページング付き一覧 |
| `get_memory` | id で 1 件取得 |
| `update_memory` | テキストやメタデータを上書き |
| `delete_memory` | 1 件削除 |
| `delete_all_memories` | スコープをクリア |
| `delete_entities` | エンティティを削除してカスケード |
| `list_entities` | users/agents/apps/runs を一覧 |
| `list_events` | メモリ操作を一覧 |
| `get_event_status` | 非同期操作をポーリング |

---

## 🌐 セルフホスト REST API

1 プロセス、1 ポートで、`X-API-Key`、`Bearer`、`Token` の認証ヘッダーを受け付けます。
コンソールと API は同じリスナーを共有します。

| メソッド | パス | 用途 |
| --- | --- | --- |
| `GET` | `/v1/status/` | 死活監視プローブ + 現在の構成レポート |
| `GET` | `/v1/providers/` | すべてのプロバイダーとその現在の可用性 |
| `POST` | `/v3/memories/add/` | 抽出して保存（非同期、イベント id を返す） |
| `POST` | `/v3/memories/search/` | セマンティック検索 |
| `POST` | `/v3/memories/get-all/` | フィルタ付き一覧 |
| `GET` / `PUT` / `DELETE` | `/v3/memories/{id}/` | 1 件の取得 / 更新 / 削除 |
| `DELETE` | `/v3/memories/` | スコープをクリア |
| `GET` | `/v3/memories/{id}/history/` | 変更履歴 |
| `GET` | `/v1/event/{id}/` · `/v1/events/` | 操作のポーリング / 一覧 |
| `GET` / `DELETE` | `/v2/entities/` | スコープの一覧 / 削除 |
| `POST` | `/v3/graph/{add,search,get-all,delete-all}/` | グラフメモリ |
| `POST` | `/v1/capsule/` · `/v1/expand/` | ロスレス圧縮 |
| `GET` | `/v1/integrity/` | 台帳の検証 |
| `GET` / `POST` / `DELETE` | `/v1/keys/` | API キー管理 |

---

## 🧠 Python API

```python
from mnemosyne import Memory, AsyncMemory, MemoryClient

# --- 抽出 / スコープ / フィルタ -----------------------------------------------
m = Memory()
m.add([{"role": "user", "content": "I moved to Berlin in 2023."}],
      user_id="alice", metadata={"source": "onboarding"},
      observation_date="2023-06-01")
m.add("The invoice number is INV-2024-001.", user_id="alice", immutable=True)

hits = m.search("where does the user live",
                filters={"user_id": "alice",
                         "AND": [{"source": {"eq": "onboarding"}}]},
                top_k=5, threshold=0.1, rerank=False, explain=True)

# --- マルチモーダル -----------------------------------------------------------
m.add([{"role": "user", "content": [
    {"type": "text", "text": "My new desk."},
    {"type": "image_url", "image_url": {"url": "https://example.com/desk.jpg"}},
]}], user_id="alice")

# --- グラフメモリ -------------------------------------------------------------
m.graph_add("Jobs founded Apple in Cupertino.", user_id="alice")
m.graph_search("Apple", filters={"user_id": "alice"})

# --- 非同期とイベント ---------------------------------------------------------
async def ingest():
    am = AsyncMemory()
    await am.add_many([{"messages": t, "options": {"user_id": "alice"}}
                       for t in transcripts])
```

`Memory`、`AsyncMemory`、`MemoryClient` は、他のメモリライブラリで使われている慣例的な
エージェントメモリの呼び出し形式も受け付けます。したがって、その形式で書かれた既存コードは
import を変えるだけで切り替えられます。詳細は
[docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) を参照してください。

エンジン自身の機能は同じオブジェクトから利用できます：

```python
from mnemosyne import MemoryBrain

brain = MemoryBrain("./memories", enable_embeddings=True)
brain.ensure_init()
brain.retain("His laptop is an ASUS VivoBook Pro 14", fast=True)

results = brain.recall("what are that machine's specs", k=5)
results, cost = brain.recall("that machine's specs", k=5, budget_tokens=100)

cap = brain.capsule("<memory_id>", budget_tokens=60)   # ポインタ + 事実 + アトム
brain.expand(cap["ref"])                                # バイト単位での完全復元
brain.verify_integrity()                                # SHA-256 台帳チェック
```

---

## 📂 ディレクトリ構成

```
mnemosyne/
├── api/                 # メモリ API：Memory / AsyncMemory / MemoryClient
│   ├── memory.py        #   エンジンに支えられたクライアント
│   ├── config.py        #   MemoryConfig + 次元の整合性チェック
│   ├── filters.py       #   フィルタ言語 → 述語
│   ├── extract.py       #   単一パスの ADD-only 抽出
│   ├── multimodal.py    #   画像 / 音声添付の解析
│   ├── events.py        #   永続化された操作ログ
│   └── client.py        #   組み込み + HTTP のトランスポート
├── providers/           # 任意コンポーネントのアダプタ（合計 72 個）
│   ├── llms.py          #   20 個の LLM プロバイダー
│   ├── embedders.py     #   13 個のエンベッダープロバイダー
│   ├── vector_stores.py #   28 個のベクターストア
│   ├── graph_stores.py  #   6 個のグラフストア
│   ├── rerankers.py     #   5 個のリランカー
│   ├── vision.py        #   3 種類の画像 wire format
│   └── transport.py     #   stdlib HTTP + リトライ + 認証情報のマスク
├── brain.py             # MemoryBrain —— エンジンのファサード
├── capsule.py           # AIC ロスレス圧縮
├── retrieval.py         # マルチシグナル融合と関連度のキャリブレーション
├── graph.py             # 時間的トリプルストア
├── notary.py            # 書き込み前のトラストパイプライン
├── cli.py               # ネイティブ CLI
├── api_cli.py           # クライアント API CLI
└── webui/
    ├── web_server.py    # コンソール + REST ホスト
    ├── api_routes.py    # /v1 /v2 /v3 ルート
    ├── mcp_server.py    # 20 個のネイティブ MCP ツール
    └── mcp_api.py       # 11 個のクライアント互換 MCP ツール

storage/                 # SQLite バックエンド、ハッシュチェーン台帳、プラグイン SDK
security/                # 矛盾検出、セキュリティレポート
scripts/                 # 検証スクリプト
docs/                    # 受け入れガイド、想起戦略、互換性
```

---

## ✅ テスト

```bash
python verify.py                              # セルフチェック
python scripts/verify_api.py                  # クライアント API の検証、完全オフライン
python scripts/verify_memory_lifecycle.py --brain-dir ./mem --src-root .
python scripts/verify_precision_recall.py     # オフラインの精度リグレッション
python scripts/verify_recall_quality.py       # エンドツーエンドの想起品質
```

---

## 📚 ドキュメント

- [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) —— 慣例的なエージェントメモリの呼び出し形式
- [docs/ACCEPTANCE_GUIDE.md](docs/ACCEPTANCE_GUIDE.md) —— 受け入れ基準と、その判定スクリプト
- [docs/RECALL_STRATEGY.md](docs/RECALL_STRATEGY.md) —— 検索がどのように組み立てられ、予算配分されるか
- [docs/KNOWN_DEFECTS.md](docs/KNOWN_DEFECTS.md) —— 確認済みの不具合、実測値と修正方法
- [docs/DEPLOY_DEEPSEEK_HARNESS.md](docs/DEPLOY_DEEPSEEK_HARNESS.md) —— MCP デプロイの実践ガイド
- [CHANGELOG.md](CHANGELOG.md) —— バージョン履歴

---

## 📄 ライセンス

MIT License — see [LICENSE](LICENSE).

Mnemosyne OS のコントリビューターによって構築されました。
