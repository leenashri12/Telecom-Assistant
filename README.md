# 📡 Telecom Customer Assistant (Enterprise RAG)

A production-grade Retrieval-Augmented Generation (RAG) customer care assistant for telecommunication networks. It answers complex technical queries, billing rules, and connectivity issues by dynamically retrieving context across three knowledge sources and streaming answers using **Qwen 3.8 27B** via **Groq LPU**.

---

## 🏛️ System Architecture

```
User Query (Browser / REST API / CLI)
               │
               ▼
   FastAPI REST Layer / Streamlit UI
               │ (Chat Memory: Multi-Turn History)
               ▼
     Merged ChromaDB Retriever (Top-3 from each)
   ├── 1. Official FAQs (CSV)
   ├── 2. Resolved Support Tickets (SQLite Database)
   └── 3. Telecom Technical User Guide (Chunked PDF)
               │
               ▼ (Source Attribution & Grounded Formatting)
   ChatPromptTemplate + Qwen 3.8 27B (Groq)
               │
               ▼
   Streaming Response + Rich Source Citations
```

---

## 📂 Project Structure

```
Telecom_chatbot_addnal/
├── app.py                  # Streamlit Web UI (Chat, Memory, & Live Evaluation Dashboard)
├── server.py               # FastAPI Backend REST & Streaming Server
├── evaluate_rag.py         # Automated RAG Benchmark Evaluation Suite
├── main.py                 # Interactive CLI Chatbot
├── rag_chain.py            # LangChain RAG pipeline (Conversational Memory & Citations)
├── retriever.py            # Merges FAQ, Tickets DB, and PDF Guide collections
├── ingest_faq.py           # Ingestion script for data/faq.csv
├── ingest_tickets.py       # Ingestion script for data/tickets.db (SQLite)
├── ingest_pdf.py           # Ingestion script for data/telecom_guide.pdf
├── data/
│   ├── faq.csv             # 25 FAQ Q&A entries
│   ├── tickets.db          # 19 resolved customer troubleshooting tickets (SQLite)
│   └── telecom_guide.pdf   # 9-page technical hardware & network manual
├── chroma_store/           # Persistent ChromaDB vector database
├── pyproject.toml          # Project configuration & dependencies
├── uv.lock                 # Deterministic dependency lock
├── .env.example            # Environment variables template
└── .env                    # Active API configuration
```

---

## 🚀 Key Features

1. **Three-Source Knowledge Grounding:**
   - **Official FAQ:** Policy, billing cycles, SIM activation, and international roaming.
   - **Resolved Support Tickets:** Real-world empirical cases with confirmed technician resolutions.
   - **Technical User Guide:** Detailed 5G, VoLTE, VoWiFi, and device manual specifications.
2. **Multi-Turn Chat Memory:**
   - Maintains conversational session context across multiple turns.
3. **Rich Source Attribution (Citations):**
   - Automatically cites and displays exact document sources (`FAQ`, `Support Ticket #TK-...`, `User Guide`).
4. **FastAPI Microservice Backend:**
   - Production REST endpoints, CORS middleware, and Server-Sent Events (SSE) real-time streaming.
5. **Built-in RAG Evaluation Suite:**
   - Benchmark evaluation testing retrieval hit rate (100%), answer grounding (100%), and latency.

---

## ⚙️ Quick Start

### 1. Configure Environment
Ensure your `.env` contains your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Ingest Data (Pre-built, or run once if updated)
```powershell
python ingest_faq.py
python ingest_tickets.py
python ingest_pdf.py
```

### 3. Run the Application

#### Option A: Streamlit Web UI (Recommended)
```powershell
python -m streamlit run app.py
```
* Access at **`http://localhost:8501`**
* Features interactive chat with memory, sample questions, source citations, and the **Live Evaluation Benchmark Dashboard**.

#### Option B: FastAPI Backend Server
```powershell
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
* Interactive Swagger API documentation: **`http://localhost:8000/docs`**

#### Option C: Automated Benchmark Evaluation
```powershell
python evaluate_rag.py
```
* Executes the 9-point benchmark suite and outputs accuracy scores to `rag_evaluation_report.json`.

#### Option D: Terminal CLI
```powershell
python main.py
```
