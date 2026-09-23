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
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="라이선스: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="#-mcp-서버"><img src="https://img.shields.io/badge/MCP-31%20Tools-00ADD8?style=for-the-badge" alt="모델 컨텍스트 프로토콜"></a>
  <a href="#-빠른-시작"><img src="https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge" alt="의존성 제로"></a>
  <a href="https://pepy.tech/projects/mnemosyne-os"><img src="https://img.shields.io/pepy/dt/mnemosyne-os?style=for-the-badge" alt="다운로드"></a>
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

**Mnemosyne OS 8.0.0** — 의존성 제로, 로컬 우선(local-first) AI 메모리 시스템입니다.
그래프 메모리, 멀티모달 인제스천, 재정렬(reranking), 시간 추론, 해시 체인 감사
원장, 무손실 압축, 그리고 31개의 MCP 도구를 제공합니다.

> **핵심이 실제로 서드파티 의존성을 전혀 갖지 않는** 유일한 AI 메모리 엔진입니다
> — 벡터 데이터베이스도, LLM 런타임도, 클라우드 계정도 필요하지 않습니다.
> `install_requires`는 빈 리스트입니다. 노트북에서도, 서버에서도, 서버리스
> 인프라에서도 동일하게 동작합니다.

**Python 라이브러리**, **CLI**, **HTTP API**, **MCP 서버**로 사용할 수 있습니다.

---

## 🚀 빠른 시작

### 설치

```bash
pip install mnemosyne-os          # core: zero third-party dependencies
```

### 아무것도 설정하지 않고 기억하고 불러오기

```python
from mnemosyne import Memory

m = Memory()                       # built-in embedder + rule-based extractor
m.add("I prefer dark mode and use vim keybindings. My name is Alice.",
      user_id="alice")

for hit in m.search("what does alice prefer", filters={"user_id": "alice"})["results"]:
    print(f"{hit['score']:.3f}  {hit['memory']}")
```

오프라인으로 동작하고, API 키도, 모델 다운로드도, 설치할 데이터베이스도 필요하지
않습니다 — 그래서 다음 절이 가능합니다.

### 리콜이 더 강해져야 할 때만 실제 모델을 연결하기

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

모든 컴포넌트는 각각 독립적으로 선택 사항입니다. 프로바이더를 구성할 수 없으면
내장 동등 구현으로 폴백하고 **그 사실을 알려줍니다** — 어떤 것도 조용히 성능이
저하되지 않습니다:

```python
m.describe()["degraded"]
# {'llm': {'requested': 'openai', 'used': 'rules', 'reason': 'no API key configured',
#          'hint': 'Set MNEMOSYNE_LLM_OPENAI_API_KEY ...'}}
```

### 또는 명령줄에서 실행하기

```bash
mnemosyne init
mnemosyne add "I prefer dark mode and vim keybindings" --user-id alice
mnemosyne search "what does alice prefer" --user-id alice
mnemosyne list  --user-id alice
mnemosyne event --limit 10
mnemosyne --agent search "preferences" --user-id alice   # JSON envelope for tool loops
```

### 또는 MCP로 노출하기

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

### 또는 HTTP로 제공하기

```bash
mnemosyne-web --port 9090          # console and REST share one port
curl -X POST http://127.0.0.1:8788/v3/memories/add/ \
  -H "Authorization: Bearer $MNEMOSYNE_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"I moved to Berlin in 2023."}],"user_id":"alice"}'
```

---

## 📊 벤치마크

이 저장소에 함께 실려 있는 하네스로 측정했습니다. 재현에는
`scripts/verify_recall_quality.py`와 `scripts/verify_precision_recall.py`를
사용합니다.

| 벤치마크 | 점수 | 측정 대상 |
| --- | --- | --- |
| LongMemEval | **96.2** | 장기 대화 리콜 |
| LoCoMo | **94.8** | 멀티 세션 대화 메모리 |
| BEAM (1M) | **68.5** | 1M 토큰 컨텍스트 예산에서의 리콜 |
| BEAM (10M) | **53.9** | 10M 토큰 컨텍스트 예산에서의 리콜 |

점수는 100점 만점입니다.

---

## 🧩 기능

<table>
<tr><td><b>메모리 API</b></td><td>완전한 메서드 표면을 갖춘 <code>Memory</code> / <code>AsyncMemory</code> / <code>MemoryClient</code>: <code>add</code> <code>get</code> <code>get_all</code> <code>search</code> <code>update</code> <code>delete</code> <code>delete_all</code> <code>history</code> <code>reset</code> <code>close</code> <code>from_config</code>.</td></tr>
<tr><td><b>4차원 스코핑</b></td><td><code>user_id</code> / <code>agent_id</code> / <code>run_id</code> / <code>app_id</code> — <b>물리적 격리</b>로 강제합니다. 공유 행에 필터를 적용하는 방식이 아니라 스코프마다 하나의 SQLite 파일을 사용합니다.</td></tr>
<tr><td><b>필터 언어</b></td><td><code>eq</code> <code>ne</code> <code>gt</code> <code>gte</code> <code>lt</code> <code>lte</code> <code>in</code> <code>nin</code> <code>contains</code> <code>icontains</code> <code>wildcard</code>, 그리고 <code>AND</code>/<code>OR</code>/<code>NOT</code>의 임의 중첩을 지원합니다.</td></tr>
<tr><td><b>단일 패스 ADD-only 추출</b></td><td>쓰기 한 번에 모델 호출 한 번이며, 메모리는 누적되기만 하고 덮어써지지 않습니다. 재작성이 없기 때문에 잘못된 추출은 노이즈를 더할 뿐이며, 실제 사실을 파괴할 수는 없습니다.</td></tr>
<tr><td><b>그래프 메모리 상시 활성</b></td><td>엔티티 링킹과 멀티홉 순회가 동일한 SQLite 파일 안에 있습니다. 외부 그래프 데이터베이스가 필요하지 않습니다.</td></tr>
<tr><td><b>멀티모달 인제스천</b></td><td>OpenAI, Anthropic, Gemini의 이미지 콘텐츠 형식을 받아들이며 오디오도 지원합니다. 비전 모델을 구성하면 설명을 저장하고, 구성하지 않으면 참조를 저장합니다 — 아무것도 버려지지 않습니다.</td></tr>
<tr><td><b>다중 신호 검색</b></td><td>시맨틱 + BM25 키워드 + 엔티티 그래프 + 시간 + 태그를 결합하고, 보정된 관련성 하한과 어휘 기반 폴백을 함께 사용합니다.</td></tr>
<tr><td><b>시간 추론</b></td><td>관측 날짜, 상대 시간 해석, 만료 시맨틱, 그리고 엔티티별 버전 체인.</td></tr>
<tr><td><b>계층형 메모리</b></td><td>핫 / 웜 / 콜드 계층과 망각 경제학: 저가치 메모리는 강등되어 압축되며, 조용히 삭제되지 않습니다.</td></tr>
<tr><td><b>무손실 압축(AIC)</b></td><td>메모리를 <i>포인터 + 구조화된 사실 + 콘텐츠 원자</i>로 압축합니다. 숫자, 날짜, 금액, 모델 번호는 모든 계층에서 그대로 보존되며, <code>expand()</code>는 원문을 바이트 단위로 복원하고 해시를 검증합니다.</td></tr>
<tr><td><b>해시 체인 감사 원장</b></td><td>SHA-256 체인이며, <code>verify_integrity()</code>가 변조를 감지하고 변경된 정확한 항목을 지목합니다.</td></tr>
<tr><td><b>비동기 API와 이벤트</b></td><td>고처리량 쓰기를 위한 <code>AsyncMemory</code>, 그리고 수락된 쓰기가 프로세스 간에도 보이도록 하는 영속 작업 로그를 제공합니다.</td></tr>
<tr><td><b>중국어 최적화</b></td><td>바이그램 토큰화 + FTS5 + 내장 동의어 사전을 사용하며, 라틴 문자도 완전히 지원합니다.</td></tr>
<tr><td><b>안전 공증기</b></td><td>쓰기가 반영되기 전에 자격 증명, 보이지 않는 유니코드, HTML 인젝션을 탐지하고 필드 수준에서 마스킹합니다.</td></tr>
</table>

---

## 🔌 통합

모든 어댑터는 선택 사항입니다. **stdlib** 어댑터는 서드파티 패키지가 전혀 필요하지
않습니다 — `urllib`로 HTTP를 직접 사용합니다. **sdk** 어댑터는 SDK를 지연 임포트하며
어떤 패키지가 없는지 정확히 알려줍니다.

### LLM 프로바이더(20)

| 전송 방식 | 프로바이더 |
| --- | --- |
| **stdlib HTTP** | `openai` `openai_structured` `azure_openai` `azure_openai_structured` `ollama` `anthropic` `gemini` `groq` `together` `deepseek` `minimax` `xai` `sarvam` `openrouter` `litellm` `lmstudio` `vllm` |
| **sdk** | `langchain` `aws_bedrock` |
| **내장** | `rules` — 결정적 오프라인 추출기이며, 그래서 모델을 전혀 구성하지 않아도 `add()`가 동작합니다 |

### 임베더(13)

| 전송 방식 | 프로바이더 |
| --- | --- |
| **stdlib HTTP** | `openai` `azure_openai` `ollama` `gemini` `vertexai` `together` `lmstudio` `huggingface` |
| **sdk** | `fastembed` `langchain` `aws_bedrock` |
| **내장** | `builtin`(128차원, 의존성 제로, 결정적) · `hashing`(임의 차원, 오프라인) |

### 벡터 스토어(28)

| 전송 방식 | 스토어 |
| --- | --- |
| **임베디드** | `builtin`(하나의 SQLite 파일이 메모리와 벡터를 모두 보관) · `memory` · `generic`(선언적 REST) |
| **stdlib HTTP** | `qdrant` `pinecone` `elasticsearch` `opensearch` `weaviate` `upstash_vector` `turbopuffer` |
| **sdk** | `chroma` `pgvector` `milvus` `mongodb` `redis` `valkey` `azure_ai_search` `azure_mysql` `baidu` `cassandra` `databricks` `faiss` `langchain` `neptune` `oracledb` `s3_vectors` `supabase` `vertex_ai_vector_search` |

### 그래프 스토어(6)

`builtin`(네이티브 SQLite 트리플) · `neo4j` · `memgraph` · `neptune` · `kuzu` · `sparql`(모든 SPARQL 1.1 엔드포인트)

### 리랭커(5)

`llm` · `cohere` · `zero_entropy` · `huggingface` · `sentence_transformer`

### 프레임워크 어댑터

LangChain · LlamaIndex · CrewAI · Dify · n8n · Vercel AI SDK · Ollama · MCP(stdio + Streamable HTTP)

---

## 🛠 MCP 서버

stdio JSON-RPC로 동작합니다:

```bash
export MNEMOSYNE_MCP_TOKEN="your-secret-token"   # optional, but recommended
python -m mnemosyne.webui.mcp_server --brain-dir ./mem --namespace default
```

**31개 도구** — 네이티브 20개에, 관용적인 에이전트 메모리 도구 이름을 그대로 쓰는
11개를 더한 구성입니다. 따라서 기존 MCP 클라이언트는 도구 정의를 다시 작성하지
않고도 Mnemosyne OS를 가리키도록 설정할 수 있습니다.

**네이티브(20):**

| 도구 | 용도 |
| --- | --- |
| `retain` | 메모리 하나를 저장합니다 |
| `recall` | 메모리를 검색합니다 |
| `retain_batch` | 대량 쓰기, 약 15배 빠릅니다 |
| `forget` | 메모리를 망각합니다 — id로 지정하거나 자연어 질의로 찾아서 지정할 수 있습니다 |
| `capsule` | 메모리를 포인터 + 사실 + 원자로 압축합니다 |
| `expand` | 캡슐의 원문을 바이트 단위로 복원합니다 |
| `recall_health` | 읽기 전용 리콜 품질 지표 |
| `consolidate` | 거의 중복인 메모리를 하나의 대표로 병합합니다 |
| `reflect` | 통계, 빈출 엔티티, 충돌 탐지, 인지 패턴 |
| `dedup` | 중복과 거의 중복을 탐지합니다 |
| `graph_query` | 지식 그래프 순회 |
| `temporal_query` | 버전 체인 질의 |
| `list_projects` | 격리된 프로젝트를 나열합니다 |
| `doctor` | 상태 점검 — 무결성, 개수, 디스크, 백엔드 상태 |
| `stats` | 런타임 통계 |
| `audit` | 감사 체인 질의 |
| `confidence_history` | 신뢰도 추이 |
| `memory/export-v1` | Memory Exchange Protocol로 내보내기 |
| `memory/import-v1` | Memory Exchange Protocol로 가져오기 |
| `memory/claim` | 외부 내보내기에서 메모리를 인수합니다 |

**클라이언트 호환(11):**

| 도구 | 용도 |
| --- | --- |
| `add_memory` | 사용자/에이전트의 텍스트 또는 대화 기록을 저장합니다 |
| `search_memories` | 필터를 사용한 시맨틱 검색 |
| `get_memories` | 구조화 필터 + 페이지네이션 목록 |
| `get_memory` | id로 하나를 조회합니다 |
| `update_memory` | 텍스트 및/또는 메타데이터를 덮어씁니다 |
| `delete_memory` | 하나를 삭제합니다 |
| `delete_all_memories` | 스코프를 비웁니다 |
| `delete_entities` | 엔티티를 삭제하고 연쇄 처리합니다 |
| `list_entities` | users/agents/apps/runs를 나열합니다 |
| `list_events` | 메모리 작업을 나열합니다 |
| `get_event_status` | 비동기 작업을 폴링합니다 |

---

## 🌐 셀프 호스팅 REST API

하나의 프로세스, 하나의 포트로 동작하며 `X-API-Key`, `Bearer`, `Token` 인증
헤더를 모두 받습니다. 콘솔과 API는 같은 리스너를 공유합니다.

| 메서드 | 경로 | 용도 |
| --- | --- | --- |
| `GET` | `/v1/status/` | 라이브니스 프로브 + 실시간 구성 리포트 |
| `GET` | `/v1/providers/` | 모든 프로바이더와 현재 가용성 |
| `POST` | `/v3/memories/add/` | 추출 후 저장(비동기, 이벤트 id 반환) |
| `POST` | `/v3/memories/search/` | 시맨틱 검색 |
| `POST` | `/v3/memories/get-all/` | 필터가 적용된 목록 |
| `GET` / `PUT` / `DELETE` | `/v3/memories/{id}/` | 하나 조회 / 수정 / 삭제 |
| `DELETE` | `/v3/memories/` | 스코프 비우기 |
| `GET` | `/v3/memories/{id}/history/` | 변경 이력 |
| `GET` | `/v1/event/{id}/` · `/v1/events/` | 작업 폴링 / 목록 |
| `GET` / `DELETE` | `/v2/entities/` | 스코프 나열 / 삭제 |
| `POST` | `/v3/graph/{add,search,get-all,delete-all}/` | 그래프 메모리 |
| `POST` | `/v1/capsule/` · `/v1/expand/` | 무손실 압축 |
| `GET` | `/v1/integrity/` | 원장 검증 |
| `GET` / `POST` / `DELETE` | `/v1/keys/` | API 키 관리 |

---

## 🧠 Python API

```python
from mnemosyne import Memory, AsyncMemory, MemoryClient

# --- extraction / scope / filters ---------------------------------------------
m = Memory()
m.add([{"role": "user", "content": "I moved to Berlin in 2023."}],
      user_id="alice", metadata={"source": "onboarding"},
      observation_date="2023-06-01")
m.add("The invoice number is INV-2024-001.", user_id="alice", immutable=True)

hits = m.search("where does the user live",
                filters={"user_id": "alice",
                         "AND": [{"source": {"eq": "onboarding"}}]},
                top_k=5, threshold=0.1, rerank=False, explain=True)

# --- multimodal ---------------------------------------------------------------
m.add([{"role": "user", "content": [
    {"type": "text", "text": "My new desk."},
    {"type": "image_url", "image_url": {"url": "https://example.com/desk.jpg"}},
]}], user_id="alice")

# --- graph memory -------------------------------------------------------------
m.graph_add("Jobs founded Apple in Cupertino.", user_id="alice")
m.graph_search("Apple", filters={"user_id": "alice"})

# --- async and events ---------------------------------------------------------
async def ingest():
    am = AsyncMemory()
    await am.add_many([{"messages": t, "options": {"user_id": "alice"}}
                       for t in transcripts])
```

`Memory`, `AsyncMemory`, `MemoryClient`는 다른 메모리 라이브러리가 사용하는
관용적인 에이전트 메모리 호출 형태도 함께 받아들입니다. 따라서 그 형태에 맞춰
작성된 코드는 import만 바꾸면 전환할 수 있습니다.
[docs/COMPATIBILITY.md](docs/COMPATIBILITY.md)를 참고하십시오.

엔진 자체의 기능도 같은 객체에 붙어 있습니다:

```python
from mnemosyne import MemoryBrain

brain = MemoryBrain("./memories", enable_embeddings=True)
brain.ensure_init()
brain.retain("His laptop is an ASUS VivoBook Pro 14", fast=True)

results = brain.recall("what are that machine's specs", k=5)
results, cost = brain.recall("that machine's specs", k=5, budget_tokens=100)

cap = brain.capsule("<memory_id>", budget_tokens=60)   # pointer + facts + atoms
brain.expand(cap["ref"])                                # byte-exact recovery
brain.verify_integrity()                                # SHA-256 ledger check
```

---

## 📂 디렉터리 구조

```
mnemosyne/
├── api/                 # the memory API: Memory / AsyncMemory / MemoryClient
│   ├── memory.py        #   engine-backed client
│   ├── config.py        #   MemoryConfig + dimension consistency checks
│   ├── filters.py       #   filter language -> predicates
│   ├── extract.py       #   single-pass ADD-only extraction
│   ├── multimodal.py    #   image / audio attachment parsing
│   ├── events.py        #   persisted operation log
│   └── client.py        #   embedded + HTTP transports
├── providers/           # optional component adapters (72 in total)
│   ├── llms.py          #   20 LLM providers
│   ├── embedders.py     #   13 embedder providers
│   ├── vector_stores.py #   28 vector stores
│   ├── graph_stores.py  #   6 graph stores
│   ├── rerankers.py     #   5 rerankers
│   ├── vision.py        #   three image wire formats
│   └── transport.py     #   stdlib HTTP + retries + credential redaction
├── brain.py             # MemoryBrain — the engine facade
├── capsule.py           # AIC lossless compression
├── retrieval.py         # multi-signal fusion and relevance calibration
├── graph.py             # temporal triple store
├── notary.py            # pre-write trust pipeline
├── cli.py               # native CLI
├── api_cli.py           # client-API CLI
└── webui/
    ├── web_server.py    # console + REST host
    ├── api_routes.py    # /v1 /v2 /v3 routes
    ├── mcp_server.py    # 20 native MCP tools
    └── mcp_api.py       # 11 client-compatible MCP tools

storage/                 # SQLite backend, hash-chained ledger, plugin SDK
security/                # contradiction detection, security reporting
scripts/                 # verification scripts
docs/                    # acceptance guide, recall strategy, compatibility
```

---

## ✅ 테스트

```bash
python verify.py                              # self-check
python scripts/verify_api.py                  # client API verification, fully offline
python scripts/verify_memory_lifecycle.py --brain-dir ./mem --src-root .
python scripts/verify_precision_recall.py     # offline precision regression
python scripts/verify_recall_quality.py       # end-to-end recall quality
```

---

## 📚 문서

- [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) — 관용적인 에이전트 메모리 호출 형태
- [docs/ACCEPTANCE_GUIDE.md](docs/ACCEPTANCE_GUIDE.md) — 인수 기준과 각 기준에 대응하는 스크립트
- [docs/RECALL_STRATEGY.md](docs/RECALL_STRATEGY.md) — 검색이 어떻게 조립되고 예산이 배분되는지
- [docs/KNOWN_DEFECTS.md](docs/KNOWN_DEFECTS.md) — 확인된 결함, 측정치와 수정 방법 포함
- [docs/DEPLOY_DEEPSEEK_HARNESS.md](docs/DEPLOY_DEEPSEEK_HARNESS.md) — MCP 배포 실습 안내
- [CHANGELOG.md](CHANGELOG.md) — 버전 이력

---

## 📄 라이선스

MIT License — see [LICENSE](LICENSE).

Mnemosyne OS 기여자들이 만들었습니다.
