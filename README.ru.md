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
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="Лицензия: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="#-mcp-сервер"><img src="https://img.shields.io/badge/MCP-31%20Tools-00ADD8?style=for-the-badge" alt="Протокол Model Context"></a>
  <a href="#-быстрый-старт"><img src="https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge" alt="Без зависимостей"></a>
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

**Mnemosyne OS 8.0.0** — локальная система ИИ-памяти без зависимостей. Графовая
память, мультимодальный приём, переранжирование, временные рассуждения,
аудиторский журнал с хеш-цепочкой, сжатие без потерь и 31 инструмент MCP.

> Единственный движок ИИ-памяти, у которого **ядро действительно не тянет
> сторонних зависимостей** — ни векторной базы данных, ни среды выполнения LLM,
> ни облачного аккаунта. `install_requires` — пустой список. Одинаково работает
> на ноутбуке, на сервере и в бессерверной инфраструктуре.

Используйте его как **библиотеку Python**, **CLI**, **HTTP API** или **MCP-сервер**.

---

## 🚀 Быстрый старт

### Установка

```bash
pip install mnemosyne-os          # ядро: без сторонних зависимостей
```

### Запоминаем и вспоминаем, ничего не настраивая

```python
from mnemosyne import Memory

m = Memory()                       # встроенный эмбеддер + извлекатель на правилах
m.add("I prefer dark mode and use vim keybindings. My name is Alice.",
      user_id="alice")

for hit in m.search("what does alice prefer", filters={"user_id": "alice"})["results"]:
    print(f"{hit['score']:.3f}  {hit['memory']}")
```

Офлайн, без API-ключа, без скачивания моделей, без установки базы данных — именно
это делает возможным следующий раздел.

### Настоящие модели подключаются только тогда, когда воспроизведение нужно усилить

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

Каждый компонент необязателен сам по себе. Когда провайдера не удаётся собрать,
происходит откат к встроенному эквиваленту, и об этом **сообщается прямо** —
ничего не деградирует молча:

```python
m.describe()["degraded"]
# {'llm': {'requested': 'openai', 'used': 'rules', 'reason': 'no API key configured',
#          'hint': 'Set MNEMOSYNE_LLM_OPENAI_API_KEY ...'}}
```

### Или управляйте из командной строки

```bash
mnemosyne init
mnemosyne add "I prefer dark mode and vim keybindings" --user-id alice
mnemosyne search "what does alice prefer" --user-id alice
mnemosyne list  --user-id alice
mnemosyne event --limit 10
mnemosyne --agent search "preferences" --user-id alice   # JSON-конверт для циклов инструментов
```

### Или отдайте его по MCP

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

### Или поднимите его по HTTP

```bash
mnemosyne-web --port 9090          # консоль и REST делят один порт
curl -X POST http://127.0.0.1:8788/v3/memories/add/ \
  -H "Authorization: Bearer $MNEMOSYNE_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"I moved to Berlin in 2023."}],"user_id":"alice"}'
```

---

## 📊 Бенчмарки

Измерено стендом, поставляемым вместе с этим репозиторием. Воспроизводится
скриптами `scripts/verify_recall_quality.py` и `scripts/verify_precision_recall.py`.

| Бенчмарк | Оценка | Что измеряет |
| --- | --- | --- |
| LongMemEval | **96.2** | воспроизведение в длинных диалогах |
| LoCoMo | **94.8** | память многосессионных диалогов |
| BEAM (1M) | **68.5** | воспроизведение при бюджете контекста 1M токенов |
| BEAM (10M) | **53.9** | воспроизведение при бюджете контекста 10M токенов |

Оценки по 100-балльной шкале.

---

## 🧩 Возможности

<table>
<tr><td><b>API памяти</b></td><td><code>Memory</code> / <code>AsyncMemory</code> / <code>MemoryClient</code> с полным набором методов: <code>add</code> <code>get</code> <code>get_all</code> <code>search</code> <code>update</code> <code>delete</code> <code>delete_all</code> <code>history</code> <code>reset</code> <code>close</code> <code>from_config</code>.</td></tr>
<tr><td><b>Четырёхмерная область видимости</b></td><td><code>user_id</code> / <code>agent_id</code> / <code>run_id</code> / <code>app_id</code> — обеспечивается <b>физической изоляцией</b>: по одному файлу SQLite на область видимости, а не общие строки с наложенным фильтром.</td></tr>
<tr><td><b>Язык фильтров</b></td><td><code>eq</code> <code>ne</code> <code>gt</code> <code>gte</code> <code>lt</code> <code>lte</code> <code>in</code> <code>nin</code> <code>contains</code> <code>icontains</code> <code>wildcard</code> с произвольной вложенностью <code>AND</code>/<code>OR</code>/<code>NOT</code>.</td></tr>
<tr><td><b>Однопроходное извлечение «только добавление» (ADD-only)</b></td><td>Один вызов модели на запись; памяти накапливаются и никогда не перезаписываются. Поскольку ничего не перезаписывается, плохое извлечение лишь добавляет шум — оно никогда не может уничтожить реальный факт.</td></tr>
<tr><td><b>Графовая память, всегда включена</b></td><td>Связывание сущностей и многошаговый обход живут в одном и том же файле SQLite. Внешняя графовая база данных не требуется.</td></tr>
<tr><td><b>Мультимодальный приём</b></td><td>Принимает форматы изображений OpenAI, Anthropic и Gemini (плюс аудио). С настроенной vision-моделью сохраняется описание; без неё сохраняется ссылка — ничего не отбрасывается.</td></tr>
<tr><td><b>Многосигнальный поиск</b></td><td>Семантика + ключевые слова BM25 + граф сущностей + время + теги, объединённые с откалиброванными порогами релевантности и лексическим откатом.</td></tr>
<tr><td><b>Временные рассуждения</b></td><td>Даты наблюдений, разрешение относительного времени, семантика истечения срока и цепочки версий по сущностям.</td></tr>
<tr><td><b>Многоуровневая память</b></td><td>Уровни горячий / тёплый / холодный с экономикой забывания: малоценные памяти понижаются в уровне и сжимаются, но никогда не удаляются молча.</td></tr>
<tr><td><b>Сжатие без потерь (AIC)</b></td><td>Сжимает память в <i>указатель + структурированные факты + атомы содержимого</i>. Числа, даты, суммы и номера моделей сохраняются на любом уровне; <code>expand()</code> побайтово восстанавливает исходный текст и проверяет его хеш.</td></tr>
<tr><td><b>Аудиторский журнал с хеш-цепочкой</b></td><td>Цепочка SHA-256; <code>verify_integrity()</code> обнаруживает подмену и называет конкретную изменённую запись.</td></tr>
<tr><td><b>Асинхронный API и события</b></td><td><code>AsyncMemory</code> для высокопроизводительных записей плюс сохраняемый журнал операций, чтобы принятая запись оставалась видимой между процессами.</td></tr>
<tr><td><b>Оптимизация под китайский</b></td><td>Bigram-токенизация + FTS5 + встроенный словарь синонимов при полной поддержке латиницы.</td></tr>
<tr><td><b>Нотариус безопасности</b></td><td>До того как запись ляжет в хранилище, обнаруживает учётные данные, невидимый Unicode и HTML-инъекции и выполняет сокрытие на уровне полей.</td></tr>
</table>

---

## 🔌 Интеграции

Каждый адаптер необязателен. Адаптерам **stdlib** сторонние пакеты не нужны
вообще — они говорят по HTTP напрямую через `urllib`. Адаптеры **sdk** лениво
импортируют свой SDK и точно сообщают, какого пакета не хватает.

### Провайдеры LLM (20)

| Транспорт | Провайдеры |
| --- | --- |
| **stdlib HTTP** | `openai` `openai_structured` `azure_openai` `azure_openai_structured` `ollama` `anthropic` `gemini` `groq` `together` `deepseek` `minimax` `xai` `sarvam` `openrouter` `litellm` `lmstudio` `vllm` |
| **sdk** | `langchain` `aws_bedrock` |
| **встроенный** | `rules` — детерминированный офлайн-извлекатель, поэтому `add()` работает вообще без настроенной модели |

### Эмбеддеры (13)

| Транспорт | Провайдеры |
| --- | --- |
| **stdlib HTTP** | `openai` `azure_openai` `ollama` `gemini` `vertexai` `together` `lmstudio` `huggingface` |
| **sdk** | `fastembed` `langchain` `aws_bedrock` |
| **встроенный** | `builtin` (128 измерений, без зависимостей, детерминированный) · `hashing` (любая размерность, офлайн) |

### Векторные хранилища (28)

| Транспорт | Хранилища |
| --- | --- |
| **встроенные** | `builtin` (один файл SQLite хранит и памяти, и векторы) · `memory` · `generic` (декларативный REST) |
| **stdlib HTTP** | `qdrant` `pinecone` `elasticsearch` `opensearch` `weaviate` `upstash_vector` `turbopuffer` |
| **sdk** | `chroma` `pgvector` `milvus` `mongodb` `redis` `valkey` `azure_ai_search` `azure_mysql` `baidu` `cassandra` `databricks` `faiss` `langchain` `neptune` `oracledb` `s3_vectors` `supabase` `vertex_ai_vector_search` |

### Графовые хранилища (6)

`builtin` (нативные тройки SQLite) · `neo4j` · `memgraph` · `neptune` · `kuzu` · `sparql` (любая конечная точка SPARQL 1.1)

### Реранкеры (5)

`llm` · `cohere` · `zero_entropy` · `huggingface` · `sentence_transformer`

### Адаптеры фреймворков

LangChain · LlamaIndex · CrewAI · Dify · n8n · Vercel AI SDK · Ollama · MCP (stdio + Streamable HTTP)

---

## 🛠 MCP сервер

Работает по stdio JSON-RPC:

```bash
export MNEMOSYNE_MCP_TOKEN="your-secret-token"   # необязательно, но рекомендуется
python -m mnemosyne.webui.mcp_server --brain-dir ./mem --namespace default
```

**31 инструмент** — двадцать нативных плюс одиннадцать, которые переиспользуют
привычные имена инструментов агентской памяти, так что существующий MCP-клиент
можно направить на Mnemosyne OS, не переписывая определения инструментов.

**Нативные (20):**

| Инструмент | Назначение |
| --- | --- |
| `retain` | Сохранить одну память |
| `recall` | Извлечь памяти |
| `retain_batch` | Массовая запись, примерно в 15× быстрее |
| `forget` | Забыть память — по id или найдя её запросом на естественном языке |
| `capsule` | Сжать память в  указатель + факты + атомы |
| `expand` | Побайтово восстановить исходный текст капсулы |
| `recall_health` | Метрики качества воспроизведения только для чтения |
| `consolidate` | Объединить почти дублирующиеся памяти в одного представителя |
| `reflect` | Статистика, частые сущности, обнаружение конфликтов, когнитивные паттерны |
| `dedup` | Обнаружить дубликаты и почти дубликаты |
| `graph_query` | Обход графа знаний |
| `temporal_query` | Запросы по цепочкам версий |
| `list_projects` | Список изолированных проектов |
| `doctor` | Проверка состояния — целостность, количество, диск, состояние бэкенда |
| `stats` | Статистика выполнения |
| `audit` | Запросы по аудиторской цепочке |
| `confidence_history` | Траектории уверенности |
| `memory/export-v1` | Экспорт через Memory Exchange Protocol |
| `memory/import-v1` | Импорт через Memory Exchange Protocol |
| `memory/claim` | Принять памяти из внешнего экспорта |

**Совместимые с клиентами (11):**

| Инструмент | Назначение |
| --- | --- |
| `add_memory` | Сохранить текст или историю диалога для пользователя/агента |
| `search_memories` | Семантический поиск с фильтрами |
| `get_memories` | Структурный фильтр + постраничный список |
| `get_memory` | Получить одну по id |
| `update_memory` | Перезаписать текст и/или метаданные |
| `delete_memory` | Удалить одну |
| `delete_all_memories` | Очистить область видимости |
| `delete_entities` | Удалить сущности с каскадом |
| `list_entities` | Список users/agents/apps/runs |
| `list_events` | Список операций с памятью |
| `get_event_status` | Опросить асинхронную операцию |

---

## 🌐 REST API на своём хостинге

Один процесс, один порт, принимает заголовки авторизации `X-API-Key`, `Bearer`
и `Token`. Консоль и API используют один и тот же слушатель.

| Метод | Путь | Назначение |
| --- | --- | --- |
| `GET` | `/v1/status/` | Проверка живости + отчёт о текущей конфигурации |
| `GET` | `/v1/providers/` | Все провайдеры и их текущая доступность |
| `POST` | `/v3/memories/add/` | Извлечь и сохранить (асинхронно, возвращает id события) |
| `POST` | `/v3/memories/search/` | Семантический поиск |
| `POST` | `/v3/memories/get-all/` | Список с фильтрацией |
| `GET` / `PUT` / `DELETE` | `/v3/memories/{id}/` | Получить / обновить / удалить одну |
| `DELETE` | `/v3/memories/` | Очистить область видимости |
| `GET` | `/v3/memories/{id}/history/` | История изменений |
| `GET` | `/v1/event/{id}/` · `/v1/events/` | Опросить / список операций |
| `GET` / `DELETE` | `/v2/entities/` | Список / удаление областей видимости |
| `POST` | `/v3/graph/{add,search,get-all,delete-all}/` | Графовая память |
| `POST` | `/v1/capsule/` · `/v1/expand/` | Сжатие без потерь |
| `GET` | `/v1/integrity/` | Проверка журнала |
| `GET` / `POST` / `DELETE` | `/v1/keys/` | Управление API-ключами |

---

## 🧠 Python API

```python
from mnemosyne import Memory, AsyncMemory, MemoryClient

# --- извлечение / область видимости / фильтры ---------------------------------
m = Memory()
m.add([{"role": "user", "content": "I moved to Berlin in 2023."}],
      user_id="alice", metadata={"source": "onboarding"},
      observation_date="2023-06-01")
m.add("The invoice number is INV-2024-001.", user_id="alice", immutable=True)

hits = m.search("where does the user live",
                filters={"user_id": "alice",
                         "AND": [{"source": {"eq": "onboarding"}}]},
                top_k=5, threshold=0.1, rerank=False, explain=True)

# --- мультимодальность --------------------------------------------------------
m.add([{"role": "user", "content": [
    {"type": "text", "text": "My new desk."},
    {"type": "image_url", "image_url": {"url": "https://example.com/desk.jpg"}},
]}], user_id="alice")

# --- графовая память ----------------------------------------------------------
m.graph_add("Jobs founded Apple in Cupertino.", user_id="alice")
m.graph_search("Apple", filters={"user_id": "alice"})

# --- асинхронность и события --------------------------------------------------
async def ingest():
    am = AsyncMemory()
    await am.add_many([{"messages": t, "options": {"user_id": "alice"}}
                       for t in transcripts])
```

`Memory`, `AsyncMemory` и `MemoryClient` принимают также привычную форму вызова
агентской памяти, используемую другими библиотеками памяти, поэтому код, уже
написанный под эту форму, переключается сменой одного лишь импорта. См.
[docs/COMPATIBILITY.md](docs/COMPATIBILITY.md).

Собственные возможности движка висят на том же объекте:

```python
from mnemosyne import MemoryBrain

brain = MemoryBrain("./memories", enable_embeddings=True)
brain.ensure_init()
brain.retain("His laptop is an ASUS VivoBook Pro 14", fast=True)

results = brain.recall("what are that machine's specs", k=5)
results, cost = brain.recall("that machine's specs", k=5, budget_tokens=100)

cap = brain.capsule("<memory_id>", budget_tokens=60)   # указатель + факты + атомы
brain.expand(cap["ref"])                                # побайтовое восстановление
brain.verify_integrity()                                # проверка журнала SHA-256
```

---

## 📂 Структура проекта

```
mnemosyne/
├── api/                 # API памяти: Memory / AsyncMemory / MemoryClient
│   ├── memory.py        #   клиент на движке
│   ├── config.py        #   MemoryConfig + проверки согласованности размерности
│   ├── filters.py       #   язык фильтров -> предикаты
│   ├── extract.py       #   однопроходное извлечение ADD-only
│   ├── multimodal.py    #   разбор вложений изображений / аудио
│   ├── events.py        #   сохраняемый журнал операций
│   └── client.py        #   встроенный + HTTP транспорты
├── providers/           # адаптеры необязательных компонентов (всего 72)
│   ├── llms.py          #   20 провайдеров LLM
│   ├── embedders.py     #   13 провайдеров эмбеддеров
│   ├── vector_stores.py #   28 векторных хранилищ
│   ├── graph_stores.py  #   6 графовых хранилищ
│   ├── rerankers.py     #   5 реранкеров
│   ├── vision.py        #   три проводных формата изображений
│   └── transport.py     #   stdlib HTTP + повторы + сокрытие учётных данных
├── brain.py             # MemoryBrain — фасад движка
├── capsule.py           # AIC сжатие без потерь
├── retrieval.py         # многосигнальное объединение и калибровка релевантности
├── graph.py             # хранилище временных троек
├── notary.py            # конвейер доверия перед записью
├── cli.py               # нативный CLI
├── api_cli.py           # CLI клиентского API
└── webui/
    ├── web_server.py    # хост консоли + REST
    ├── api_routes.py    # маршруты /v1 /v2 /v3
    ├── mcp_server.py    # 20 нативных инструментов MCP
    └── mcp_api.py       # 11 совместимых с клиентами инструментов MCP

storage/                 # бэкенд SQLite, журнал с хеш-цепочкой, SDK плагинов
security/                # обнаружение противоречий, отчёты о безопасности
scripts/                 # скрипты проверки
docs/                    # руководство по приёмке, стратегия воспроизведения, совместимость
```

---

## ✅ Тесты

```bash
python verify.py                              # самопроверка
python scripts/verify_api.py                  # проверка клиентского API, полностью офлайн
python scripts/verify_memory_lifecycle.py --brain-dir ./mem --src-root .
python scripts/verify_precision_recall.py     # офлайн-регрессия точности
python scripts/verify_recall_quality.py       # сквозное качество воспроизведения
```

---

## 📚 Документация

- [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) — привычная форма вызова агентской памяти
- [docs/ACCEPTANCE_GUIDE.md](docs/ACCEPTANCE_GUIDE.md) — критерии приёмки и скрипт для каждого
- [docs/RECALL_STRATEGY.md](docs/RECALL_STRATEGY.md) — как собирается поиск и как расходуется бюджет
- [docs/KNOWN_DEFECTS.md](docs/KNOWN_DEFECTS.md) — подтверждённые дефекты, с измерениями и исправлениями
- [docs/DEPLOY_DEEPSEEK_HARNESS.md](docs/DEPLOY_DEEPSEEK_HARNESS.md) — пошаговое развёртывание MCP
- [CHANGELOG.md](CHANGELOG.md) — история версий

---

## 📄 Лицензия

MIT License — see [LICENSE](LICENSE).

Создано участниками Mnemosyne OS.
