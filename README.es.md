<p align="center">
  <img src="assets/banner.png" alt="Mnemosyne OS" width="100%">
</p>

# Mnemosyne OS

<p align="center">
  <a href="https://pypi.org/project/mnemosyne-os/">PyPI</a> ·
  <a href="https://github.com/FrankHu-HK/mnemosyne">GitHub</a> ·
  <a href="README.md">English</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/mnemosyne-os/"><img src="https://img.shields.io/badge/PyPI-mnemosyne--os-blue?style=for-the-badge" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="Licencia: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="#-servidor-mcp"><img src="https://img.shields.io/badge/MCP-31%20Tools-00ADD8?style=for-the-badge" alt="Protocolo de Contexto de Modelo"></a>
  <a href="#-inicio-rápido"><img src="https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge" alt="Cero dependencias"></a>
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

**Mnemosyne OS 8.0.0** — un sistema de memoria de IA local-first y de cero
dependencias. Memoria en grafo, ingesta multimodal, reranking, razonamiento
temporal, un libro de auditoría encadenado por hash, compresión sin pérdida y
31 herramientas MCP.

> El único motor de memoria de IA cuyo **núcleo no tiene de verdad ninguna
> dependencia de terceros** — sin base de datos vectorial, sin runtime de LLM,
> sin cuenta en la nube. `install_requires` es una lista vacía. Se ejecuta igual
> en un portátil, en un servidor o en infraestructura sin servidor.

Se puede usar como **biblioteca de Python**, **CLI**, **API HTTP** o **servidor MCP**.

---

## 🚀 Inicio rápido

### Instalación

```bash
pip install mnemosyne-os          # núcleo: cero dependencias de terceros
```

### Recordar y recuperar sin configurar nada

```python
from mnemosyne import Memory

m = Memory()                       # embedder integrado + extractor basado en reglas
m.add("I prefer dark mode and use vim keybindings. My name is Alice.",
      user_id="alice")

for hit in m.search("what does alice prefer", filters={"user_id": "alice"})["results"]:
    print(f"{hit['score']:.3f}  {hit['memory']}")
```

Funciona sin conexión, sin clave de API, sin descargar modelos y sin instalar
ninguna base de datos — y eso es lo que hace posible la siguiente sección.

### Conectar modelos reales solo cuando la recuperación necesite ser mejor

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

Cada componente es opcional de forma independiente. Cuando un proveedor no se
puede construir, se recurre al equivalente integrado y **se informa de ello** —
nada se degrada en silencio:

```python
m.describe()["degraded"]
# {'llm': {'requested': 'openai', 'used': 'rules', 'reason': 'no API key configured',
#          'hint': 'Set MNEMOSYNE_LLM_OPENAI_API_KEY ...'}}
```

### O controlarlo desde la línea de comandos

```bash
mnemosyne init
mnemosyne add "I prefer dark mode and vim keybindings" --user-id alice
mnemosyne search "what does alice prefer" --user-id alice
mnemosyne list  --user-id alice
mnemosyne event --limit 10
mnemosyne --agent search "preferences" --user-id alice   # sobre JSON para bucles de herramientas
```

### O exponerlo por MCP

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

### O servirlo por HTTP

```bash
mnemosyne-web --port 9090          # la consola y REST comparten un solo puerto
curl -X POST http://127.0.0.1:8788/v3/memories/add/ \
  -H "Authorization: Bearer $MNEMOSYNE_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"I moved to Berlin in 2023."}],"user_id":"alice"}'
```

---

## 📊 Benchmarks

Medido con el arnés de pruebas incluido en este repositorio. Se reproduce con
`scripts/verify_recall_quality.py` y `scripts/verify_precision_recall.py`.

| Benchmark | Puntuación | Qué mide |
| --- | --- | --- |
| LongMemEval | **96.2** | recuperación conversacional de largo horizonte |
| LoCoMo | **94.8** | memoria de diálogo multi-sesión |
| BEAM (1M) | **68.5** | recuperación con un presupuesto de contexto de 1M tokens |
| BEAM (10M) | **53.9** | recuperación con un presupuesto de contexto de 10M tokens |

Las puntuaciones son sobre 100.

---

## 🧩 Capacidades

<table>
<tr><td><b>API de memoria</b></td><td><code>Memory</code> / <code>AsyncMemory</code> / <code>MemoryClient</code> con una superficie de métodos completa: <code>add</code> <code>get</code> <code>get_all</code> <code>search</code> <code>update</code> <code>delete</code> <code>delete_all</code> <code>history</code> <code>reset</code> <code>close</code> <code>from_config</code>.</td></tr>
<tr><td><b>Alcance en cuatro dimensiones</b></td><td><code>user_id</code> / <code>agent_id</code> / <code>run_id</code> / <code>app_id</code> — aplicado mediante <b>aislamiento físico</b>: un archivo SQLite por alcance, en lugar de filas compartidas con un filtro aplicado.</td></tr>
<tr><td><b>Lenguaje de filtros</b></td><td><code>eq</code> <code>ne</code> <code>gt</code> <code>gte</code> <code>lt</code> <code>lte</code> <code>in</code> <code>nin</code> <code>contains</code> <code>icontains</code> <code>wildcard</code>, con anidamiento arbitrario de <code>AND</code>/<code>OR</code>/<code>NOT</code>.</td></tr>
<tr><td><b>Extracción ADD-only de una sola pasada</b></td><td>Una llamada al modelo por escritura; las memorias se acumulan y nunca se sobrescriben. Como no se reescribe nada, una extracción defectuosa solo introduce ruido — nunca puede destruir un hecho real.</td></tr>
<tr><td><b>Memoria en grafo, siempre activa</b></td><td>El enlazado de entidades y el recorrido multi-salto viven en el mismo archivo SQLite. No hace falta ninguna base de datos de grafos externa.</td></tr>
<tr><td><b>Ingesta multimodal</b></td><td>Acepta los formatos de contenido de imagen de OpenAI, Anthropic y Gemini (además de audio). Con un modelo de visión configurado almacena una descripción; sin uno, almacena la referencia — no se descarta nada.</td></tr>
<tr><td><b>Recuperación multi-señal</b></td><td>Semántica + palabras clave BM25 + grafo de entidades + temporal + etiqueta, fusionadas con umbrales de relevancia calibrados y un respaldo léxico.</td></tr>
<tr><td><b>Razonamiento temporal</b></td><td>Fechas de observación, resolución de tiempo relativo, semántica de caducidad y cadenas de versiones por entidad.</td></tr>
<tr><td><b>Memoria por niveles</b></td><td>Niveles caliente / templado / frío con economía del olvido: las memorias de bajo valor se degradan y se comprimen, nunca se eliminan en silencio.</td></tr>
<tr><td><b>Compresión sin pérdida (AIC)</b></td><td>Comprime una memoria en <i>puntero + hechos estructurados + átomos de contenido</i>. Números, fechas, importes y números de modelo sobreviven en todos los niveles; <code>expand()</code> recupera el texto original byte a byte y verifica su hash.</td></tr>
<tr><td><b>Libro de auditoría encadenado por hash</b></td><td>Una cadena SHA-256; <code>verify_integrity()</code> detecta manipulaciones y señala la entrada exacta que cambió.</td></tr>
<tr><td><b>API asíncrona y eventos</b></td><td><code>AsyncMemory</code> para escrituras de alto rendimiento, más un registro de operaciones persistido, de modo que una escritura aceptada sigue siendo visible entre procesos.</td></tr>
<tr><td><b>Optimizado para chino</b></td><td>Tokenización por bigramas + FTS5 + un diccionario de sinónimos integrado, con soporte completo de escritura latina.</td></tr>
<tr><td><b>Notaría de seguridad</b></td><td>Detecta credenciales, Unicode invisible e inyección de HTML antes de que una escritura se materialice, y redacta a nivel de campo.</td></tr>
</table>

---

## 🔌 Integraciones

Todos los adaptadores son opcionales. Los adaptadores **stdlib** no necesitan
ningún paquete de terceros: hablan HTTP directamente mediante `urllib`. Los
adaptadores **sdk** importan su SDK de forma diferida y te dicen exactamente qué
paquete falta.

### Proveedores de LLM (20)

| Transporte | Proveedores |
| --- | --- |
| **stdlib HTTP** | `openai` `openai_structured` `azure_openai` `azure_openai_structured` `ollama` `anthropic` `gemini` `groq` `together` `deepseek` `minimax` `xai` `sarvam` `openrouter` `litellm` `lmstudio` `vllm` |
| **sdk** | `langchain` `aws_bedrock` |
| **integrado** | `rules` — un extractor offline determinista, y por eso `add()` funciona sin ningún modelo configurado |

### Modelos de embedding (13)

| Transporte | Proveedores |
| --- | --- |
| **stdlib HTTP** | `openai` `azure_openai` `ollama` `gemini` `vertexai` `together` `lmstudio` `huggingface` |
| **sdk** | `fastembed` `langchain` `aws_bedrock` |
| **integrado** | `builtin` (128 dim, cero dependencias, determinista) · `hashing` (cualquier dimensión, offline) |

### Almacenes vectoriales (28)

| Transporte | Almacenes |
| --- | --- |
| **embebido** | `builtin` (un solo archivo SQLite contiene tanto las memorias como los vectores) · `memory` · `generic` (REST declarativo) |
| **stdlib HTTP** | `qdrant` `pinecone` `elasticsearch` `opensearch` `weaviate` `upstash_vector` `turbopuffer` |
| **sdk** | `chroma` `pgvector` `milvus` `mongodb` `redis` `valkey` `azure_ai_search` `azure_mysql` `baidu` `cassandra` `databricks` `faiss` `langchain` `neptune` `oracledb` `s3_vectors` `supabase` `vertex_ai_vector_search` |

### Almacenes de grafos (6)

`builtin` (triples nativos en SQLite) · `neo4j` · `memgraph` · `neptune` · `kuzu` · `sparql` (cualquier endpoint SPARQL 1.1)

### Rerankers (5)

`llm` · `cohere` · `zero_entropy` · `huggingface` · `sentence_transformer`

### Adaptadores de frameworks

LangChain · LlamaIndex · CrewAI · Dify · n8n · Vercel AI SDK · Ollama · MCP (stdio + Streamable HTTP)

---

## 🛠 Servidor MCP

Se ejecuta sobre stdio JSON-RPC:

```bash
export MNEMOSYNE_MCP_TOKEN="your-secret-token"   # opcional, pero recomendado
python -m mnemosyne.webui.mcp_server --brain-dir ./mem --namespace default
```

**31 herramientas** — veinte nativas, más once que reutilizan los nombres de
herramienta convencionales de la memoria de agentes, de modo que un cliente MCP
existente se puede apuntar a Mnemosyne OS sin reescribir sus definiciones de
herramientas.

**Nativas (20):**

| Herramienta | Propósito |
| --- | --- |
| `retain` | Almacena una memoria |
| `recall` | Recupera memorias |
| `retain_batch` | Escritura en lote, unas 15× más rápida |
| `forget` | Olvida una memoria — por id, o localizándola con una consulta en lenguaje natural |
| `capsule` | Comprime una memoria en puntero + hechos + átomos |
| `expand` | Recupera el texto original de una cápsula byte a byte |
| `recall_health` | Métricas de calidad de recuperación de solo lectura |
| `consolidate` | Fusiona memorias casi duplicadas en una sola representante |
| `reflect` | Estadísticas, entidades frecuentes, detección de conflictos, patrones cognitivos |
| `dedup` | Detecta duplicados y casi duplicados |
| `graph_query` | Recorrido del grafo de conocimiento |
| `temporal_query` | Consultas de cadenas de versiones |
| `list_projects` | Lista los proyectos aislados |
| `doctor` | Comprobación de estado — integridad, recuentos, disco, estado del backend |
| `stats` | Estadísticas en tiempo de ejecución |
| `audit` | Consultas de la cadena de auditoría |
| `confidence_history` | Trayectorias de confianza |
| `memory/export-v1` | Exporta mediante el Memory Exchange Protocol |
| `memory/import-v1` | Importa mediante el Memory Exchange Protocol |
| `memory/claim` | Adopta memorias de una exportación externa |

**Compatibles con clientes (11):**

| Herramienta | Propósito |
| --- | --- |
| `add_memory` | Guarda texto o historial de conversación para un usuario/agente |
| `search_memories` | Búsqueda semántica con filtros |
| `get_memories` | Filtro estructurado + listado paginado |
| `get_memory` | Obtiene una por id |
| `update_memory` | Sobrescribe el texto y/o los metadatos |
| `delete_memory` | Elimina una |
| `delete_all_memories` | Vacía un alcance |
| `delete_entities` | Elimina entidades y en cascada |
| `list_entities` | Lista usuarios/agentes/apps/runs |
| `list_events` | Lista las operaciones sobre memorias |
| `get_event_status` | Consulta el estado de una operación asíncrona |

---

## 🌐 API REST autoalojada

Un proceso, un puerto, que acepta los encabezados de autenticación `X-API-Key`,
`Bearer` y `Token`. La consola y la API comparten el mismo listener.

| Método | Ruta | Propósito |
| --- | --- | --- |
| `GET` | `/v1/status/` | Sonda de vida + informe de configuración en vivo |
| `GET` | `/v1/providers/` | Todos los proveedores y su disponibilidad actual |
| `POST` | `/v3/memories/add/` | Extrae y almacena (asíncrono, devuelve un id de evento) |
| `POST` | `/v3/memories/search/` | Búsqueda semántica |
| `POST` | `/v3/memories/get-all/` | Listado con filtros |
| `GET` / `PUT` / `DELETE` | `/v3/memories/{id}/` | Obtener / actualizar / eliminar una |
| `DELETE` | `/v3/memories/` | Vaciar un alcance |
| `GET` | `/v3/memories/{id}/history/` | Historial de cambios |
| `GET` | `/v1/event/{id}/` · `/v1/events/` | Consultar / listar operaciones |
| `GET` / `DELETE` | `/v2/entities/` | Listar / eliminar alcances |
| `POST` | `/v3/graph/{add,search,get-all,delete-all}/` | Memoria en grafo |
| `POST` | `/v1/capsule/` · `/v1/expand/` | Compresión sin pérdida |
| `GET` | `/v1/integrity/` | Verificación del libro |
| `GET` / `POST` / `DELETE` | `/v1/keys/` | Gestión de claves de API |

---

## 🧠 API de Python

```python
from mnemosyne import Memory, AsyncMemory, MemoryClient

# --- extracción / alcance / filtros -------------------------------------------
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

# --- memoria en grafo ---------------------------------------------------------
m.graph_add("Jobs founded Apple in Cupertino.", user_id="alice")
m.graph_search("Apple", filters={"user_id": "alice"})

# --- asíncrono y eventos ------------------------------------------------------
async def ingest():
    am = AsyncMemory()
    await am.add_many([{"messages": t, "options": {"user_id": "alice"}}
                       for t in transcripts])
```

`Memory`, `AsyncMemory` y `MemoryClient` también aceptan la forma de llamada
convencional de la memoria de agentes que usan otras bibliotecas de memoria, de
modo que el código ya escrito contra esa forma puede cambiar con solo modificar
el import. Consulta [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md).

Las capacidades propias del motor cuelgan del mismo objeto:

```python
from mnemosyne import MemoryBrain

brain = MemoryBrain("./memories", enable_embeddings=True)
brain.ensure_init()
brain.retain("His laptop is an ASUS VivoBook Pro 14", fast=True)

results = brain.recall("what are that machine's specs", k=5)
results, cost = brain.recall("that machine's specs", k=5, budget_tokens=100)

cap = brain.capsule("<memory_id>", budget_tokens=60)   # puntero + hechos + átomos
brain.expand(cap["ref"])                                # recuperación byte a byte
brain.verify_integrity()                                # comprobación del libro SHA-256
```

---

## 📂 Estructura

```
mnemosyne/
├── api/                 # la API de memoria: Memory / AsyncMemory / MemoryClient
│   ├── memory.py        #   cliente respaldado por el motor
│   ├── config.py        #   MemoryConfig + comprobaciones de consistencia de dimensión
│   ├── filters.py       #   lenguaje de filtros -> predicados
│   ├── extract.py       #   extracción ADD-only de una sola pasada
│   ├── multimodal.py    #   análisis de adjuntos de imagen / audio
│   ├── events.py        #   registro de operaciones persistido
│   └── client.py        #   transportes embebido + HTTP
├── providers/           # adaptadores de componentes opcionales (72 en total)
│   ├── llms.py          #   20 proveedores de LLM
│   ├── embedders.py     #   13 proveedores de embedder
│   ├── vector_stores.py #   28 almacenes vectoriales
│   ├── graph_stores.py  #   6 almacenes de grafos
│   ├── rerankers.py     #   5 rerankers
│   ├── vision.py        #   tres formatos de imagen de transferencia
│   └── transport.py     #   HTTP de stdlib + reintentos + redacción de credenciales
├── brain.py             # MemoryBrain — la fachada del motor
├── capsule.py           # compresión sin pérdida AIC
├── retrieval.py         # fusión multi-señal y calibración de relevancia
├── graph.py             # almacén de triples temporal
├── notary.py            # canal de confianza previo a la escritura
├── cli.py               # CLI nativa
├── api_cli.py           # CLI de la API de cliente
└── webui/
    ├── web_server.py    # host de consola + REST
    ├── api_routes.py    # rutas /v1 /v2 /v3
    ├── mcp_server.py    # 20 herramientas MCP nativas
    └── mcp_api.py       # 11 herramientas MCP compatibles con clientes

storage/                 # backend SQLite, libro encadenado por hash, SDK de plugins
security/                # detección de contradicciones, informes de seguridad
scripts/                 # scripts de verificación
docs/                    # guía de aceptación, estrategia de recuperación, compatibilidad
```

---

## ✅ Pruebas

```bash
python verify.py                              # autocomprobación
python scripts/verify_api.py                  # verificación de la API de cliente, totalmente offline
python scripts/verify_memory_lifecycle.py --brain-dir ./mem --src-root .
python scripts/verify_precision_recall.py     # regresión de precisión offline
python scripts/verify_recall_quality.py       # calidad de recuperación de extremo a extremo
```

---

## 📚 Documentación

- [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) — la forma de llamada convencional de la memoria de agentes
- [docs/ACCEPTANCE_GUIDE.md](docs/ACCEPTANCE_GUIDE.md) — criterios de aceptación y el script para cada uno
- [docs/RECALL_STRATEGY.md](docs/RECALL_STRATEGY.md) — cómo se ensambla y se presupuesta la recuperación
- [docs/KNOWN_DEFECTS.md](docs/KNOWN_DEFECTS.md) — defectos confirmados, con mediciones y correcciones
- [docs/DEPLOY_DEEPSEEK_HARNESS.md](docs/DEPLOY_DEEPSEEK_HARNESS.md) — guía práctica de despliegue MCP
- [CHANGELOG.md](CHANGELOG.md) — historial de versiones

---

## 📄 Licencia

MIT License — see [LICENSE](LICENSE).

Creado por los colaboradores de Mnemosyne OS.
