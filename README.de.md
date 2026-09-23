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
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="Lizenz: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="#-mcp-server"><img src="https://img.shields.io/badge/MCP-31%20Tools-00ADD8?style=for-the-badge" alt="Model Context Protocol"></a>
  <a href="#-schnellstart"><img src="https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge" alt="Keine Abhängigkeiten"></a>
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

**Mnemosyne OS 8.0.0** — ein abhängigkeitsfreies, lokal arbeitendes KI-Gedächtnissystem.
Graph-Gedächtnis, multimodale Ingestion, Reranking, temporales Reasoning, ein
hash-verkettetes Audit-Ledger, verlustfreie Kompression und 31 MCP-Tools.

> Die einzige KI-Gedächtnis-Engine, deren **Kern tatsächlich ohne jegliche
> Drittanbieter-Abhängigkeiten auskommt** — keine Vektordatenbank, keine LLM-Runtime,
> kein Cloud-Konto. `install_requires` ist eine leere Liste. Sie läuft auf einem
> Laptop, einem Server oder in serverloser Infrastruktur gleichermaßen.

Einsetzbar als **Python-Bibliothek**, **CLI**, **HTTP-API** oder **MCP-Server**.

---

## 🚀 Schnellstart

### Installation

```bash
pip install mnemosyne-os          # Kern: keine Drittanbieter-Abhängigkeiten
```

### Merken und wiederfinden, ohne irgendetwas zu konfigurieren

```python
from mnemosyne import Memory

m = Memory()                       # eingebauter Embedder + regelbasierter Extraktor
m.add("I prefer dark mode and use vim keybindings. My name is Alice.",
      user_id="alice")

for hit in m.search("what does alice prefer", filters={"user_id": "alice"})["results"]:
    print(f"{hit['score']:.3f}  {hit['memory']}")
```

Offline, kein API-Key, kein Modell-Download, keine Datenbank zu installieren — und
genau das macht den nächsten Abschnitt möglich.

### Echte Modelle erst anhängen, wenn das Recall stärker werden muss

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

Jede Komponente ist unabhängig optional. Lässt sich ein Provider nicht aufbauen,
fällt das System auf die eingebaute Entsprechung zurück und **sagt das auch** —
nichts degradiert stillschweigend:

```python
m.describe()["degraded"]
# {'llm': {'requested': 'openai', 'used': 'rules', 'reason': 'no API key configured',
#          'hint': 'Set MNEMOSYNE_LLM_OPENAI_API_KEY ...'}}
```

### Oder alles über die Kommandozeile steuern

```bash
mnemosyne init
mnemosyne add "I prefer dark mode and vim keybindings" --user-id alice
mnemosyne search "what does alice prefer" --user-id alice
mnemosyne list  --user-id alice
mnemosyne event --limit 10
mnemosyne --agent search "preferences" --user-id alice   # JSON-Envelope für Tool-Schleifen
```

### Oder über MCP bereitstellen

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

### Oder über HTTP ausliefern

```bash
mnemosyne-web --port 9090          # Konsole und REST teilen sich einen Port
curl -X POST http://127.0.0.1:8788/v3/memories/add/ \
  -H "Authorization: Bearer $MNEMOSYNE_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"I moved to Berlin in 2023."}],"user_id":"alice"}'
```

---

## 📊 Benchmarks

Gemessen mit der in diesem Repository mitgelieferten Harness. Reproduzierbar mit
`scripts/verify_recall_quality.py` und `scripts/verify_precision_recall.py`.

| Benchmark | Score | Was gemessen wird |
| --- | --- | --- |
| LongMemEval | **96.2** | Recall in langen Gesprächsverläufen |
| LoCoMo | **94.8** | Gedächtnis über mehrere Sitzungen hinweg |
| BEAM (1M) | **68.5** | Recall unter einem Kontextbudget von 1M Tokens |
| BEAM (10M) | **53.9** | Recall unter einem Kontextbudget von 10M Tokens |

Die Werte gehen bis 100.

---

## 🧩 Funktionen

<table>
<tr><td><b>Memory-API</b></td><td><code>Memory</code> / <code>AsyncMemory</code> / <code>MemoryClient</code> mit vollständiger Methodenfläche: <code>add</code> <code>get</code> <code>get_all</code> <code>search</code> <code>update</code> <code>delete</code> <code>delete_all</code> <code>history</code> <code>reset</code> <code>close</code> <code>from_config</code>.</td></tr>
<tr><td><b>Vierdimensionale Abgrenzung</b></td><td><code>user_id</code> / <code>agent_id</code> / <code>run_id</code> / <code>app_id</code> — durchgesetzt über <b>physische Isolation</b>: eine SQLite-Datei pro Scope statt gemeinsamer Zeilen mit angewendetem Filter.</td></tr>
<tr><td><b>Filtersprache</b></td><td><code>eq</code> <code>ne</code> <code>gt</code> <code>gte</code> <code>lt</code> <code>lte</code> <code>in</code> <code>nin</code> <code>contains</code> <code>icontains</code> <code>wildcard</code>, mit beliebig verschachteltem <code>AND</code>/<code>OR</code>/<code>NOT</code>.</td></tr>
<tr><td><b>Einmalige ADD-only-Extraktion</b></td><td>Ein Modellaufruf pro Schreibvorgang; Erinnerungen sammeln sich an und werden nie überschrieben. Weil nichts neu geschrieben wird, erzeugt eine schlechte Extraktion nur Rauschen — sie kann niemals eine echte Tatsache zerstören.</td></tr>
<tr><td><b>Graph-Gedächtnis, immer aktiv</b></td><td>Entity-Linking und Multi-Hop-Traversierung liegen in derselben SQLite-Datei. Keine externe Graphdatenbank erforderlich.</td></tr>
<tr><td><b>Multimodale Ingestion</b></td><td>Akzeptiert die Bild-Content-Formate von OpenAI, Anthropic und Gemini (plus Audio). Mit konfiguriertem Vision-Modell wird eine Beschreibung gespeichert; ohne eines die Referenz — nichts geht verloren.</td></tr>
<tr><td><b>Multi-Signal-Retrieval</b></td><td>Semantik + BM25-Keywords + Entity-Graph + Temporal + Tag, fusioniert mit kalibrierten Relevanzschwellen und einem lexikalischen Fallback.</td></tr>
<tr><td><b>Temporales Reasoning</b></td><td>Beobachtungsdaten, Auflösung relativer Zeitangaben, Ablauf-Semantik und Versionsketten pro Entity.</td></tr>
<tr><td><b>Gestuftes Gedächtnis</b></td><td>Hot- / Warm- / Cold-Stufen mit Vergessens-Ökonomie: Erinnerungen mit geringem Wert werden herabgestuft und komprimiert, aber nie stillschweigend gelöscht.</td></tr>
<tr><td><b>Verlustfreie Kompression (AIC)</b></td><td>Komprimiert eine Erinnerung zu <i>Pointer + strukturierten Fakten + Content-Atomen</i>. Zahlen, Daten, Beträge und Modellnummern bleiben in jeder Stufe erhalten; <code>expand()</code> rekonstruiert den Originaltext byteweise und verifiziert seinen Hash.</td></tr>
<tr><td><b>Hash-verkettetes Audit-Ledger</b></td><td>Eine SHA-256-Kette; <code>verify_integrity()</code> erkennt Manipulationen und benennt den genauen Eintrag, der verändert wurde.</td></tr>
<tr><td><b>Async-API und Events</b></td><td><code>AsyncMemory</code> für Schreibvorgänge mit hohem Durchsatz, dazu ein persistiertes Operationsprotokoll, sodass ein akzeptierter Schreibvorgang prozessübergreifend sichtbar bleibt.</td></tr>
<tr><td><b>Für Chinesisch optimiert</b></td><td>Bigram-Tokenisierung + FTS5 + integriertes Synonymwörterbuch, mit vollständiger Unterstützung lateinischer Schrift.</td></tr>
<tr><td><b>Sicherheits-Notar</b></td><td>Erkennt Zugangsdaten, unsichtbares Unicode und HTML-Injection, bevor ein Schreibvorgang durchgeht, und redigiert auf Feldebene.</td></tr>
</table>

---

## 🔌 Integrationen

Jeder Adapter ist optional. **stdlib**-Adapter brauchen überhaupt kein
Drittanbieter-Paket — sie sprechen HTTP direkt über `urllib`. **sdk**-Adapter
importieren ihr SDK lazy und sagen genau, welches Paket fehlt.

### LLM-Provider (20)

| Transport | Provider |
| --- | --- |
| **stdlib HTTP** | `openai` `openai_structured` `azure_openai` `azure_openai_structured` `ollama` `anthropic` `gemini` `groq` `together` `deepseek` `minimax` `xai` `sarvam` `openrouter` `litellm` `lmstudio` `vllm` |
| **sdk** | `langchain` `aws_bedrock` |
| **integriert** | `rules` — ein deterministischer Offline-Extraktor, weshalb `add()` auch ganz ohne konfiguriertes Modell funktioniert |

### Embedder (13)

| Transport | Provider |
| --- | --- |
| **stdlib HTTP** | `openai` `azure_openai` `ollama` `gemini` `vertexai` `together` `lmstudio` `huggingface` |
| **sdk** | `fastembed` `langchain` `aws_bedrock` |
| **integriert** | `builtin` (128-dim, ohne Abhängigkeiten, deterministisch) · `hashing` (beliebige Dimension, offline) |

### Vektorspeicher (28)

| Transport | Speicher |
| --- | --- |
| **eingebettet** | `builtin` (eine SQLite-Datei hält Erinnerungen und Vektoren) · `memory` · `generic` (deklaratives REST) |
| **stdlib HTTP** | `qdrant` `pinecone` `elasticsearch` `opensearch` `weaviate` `upstash_vector` `turbopuffer` |
| **sdk** | `chroma` `pgvector` `milvus` `mongodb` `redis` `valkey` `azure_ai_search` `azure_mysql` `baidu` `cassandra` `databricks` `faiss` `langchain` `neptune` `oracledb` `s3_vectors` `supabase` `vertex_ai_vector_search` |

### Graphspeicher (6)

`builtin` (native SQLite-Tripel) · `neo4j` · `memgraph` · `neptune` · `kuzu` · `sparql` (jeder SPARQL-1.1-Endpunkt)

### Reranker (5)

`llm` · `cohere` · `zero_entropy` · `huggingface` · `sentence_transformer`

### Framework-Adapter

LangChain · LlamaIndex · CrewAI · Dify · n8n · Vercel AI SDK · Ollama · MCP (stdio + Streamable HTTP)

---

## 🛠 MCP-Server

Läuft über stdio JSON-RPC:

```bash
export MNEMOSYNE_MCP_TOKEN="your-secret-token"   # optional, aber empfohlen
python -m mnemosyne.webui.mcp_server --brain-dir ./mem --namespace default
```

**31 Tools** — zwanzig native plus elf, die die üblichen Tool-Namen aus dem
Agent-Memory-Umfeld wiederverwenden, sodass ein bestehender MCP-Client auf
Mnemosyne OS gerichtet werden kann, ohne seine Tool-Definitionen umzuschreiben.

**Native (20):**

| Tool | Zweck |
| --- | --- |
| `retain` | Eine Erinnerung speichern |
| `recall` | Erinnerungen abrufen |
| `retain_batch` | Massen-Schreibvorgang, rund 15× schneller |
| `forget` | Eine Erinnerung vergessen — per id oder indem man sie über eine natürlichsprachliche Abfrage lokalisiert |
| `capsule` | Eine Erinnerung zu Pointer + Fakten + Atomen komprimieren |
| `expand` | Den Originaltext einer Kapsel byteweise rekonstruieren |
| `recall_health` | Schreibgeschützte Metriken zur Recall-Qualität |
| `consolidate` | Nahezu doppelte Erinnerungen zu einem Repräsentanten zusammenführen |
| `reflect` | Statistiken, häufige Entities, Konflikterkennung, kognitive Muster |
| `dedup` | Duplikate und Beinahe-Duplikate erkennen |
| `graph_query` | Traversierung des Wissensgraphen |
| `temporal_query` | Abfragen auf Versionsketten |
| `list_projects` | Isolierte Projekte auflisten |
| `doctor` | Health-Check — Integrität, Anzahl, Speicherplatz, Backend-Status |
| `stats` | Laufzeitstatistiken |
| `audit` | Abfragen auf die Audit-Kette |
| `confidence_history` | Konfidenzverläufe |
| `memory/export-v1` | Export über das Memory Exchange Protocol |
| `memory/import-v1` | Import über das Memory Exchange Protocol |
| `memory/claim` | Erinnerungen aus einem externen Export übernehmen |

**Client-kompatibel (11):**

| Tool | Zweck |
| --- | --- |
| `add_memory` | Text oder Gesprächsverlauf für einen Nutzer/Agenten speichern |
| `search_memories` | Semantische Suche mit Filtern |
| `get_memories` | Strukturierter Filter + paginierte Auflistung |
| `get_memory` | Einen Eintrag per id abrufen |
| `update_memory` | Text und/oder Metadaten überschreiben |
| `delete_memory` | Einen Eintrag löschen |
| `delete_all_memories` | Einen Scope leeren |
| `delete_entities` | Entities löschen und kaskadieren |
| `list_entities` | users/agents/apps/runs auflisten |
| `list_events` | Gedächtnis-Operationen auflisten |
| `get_event_status` | Eine asynchrone Operation pollen |

---

## 🌐 Selbst gehostete REST-API

Ein Prozess, ein Port, akzeptiert die Auth-Header `X-API-Key`, `Bearer` und
`Token`. Konsole und API teilen sich denselben Listener.

| Methode | Pfad | Zweck |
| --- | --- | --- |
| `GET` | `/v1/status/` | Liveness-Probe + Live-Konfigurationsbericht |
| `GET` | `/v1/providers/` | Jeder Provider und seine aktuelle Verfügbarkeit |
| `POST` | `/v3/memories/add/` | Extrahieren und speichern (asynchron, liefert eine Event-id) |
| `POST` | `/v3/memories/search/` | Semantische Suche |
| `POST` | `/v3/memories/get-all/` | Gefilterte Auflistung |
| `GET` / `PUT` / `DELETE` | `/v3/memories/{id}/` | Einen Eintrag abrufen / aktualisieren / löschen |
| `DELETE` | `/v3/memories/` | Einen Scope leeren |
| `GET` | `/v3/memories/{id}/history/` | Änderungsverlauf |
| `GET` | `/v1/event/{id}/` · `/v1/events/` | Operationen pollen / auflisten |
| `GET` / `DELETE` | `/v2/entities/` | Scopes auflisten / löschen |
| `POST` | `/v3/graph/{add,search,get-all,delete-all}/` | Graph-Gedächtnis |
| `POST` | `/v1/capsule/` · `/v1/expand/` | Verlustfreie Kompression |
| `GET` | `/v1/integrity/` | Ledger-Verifikation |
| `GET` / `POST` / `DELETE` | `/v1/keys/` | API-Key-Verwaltung |

---

## 🧠 Python API

```python
from mnemosyne import Memory, AsyncMemory, MemoryClient

# --- Extraktion / Scope / Filter ----------------------------------------------
m = Memory()
m.add([{"role": "user", "content": "I moved to Berlin in 2023."}],
      user_id="alice", metadata={"source": "onboarding"},
      observation_date="2023-06-01")
m.add("The invoice number is INV-2024-001.", user_id="alice", immutable=True)

hits = m.search("where does the user live",
                filters={"user_id": "alice",
                         "AND": [{"source": {"eq": "onboarding"}}]},
                top_k=5, threshold=0.1, rerank=False, explain=True)

# --- Multimodal ---------------------------------------------------------------
m.add([{"role": "user", "content": [
    {"type": "text", "text": "My new desk."},
    {"type": "image_url", "image_url": {"url": "https://example.com/desk.jpg"}},
]}], user_id="alice")

# --- Graph-Gedächtnis ---------------------------------------------------------
m.graph_add("Jobs founded Apple in Cupertino.", user_id="alice")
m.graph_search("Apple", filters={"user_id": "alice"})

# --- Async und Events ---------------------------------------------------------
async def ingest():
    am = AsyncMemory()
    await am.add_many([{"messages": t, "options": {"user_id": "alice"}}
                       for t in transcripts])
```

`Memory`, `AsyncMemory` und `MemoryClient` akzeptieren außerdem die übliche
Aufrufform für Agent-Memory, die andere Gedächtnis-Bibliotheken verwenden, sodass
bereits gegen diese Form geschriebener Code durch Ändern nur des Imports umsteigen
kann. Siehe
[docs/COMPATIBILITY.md](docs/COMPATIBILITY.md).

Die eigenen Fähigkeiten der Engine hängen am selben Objekt:

```python
from mnemosyne import MemoryBrain

brain = MemoryBrain("./memories", enable_embeddings=True)
brain.ensure_init()
brain.retain("His laptop is an ASUS VivoBook Pro 14", fast=True)

results = brain.recall("what are that machine's specs", k=5)
results, cost = brain.recall("that machine's specs", k=5, budget_tokens=100)

cap = brain.capsule("<memory_id>", budget_tokens=60)   # Pointer + Fakten + Atome
brain.expand(cap["ref"])                                # byteweise exakte Rekonstruktion
brain.verify_integrity()                                # SHA-256-Ledger-Prüfung
```

---

## 📂 Projektstruktur

```
mnemosyne/
├── api/                 # die Memory-API: Memory / AsyncMemory / MemoryClient
│   ├── memory.py        #   engine-gestützter Client
│   ├── config.py        #   MemoryConfig + Prüfungen der Dimensionskonsistenz
│   ├── filters.py       #   Filtersprache -> Prädikate
│   ├── extract.py       #   einmalige ADD-only-Extraktion
│   ├── multimodal.py    #   Parsing von Bild-/Audio-Anhängen
│   ├── events.py        #   persistiertes Operationsprotokoll
│   └── client.py        #   eingebetteter + HTTP-Transport
├── providers/           # optionale Komponenten-Adapter (insgesamt 72)
│   ├── llms.py          #   20 LLM-Provider
│   ├── embedders.py     #   13 Embedder-Provider
│   ├── vector_stores.py #   28 Vektorspeicher
│   ├── graph_stores.py  #   6 Graphspeicher
│   ├── rerankers.py     #   5 Reranker
│   ├── vision.py        #   drei Bild-Wire-Formate
│   └── transport.py     #   stdlib-HTTP + Retries + Redaktion von Zugangsdaten
├── brain.py             # MemoryBrain — die Engine-Fassade
├── capsule.py           # AIC verlustfreie Kompression
├── retrieval.py         # Multi-Signal-Fusion und Relevanzkalibrierung
├── graph.py             # temporaler Tripel-Store
├── notary.py            # Vertrauens-Pipeline vor dem Schreiben
├── cli.py               # native CLI
├── api_cli.py           # Client-API-CLI
└── webui/
    ├── web_server.py    # Konsole + REST-Host
    ├── api_routes.py    # /v1 /v2 /v3 Routen
    ├── mcp_server.py    # 20 native MCP-Tools
    └── mcp_api.py       # 11 client-kompatible MCP-Tools

storage/                 # SQLite-Backend, hash-verkettetes Ledger, Plugin-SDK
security/                # Widerspruchserkennung, Sicherheits-Reporting
scripts/                 # Verifikationsskripte
docs/                    # Abnahmeleitfaden, Recall-Strategie, Kompatibilität
```

---

## ✅ Tests

```bash
python verify.py                              # Selbsttest
python scripts/verify_api.py                  # Verifikation der Client-API, vollständig offline
python scripts/verify_memory_lifecycle.py --brain-dir ./mem --src-root .
python scripts/verify_precision_recall.py     # Offline-Präzisionsregression
python scripts/verify_recall_quality.py       # End-to-End-Recall-Qualität
```

---

## 📚 Dokumentation

- [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) — die übliche Aufrufform für Agent-Memory
- [docs/ACCEPTANCE_GUIDE.md](docs/ACCEPTANCE_GUIDE.md) — Abnahmekriterien und das jeweilige Skript
- [docs/RECALL_STRATEGY.md](docs/RECALL_STRATEGY.md) — wie Retrieval zusammengesetzt und budgetiert wird
- [docs/KNOWN_DEFECTS.md](docs/KNOWN_DEFECTS.md) — bestätigte Defekte, mit Messungen und Fixes
- [docs/DEPLOY_DEEPSEEK_HARNESS.md](docs/DEPLOY_DEEPSEEK_HARNESS.md) — MCP-Deployment-Walkthrough
- [CHANGELOG.md](CHANGELOG.md) — Versionshistorie

---

## 📄 Lizenz

MIT License — see [LICENSE](LICENSE).

Erstellt von den Mitwirkenden von Mnemosyne OS.
