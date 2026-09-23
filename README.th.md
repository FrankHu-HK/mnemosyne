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
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="สัญญาอนุญาต: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="#-เซิร์ฟเวอร์-mcp"><img src="https://img.shields.io/badge/MCP-31%20Tools-00ADD8?style=for-the-badge" alt="โมเดลคอนเท็กซ์โปรโตคอล"></a>
  <a href="#-เริ่มต้นอย่างรวดเร็ว"><img src="https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge" alt="ไม่พึ่งพาไลบรารีภายนอก"></a>
  <a href="https://pepy.tech/projects/mnemosyne-os"><img src="https://img.shields.io/pepy/dt/mnemosyne-os?style=for-the-badge" alt="ยอดดาวน์โหลด"></a>
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

**Mnemosyne OS 8.0.0** — ระบบหน่วยความจำ AI แบบ local-first ที่ไม่พึ่งพาไลบรารีภายนอก
ประกอบด้วยหน่วยความจำแบบกราฟ การนำเข้าข้อมูลหลายรูปแบบ (มัลติโมดัล) การจัดอันดับใหม่
การให้เหตุผลเชิงเวลา บัญชีตรวจสอบแบบ hash chain การบีบอัดแบบไม่สูญเสียข้อมูล
และเครื่องมือ MCP 31 รายการ

> เอนจินหน่วยความจำ AI ตัวเดียวที่**แกนหลักไม่มี dependency จากบุคคลที่สามเลยจริง ๆ**
> — ไม่ต้องมีฐานข้อมูลเวกเตอร์ ไม่ต้องมีรันไทม์ LLM ไม่ต้องมีบัญชีคลาวด์
> `install_requires` เป็นลิสต์ว่าง ใช้งานได้ทั้งบนแล็ปท็อป เซิร์ฟเวอร์
> หรือโครงสร้างพื้นฐานแบบ serverless อย่างเดียวกัน

ใช้ได้ทั้งเป็น **ไลบรารี Python**, **CLI**, **HTTP API** หรือ **เซิร์ฟเวอร์ MCP**

---

## 🚀 เริ่มต้นอย่างรวดเร็ว

### ติดตั้ง

```bash
pip install mnemosyne-os          # แกนหลัก: ไม่มี dependency จากบุคคลที่สาม
```

### จดจำและเรียกคืนได้โดยไม่ต้องตั้งค่าใด ๆ

```python
from mnemosyne import Memory

m = Memory()                       # ตัวสร้างเวกเตอร์ฝังในตัว + ตัวสกัดแบบกฎ
m.add("I prefer dark mode and use vim keybindings. My name is Alice.",
      user_id="alice")

for hit in m.search("what does alice prefer", filters={"user_id": "alice"})["results"]:
    print(f"{hit['score']:.3f}  {hit['memory']}")
```

ทำงานแบบออฟไลน์ ไม่ต้องมี API key ไม่ต้องดาวน์โหลดโมเดล ไม่ต้องติดตั้งฐานข้อมูล
และนั่นคือสิ่งที่ทำให้หัวข้อถัดไปเป็นไปได้

### ต่อโมเดลจริงเมื่อต้องการการเรียกคืนที่แรงขึ้น

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

ทุกคอมโพเนนต์เป็นทางเลือกแยกจากกัน เมื่อสร้างผู้ให้บริการหนึ่งไม่สำเร็จ
ระบบจะถอยไปใช้สิ่งที่เทียบเท่าที่มีในตัว และ**แจ้งให้ทราบ** — ไม่มีการลดทอนแบบเงียบ:

```python
m.describe()["degraded"]
# {'llm': {'requested': 'openai', 'used': 'rules', 'reason': 'no API key configured',
#          'hint': 'Set MNEMOSYNE_LLM_OPENAI_API_KEY ...'}}
```

### หรือขับเคลื่อนผ่านบรรทัดคำสั่ง

```bash
mnemosyne init
mnemosyne add "I prefer dark mode and vim keybindings" --user-id alice
mnemosyne search "what does alice prefer" --user-id alice
mnemosyne list  --user-id alice
mnemosyne event --limit 10
mnemosyne --agent search "preferences" --user-id alice   # เปลือก JSON สำหรับลูปของเครื่องมือ
```

### หรือเปิดให้เข้าถึงผ่าน MCP

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

### หรือให้บริการผ่าน HTTP

```bash
mnemosyne-web --port 9090          # คอนโซลและ REST ใช้พอร์ตเดียวกัน
curl -X POST http://127.0.0.1:8788/v3/memories/add/ \
  -H "Authorization: Bearer $MNEMOSYNE_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"I moved to Berlin in 2023."}],"user_id":"alice"}'
```

---

## 📊 ผลการวัดประสิทธิภาพ

วัดด้วยฮาร์เนสที่แถมมาในรีโปนี้ ทำซ้ำได้ด้วย
`scripts/verify_recall_quality.py` และ `scripts/verify_precision_recall.py`

| การทดสอบ | คะแนน | สิ่งที่วัด |
| --- | --- | --- |
| LongMemEval | **96.2** | การเรียกคืนบทสนทนาระยะยาว |
| LoCoMo | **94.8** | หน่วยความจำบทสนทนาหลายเซสชัน |
| BEAM (1M) | **68.5** | การเรียกคืนภายในงบประมาณคอนเท็กซ์ 1M โทเคน |
| BEAM (10M) | **53.9** | การเรียกคืนภายในงบประมาณคอนเท็กซ์ 10M โทเคน |

คะแนนเต็ม 100

---

## 🧩 ความสามารถ

<table>
<tr><td><b>API หน่วยความจำ</b></td><td><code>Memory</code> / <code>AsyncMemory</code> / <code>MemoryClient</code> พร้อมชุดเมธอดครบถ้วน: <code>add</code> <code>get</code> <code>get_all</code> <code>search</code> <code>update</code> <code>delete</code> <code>delete_all</code> <code>history</code> <code>reset</code> <code>close</code> <code>from_config</code>.</td></tr>
<tr><td><b>ขอบเขตสี่มิติ</b></td><td><code>user_id</code> / <code>agent_id</code> / <code>run_id</code> / <code>app_id</code> — บังคับใช้ด้วย<b>การแยกทางกายภาพ</b>: หนึ่งไฟล์ SQLite ต่อหนึ่งขอบเขต แทนที่จะเป็นแถวที่ใช้ร่วมกันแล้วค่อยใส่ตัวกรอง</td></tr>
<tr><td><b>ภาษาตัวกรอง</b></td><td><code>eq</code> <code>ne</code> <code>gt</code> <code>gte</code> <code>lt</code> <code>lte</code> <code>in</code> <code>nin</code> <code>contains</code> <code>icontains</code> <code>wildcard</code> พร้อมการซ้อน <code>AND</code>/<code>OR</code>/<code>NOT</code> ได้ไม่จำกัดชั้น</td></tr>
<tr><td><b>การสกัดแบบ ADD-only รอบเดียว</b></td><td>เรียกโมเดลหนึ่งครั้งต่อการเขียนหนึ่งครั้ง หน่วยความจำจะสะสมเพิ่มขึ้นเรื่อย ๆ และไม่ถูกเขียนทับ เพราะไม่มีการเขียนทับ การสกัดที่ผิดพลาดจึงมีผลเพียงสร้างสัญญาณรบกวน แต่ไม่สามารถทำลายข้อเท็จจริงที่มีอยู่ได้</td></tr>
<tr><td><b>หน่วยความจำกราฟเปิดทำงานตลอดเวลา</b></td><td>การเชื่อมโยงเอนทิตีและการเดินกราฟหลายฮอปอยู่ในไฟล์ SQLite เดียวกัน ไม่ต้องมีฐานข้อมูลกราฟภายนอก</td></tr>
<tr><td><b>การนำเข้าข้อมูลหลายรูปแบบ</b></td><td>รองรับรูปแบบเนื้อหารูปภาพของ OpenAI, Anthropic และ Gemini (รวมถึงเสียง) หากตั้งค่าโมเดลวิชันไว้ ระบบจะจัดเก็บคำอธิบาย หากไม่มีก็จัดเก็บข้อมูลอ้างอิง — ไม่มีการทิ้งข้อมูล</td></tr>
<tr><td><b>การเรียกคืนหลายสัญญาณ</b></td><td>ความหมายเชิงเวกเตอร์ + คำสำคัญ BM25 + กราฟเอนทิตี + เชิงเวลา + แท็ก ผสานกันด้วยค่าพื้นความเกี่ยวข้องที่ปรับเทียบแล้ว พร้อมกลไกสำรองเชิงคำศัพท์</td></tr>
<tr><td><b>การให้เหตุผลเชิงเวลา</b></td><td>วันที่สังเกต การตีความเวลาสัมพัทธ์ ความหมายของการหมดอายุ และสายเวอร์ชันรายเอนทิตี</td></tr>
<tr><td><b>หน่วยความจำแบบแบ่งชั้น</b></td><td>ชั้น hot / warm / cold พร้อมเศรษฐศาสตร์ของการลืม: หน่วยความจำที่มีมูลค่าต่ำจะถูกลดชั้นและบีบอัด ไม่ถูกลบอย่างเงียบ ๆ</td></tr>
<tr><td><b>การบีบอัดแบบไม่สูญเสียข้อมูล (AIC)</b></td><td>บีบอัดหน่วยความจำหนึ่งรายการให้เป็น <i>ตัวชี้ + ข้อเท็จจริงเชิงโครงสร้าง + อะตอมของเนื้อหา</i> ตัวเลข วันที่ จำนวนเงิน และรุ่นของสินค้ายังคงอยู่ครบในทุกชั้น; <code>expand()</code> กู้คืนข้อความต้นฉบับแบบไบต์ต่อไบต์และตรวจสอบแฮชให้</td></tr>
<tr><td><b>บัญชีตรวจสอบแบบ hash chain</b></td><td>ห่วงโซ่ SHA-256; <code>verify_integrity()</code> ตรวจจับการแก้ไขและระบุได้ว่าเป็นรายการใดที่เปลี่ยนไป</td></tr>
<tr><td><b>Async API และเหตุการณ์</b></td><td><code>AsyncMemory</code> สำหรับการเขียนปริมาณสูง พร้อมบันทึกการดำเนินการแบบถาวร เพื่อให้การเขียนที่ถูกรับไว้แล้วยังมองเห็นได้ข้ามโปรเซส</td></tr>
<tr><td><b>ปรับให้เหมาะกับภาษาจีน</b></td><td>การตัดคำแบบ Bigram + FTS5 + พจนานุกรมคำพ้องที่มีมาให้ พร้อมรองรับตัวอักษรละตินเต็มรูปแบบ</td></tr>
<tr><td><b>ระบบตรวจความปลอดภัยก่อนเขียน</b></td><td>ตรวจจับข้อมูลรับรอง Unicode ที่มองไม่เห็น และการแทรก HTML ก่อนที่การเขียนจะถูกบันทึก พร้อมปิดบังข้อมูลในระดับฟิลด์</td></tr>
</table>

---

## 🔌 การผสานรวม

อะแดปเตอร์ทุกตัวเป็นทางเลือก อะแดปเตอร์แบบ **stdlib** ไม่ต้องมีแพ็กเกจของบุคคลที่สามเลย
— สื่อสาร HTTP ตรงผ่าน `urllib` ส่วนอะแดปเตอร์แบบ **sdk** จะนำเข้า SDK แบบ lazy
และบอกคุณชัดเจนว่าขาดแพ็กเกจใด

### ผู้ให้บริการ LLM (20)

| ช่องทางการรับส่ง | ผู้ให้บริการ |
| --- | --- |
| **stdlib HTTP** | `openai` `openai_structured` `azure_openai` `azure_openai_structured` `ollama` `anthropic` `gemini` `groq` `together` `deepseek` `minimax` `xai` `sarvam` `openrouter` `litellm` `lmstudio` `vllm` |
| **sdk** | `langchain` `aws_bedrock` |
| **ในตัว** | `rules` — ตัวสกัดออฟไลน์ที่ให้ผลแน่นอนเหมือนเดิมทุกครั้ง จึงทำให้ `add()` ทำงานได้แม้ไม่ได้ตั้งค่าโมเดลใด ๆ เลย |

### ตัวสร้างเวกเตอร์ฝัง (13)

| ช่องทางการรับส่ง | ผู้ให้บริการ |
| --- | --- |
| **stdlib HTTP** | `openai` `azure_openai` `ollama` `gemini` `vertexai` `together` `lmstudio` `huggingface` |
| **sdk** | `fastembed` `langchain` `aws_bedrock` |
| **ในตัว** | `builtin` (128 มิติ, ไม่พึ่งพาไลบรารีภายนอก, ให้ผลแน่นอนเหมือนเดิม) · `hashing` (กี่มิติก็ได้, ออฟไลน์) |

### ฐานข้อมูลเวกเตอร์ (28)

| ช่องทางการรับส่ง | ฐานข้อมูลเวกเตอร์ |
| --- | --- |
| **ฝังในตัว** | `builtin` (ไฟล์ SQLite ไฟล์เดียวเก็บทั้งหน่วยความจำและเวกเตอร์) · `memory` · `generic` (REST แบบประกาศ) |
| **stdlib HTTP** | `qdrant` `pinecone` `elasticsearch` `opensearch` `weaviate` `upstash_vector` `turbopuffer` |
| **sdk** | `chroma` `pgvector` `milvus` `mongodb` `redis` `valkey` `azure_ai_search` `azure_mysql` `baidu` `cassandra` `databricks` `faiss` `langchain` `neptune` `oracledb` `s3_vectors` `supabase` `vertex_ai_vector_search` |

### ฐานข้อมูลกราฟ (6)

`builtin` (ไตรภาค SQLite แบบเนทีฟ) · `neo4j` · `memgraph` · `neptune` · `kuzu` · `sparql` (จุดปลาย SPARQL 1.1 ใดก็ได้)

### ตัวจัดอันดับใหม่ (5)

`llm` · `cohere` · `zero_entropy` · `huggingface` · `sentence_transformer`

### อะแดปเตอร์ของเฟรมเวิร์ก

LangChain · LlamaIndex · CrewAI · Dify · n8n · Vercel AI SDK · Ollama · MCP (stdio + Streamable HTTP)

---

## 🛠 เซิร์ฟเวอร์ MCP

ทำงานผ่าน stdio JSON-RPC:

```bash
export MNEMOSYNE_MCP_TOKEN="your-secret-token"   # ไม่บังคับ แต่แนะนำให้ตั้ง
python -m mnemosyne.webui.mcp_server --brain-dir ./mem --namespace default
```

**31 เครื่องมือ** — 20 เครื่องมือแบบเนทีฟ บวกอีก 11 เครื่องมือที่นำชื่อเครื่องมือ
หน่วยความจำของเอเจนต์แบบที่ใช้กันทั่วไปมาใช้ซ้ำ เพื่อให้ไคลเอนต์ MCP ที่มีอยู่แล้ว
ชี้มาที่ Mnemosyne ได้โดยไม่ต้องเขียนนิยามเครื่องมือใหม่

**เนทีฟ (20):**

| เครื่องมือ | วัตถุประสงค์ |
| --- | --- |
| `retain` | จัดเก็บหน่วยความจำหนึ่งรายการ |
| `recall` | เรียกคืนหน่วยความจำ |
| `retain_batch` | เขียนแบบเป็นชุด เร็วกว่าประมาณ 15 เท่า |
| `forget` | ลืมหน่วยความจำหนึ่งรายการ — ด้วย id หรือด้วยการค้นหาโดยใช้ภาษาธรรมชาติ |
| `capsule` | บีบอัดหน่วยความจำหนึ่งรายการให้เป็น ตัวชี้ + ข้อเท็จจริง + อะตอม |
| `expand` | กู้คืนข้อความต้นฉบับของแคปซูลแบบไบต์ต่อไบต์ |
| `recall_health` | ตัวชี้วัดคุณภาพการเรียกคืนแบบอ่านอย่างเดียว |
| `consolidate` | รวมหน่วยความจำที่ใกล้ซ้ำกันให้เหลือหนึ่งรายการแทน |
| `reflect` | สถิติ เอนทิตีที่พบบ่อย การตรวจจับความขัดแย้ง รูปแบบทางความคิด |
| `dedup` | ตรวจจับรายการซ้ำและรายการใกล้ซ้ำ |
| `graph_query` | การเดินกราฟความรู้ |
| `temporal_query` | การสืบค้นสายเวอร์ชัน |
| `list_projects` | แสดงรายการโปรเจกต์ที่แยกออกจากกัน |
| `doctor` | ตรวจสุขภาพ — ความสมบูรณ์ จำนวน ดิสก์ สถานะแบ็กเอนด์ |
| `stats` | สถิติขณะทำงาน |
| `audit` | การสืบค้นห่วงโซ่การตรวจสอบ |
| `confidence_history` | เส้นทางของค่าความเชื่อมั่น |
| `memory/export-v1` | ส่งออกผ่าน Memory Exchange Protocol |
| `memory/import-v1` | นำเข้าผ่าน Memory Exchange Protocol |
| `memory/claim` | เข้ารับช่วงหน่วยความจำจากการส่งออกภายนอก |

**เข้ากันได้กับไคลเอนต์ (11):**

| เครื่องมือ | วัตถุประสงค์ |
| --- | --- |
| `add_memory` | บันทึกข้อความหรือประวัติบทสนทนาให้ผู้ใช้/เอเจนต์ |
| `search_memories` | ค้นหาเชิงความหมายพร้อมตัวกรอง |
| `get_memories` | การกรองเชิงโครงสร้าง + รายการแบบแบ่งหน้า |
| `get_memory` | ดึงรายการเดียวด้วย id |
| `update_memory` | เขียนทับข้อความและ/หรือเมทาดาทา |
| `delete_memory` | ลบหนึ่งรายการ |
| `delete_all_memories` | ล้างข้อมูลของขอบเขตหนึ่ง |
| `delete_entities` | ลบเอนทิตีและลบต่อเนื่องตามลำดับชั้น |
| `list_entities` | แสดงรายการ users/agents/apps/runs |
| `list_events` | แสดงรายการการดำเนินการกับหน่วยความจำ |
| `get_event_status` | สอบถามสถานะการดำเนินการแบบอะซิงโครนัส |

---

## 🌐 REST API แบบโฮสต์เอง

โปรเซสเดียว พอร์ตเดียว รองรับเฮดเดอร์ยืนยันตัวตนแบบ `X-API-Key`, `Bearer` และ `Token`
คอนโซลและ API ใช้ตัวรับฟังเดียวกัน

| เมธอด | เส้นทาง | วัตถุประสงค์ |
| --- | --- | --- |
| `GET` | `/v1/status/` | ตรวจการทำงาน + รายงานการตั้งค่าปัจจุบัน |
| `GET` | `/v1/providers/` | ผู้ให้บริการทั้งหมดและความพร้อมใช้งานขณะนี้ |
| `POST` | `/v3/memories/add/` | สกัดและจัดเก็บ (อะซิงโครนัส คืนค่าเป็น event id) |
| `POST` | `/v3/memories/search/` | ค้นหาเชิงความหมาย |
| `POST` | `/v3/memories/get-all/` | รายการพร้อมตัวกรอง |
| `GET` / `PUT` / `DELETE` | `/v3/memories/{id}/` | ดึง / แก้ไข / ลบหนึ่งรายการ |
| `DELETE` | `/v3/memories/` | ล้างข้อมูลของขอบเขตหนึ่ง |
| `GET` | `/v3/memories/{id}/history/` | ประวัติการเปลี่ยนแปลง |
| `GET` | `/v1/event/{id}/` · `/v1/events/` | สอบถาม / แสดงรายการการดำเนินการ |
| `GET` / `DELETE` | `/v2/entities/` | แสดง / ลบขอบเขต |
| `POST` | `/v3/graph/{add,search,get-all,delete-all}/` | หน่วยความจำแบบกราฟ |
| `POST` | `/v1/capsule/` · `/v1/expand/` | การบีบอัดแบบไม่สูญเสียข้อมูล |
| `GET` | `/v1/integrity/` | การตรวจสอบบัญชี |
| `GET` / `POST` / `DELETE` | `/v1/keys/` | การจัดการ API key |

---

## 🧠 Python API

```python
from mnemosyne import Memory, AsyncMemory, MemoryClient

# --- การสกัด / ขอบเขต / ตัวกรอง -------------------------------------------------
m = Memory()
m.add([{"role": "user", "content": "I moved to Berlin in 2023."}],
      user_id="alice", metadata={"source": "onboarding"},
      observation_date="2023-06-01")
m.add("The invoice number is INV-2024-001.", user_id="alice", immutable=True)

hits = m.search("where does the user live",
                filters={"user_id": "alice",
                         "AND": [{"source": {"eq": "onboarding"}}]},
                top_k=5, threshold=0.1, rerank=False, explain=True)

# --- มัลติโมดัล ----------------------------------------------------------------
m.add([{"role": "user", "content": [
    {"type": "text", "text": "My new desk."},
    {"type": "image_url", "image_url": {"url": "https://example.com/desk.jpg"}},
]}], user_id="alice")

# --- หน่วยความจำกราฟ -----------------------------------------------------------
m.graph_add("Jobs founded Apple in Cupertino.", user_id="alice")
m.graph_search("Apple", filters={"user_id": "alice"})

# --- Async และเหตุการณ์ --------------------------------------------------------
async def ingest():
    am = AsyncMemory()
    await am.add_many([{"messages": t, "options": {"user_id": "alice"}}
                       for t in transcripts])
```

`Memory`, `AsyncMemory` และ `MemoryClient` ยังรับรูปแบบการเรียกใช้หน่วยความจำของ
เอเจนต์แบบที่ใช้กันทั่วไปซึ่งไลบรารีหน่วยความจำอื่นใช้ด้วย โค้ดที่เขียนตามรูปแบบนั้นไว้แล้ว
จึงสลับมาใช้ได้โดยแก้เพียงบรรทัด import ดู
[docs/COMPATIBILITY.md](docs/COMPATIBILITY.md)

ความสามารถของเอนจินเองแขวนอยู่บนออบเจกต์เดียวกัน:

```python
from mnemosyne import MemoryBrain

brain = MemoryBrain("./memories", enable_embeddings=True)
brain.ensure_init()
brain.retain("His laptop is an ASUS VivoBook Pro 14", fast=True)

results = brain.recall("what are that machine's specs", k=5)
results, cost = brain.recall("that machine's specs", k=5, budget_tokens=100)

cap = brain.capsule("<memory_id>", budget_tokens=60)   # ตัวชี้ + ข้อเท็จจริง + อะตอม
brain.expand(cap["ref"])                                # กู้คืนแบบไบต์ต่อไบต์
brain.verify_integrity()                                # ตรวจสอบบัญชี SHA-256
```

---

## 📂 โครงสร้างไดเรกทอรี

```
mnemosyne/
├── api/                 # API หน่วยความจำ: Memory / AsyncMemory / MemoryClient
│   ├── memory.py        #   ไคลเอนต์ที่ขับเคลื่อนด้วยเอนจิน
│   ├── config.py        #   MemoryConfig + การตรวจความสอดคล้องของมิติ
│   ├── filters.py       #   ภาษาตัวกรอง -> เพรดิเคต
│   ├── extract.py       #   การสกัดแบบ ADD-only รอบเดียว
│   ├── multimodal.py    #   การแยกวิเคราะห์ไฟล์แนบรูปภาพ / เสียง
│   ├── events.py        #   บันทึกการดำเนินการแบบถาวร
│   └── client.py        #   การรับส่งแบบฝังในตัว + HTTP
├── providers/           # อะแดปเตอร์คอมโพเนนต์แบบเลือกได้ (รวม 72 ตัว)
│   ├── llms.py          #   ผู้ให้บริการ LLM 20 ราย
│   ├── embedders.py     #   ผู้ให้บริการตัวสร้างเวกเตอร์ฝัง 13 ราย
│   ├── vector_stores.py #   ฐานข้อมูลเวกเตอร์ 28 ตัว
│   ├── graph_stores.py  #   ฐานข้อมูลกราฟ 6 ตัว
│   ├── rerankers.py     #   ตัวจัดอันดับใหม่ 5 ตัว
│   ├── vision.py        #   รูปแบบ wire ของภาพสามแบบ
│   └── transport.py     #   HTTP จาก stdlib + การลองซ้ำ + การปิดบังข้อมูลรับรอง
├── brain.py             # MemoryBrain — ส่วนหน้าของเอนจิน
├── capsule.py           # การบีบอัดแบบไม่สูญเสียข้อมูล AIC
├── retrieval.py         # การผสานหลายสัญญาณและการปรับเทียบความเกี่ยวข้อง
├── graph.py             # ที่เก็บไตรภาคเชิงเวลา
├── notary.py            # ไปป์ไลน์ความเชื่อถือก่อนการเขียน
├── cli.py               # CLI แบบเนทีฟ
├── api_cli.py           # CLI ของ API ฝั่งไคลเอนต์
└── webui/
    ├── web_server.py    # โฮสต์คอนโซล + REST
    ├── api_routes.py    # เส้นทาง /v1 /v2 /v3
    ├── mcp_server.py    # เครื่องมือ MCP แบบเนทีฟ 20 รายการ
    └── mcp_api.py       # เครื่องมือ MCP ที่เข้ากันได้กับไคลเอนต์ 11 รายการ

storage/                 # แบ็กเอนด์ SQLite, บัญชีแบบ hash chain, SDK ปลั๊กอิน
security/                # การตรวจจับความขัดแย้ง, การรายงานความปลอดภัย
scripts/                 # สคริปต์ตรวจสอบ
docs/                    # คู่มือการยอมรับ, กลยุทธ์การเรียกคืน, ความเข้ากันได้
```

---

## ✅ การทดสอบ

```bash
python verify.py                              # ตรวจสอบตัวเอง
python scripts/verify_api.py                  # ตรวจสอบ API ฝั่งไคลเอนต์, ออฟไลน์ทั้งหมด
python scripts/verify_memory_lifecycle.py --brain-dir ./mem --src-root .
python scripts/verify_precision_recall.py     # การถดถอยของ precision แบบออฟไลน์
python scripts/verify_recall_quality.py       # คุณภาพการเรียกคืนแบบครบวงจร
```

---

## 📚 เอกสาร

- [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) — รูปแบบการเรียกใช้หน่วยความจำของเอเจนต์แบบที่ใช้กันทั่วไป
- [docs/ACCEPTANCE_GUIDE.md](docs/ACCEPTANCE_GUIDE.md) — เกณฑ์การยอมรับและสคริปต์ที่ใช้กับแต่ละข้อ
- [docs/RECALL_STRATEGY.md](docs/RECALL_STRATEGY.md) — การประกอบการเรียกคืนและงบประมาณโทเคน
- [docs/KNOWN_DEFECTS.md](docs/KNOWN_DEFECTS.md) — ข้อบกพร่องที่ยืนยันแล้ว พร้อมผลการวัดและการแก้ไข
- [docs/DEPLOY_DEEPSEEK_HARNESS.md](docs/DEPLOY_DEEPSEEK_HARNESS.md) — ขั้นตอนการปรับใช้ MCP แบบลงมือทำ
- [CHANGELOG.md](CHANGELOG.md) — ประวัติเวอร์ชัน

---

## 📄 สัญญาอนุญาต

MIT License — see [LICENSE](LICENSE).

สร้างขึ้นโดยผู้มีส่วนร่วมของ Mnemosyne OS
