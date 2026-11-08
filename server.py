"""
FastAPI Backend Server for Telecom Customer Assistant.
Provides REST and Streaming Endpoints for RAG Pipeline, Chat Memory, and Evaluation.
Run with: uvicorn server:app --host 0.0.0.0 --port 8000 --reload
"""
import os
import uuid
import json
import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from retriever import build_retriever
from rag_chain import build_chain, build_conversational_chain, extract_source_attributions
from evaluate_rag import run_evaluation, TEST_SET

# Initialize FastAPI App
app = FastAPI(
    title="Telecom Customer Care RAG API",
    description="Enterprise Backend for RAG Chatbot integrating FAQs, SQLite Support Tickets, and PDF Guides.",
    version="2.0.0",
)

# Enable CORS for Streamlit and external frontend web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory Session Memory Store: {session_id: List[BaseMessage]}
session_memory: Dict[str, List[Any]] = {}

# Cached RAG components
retriever = build_retriever()
chain = build_chain()
conversational_chain = build_conversational_chain()


# ---------------------------------------------------------------------------
# Pydantic Request / Response Models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    question: str = Field(..., example="How do I activate international roaming?")
    session_id: Optional[str] = Field(default=None, example="user_session_123")


class SourceCitation(BaseModel):
    source_type: str
    reference: str
    category: str
    snippet: str


class ChatResponse(BaseModel):
    session_id: str
    question: str
    answer: str
    sources: List[SourceCitation]


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "Telecom Customer Care RAG API",
        "status": "online",
        "documentation": "/docs",
        "endpoints": [
            "POST /api/chat",
            "POST /api/chat/stream",
            "GET /api/sources",
            "DELETE /api/chat/history/{session_id}",
            "POST /api/evaluate",
            "GET /health",
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "llm_engine": "qwen/qwen3.8-27b (Groq LPU)",
        "vector_store": "ChromaDB",
        "active_sources": ["FAQ (CSV)", "Support Tickets (SQLite)", "Telecom User Guide (PDF)"],
    }


@app.get("/api/sources")
def get_sources():
    """Returns metadata about all indexed knowledge bases."""
    return {
        "sources": [
            {
                "id": "faq",
                "name": "Official FAQ Repository",
                "format": "Structured CSV",
                "description": "General mobile policies, billing cycles, roaming rules, and how-tos.",
                "total_documents": 25,
            },
            {
                "id": "tickets",
                "name": "Resolved Support Tickets",
                "format": "Relational SQLite Database",
                "description": "Historical tier-1/tier-2 customer troubleshooting cases with confirmed technician fixes.",
                "total_documents": 19,
            },
            {
                "id": "guides",
                "name": "Telecom Technical User Guide",
                "format": "Unstructured PDF (Chunked)",
                "description": "Official 9-page hardware, VoLTE, VoWiFi, and 5G network manual.",
                "total_chunks": 37,
            },
        ]
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Standard Non-Streaming Chat Endpoint.
    Maintains conversational session history and returns structured source citations.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    session_id = request.session_id or str(uuid.uuid4())
    history = session_memory.setdefault(session_id, [])

    # 1. Retrieve context & extract source attributions
    docs = retriever.invoke(request.question)
    citations = extract_source_attributions(docs)

    # 2. Invoke conversational chain with chat history
    from langchain_core.messages import HumanMessage, AIMessage
    formatted_history = []
    for msg in history:
        if msg.get("role") == "user":
            formatted_history.append(HumanMessage(content=msg["content"]))
        else:
            formatted_history.append(AIMessage(content=msg["content"]))

    answer = conversational_chain.invoke({
        "question": request.question,
        "chat_history": formatted_history,
    })

    # 3. Update session memory
    history.append({"role": "user", "content": request.question})
    history.append({"role": "assistant", "content": answer})

    # Limit memory to last 10 messages
    if len(history) > 10:
        session_memory[session_id] = history[-10:]

    return ChatResponse(
        session_id=session_id,
        question=request.question,
        answer=answer,
        sources=[SourceCitation(**c) for c in citations]
    )


@app.post("/api/chat/stream")
def chat_stream_endpoint(request: ChatRequest):
    """
    Server-Sent Events / Streaming Token Endpoint.
    Streams AI tokens in real-time.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    session_id = request.session_id or str(uuid.uuid4())

    def event_generator():
        # Retrieve context
        docs = retriever.invoke(request.question)
        citations = extract_source_attributions(docs)

        # First send citation metadata as a header event
        yield f"data: {json.dumps({'type': 'citations', 'sources': citations})}\n\n"

        # Stream LLM tokens
        full_text = ""
        for chunk in chain.stream(request.question):
            full_text += chunk
            yield f"data: {json.dumps({'type': 'token', 'token': chunk})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.delete("/api/chat/history/{session_id}")
def clear_history(session_id: str):
    """Clears conversational session history for a user."""
    if session_id in session_memory:
        del session_memory[session_id]
        return {"status": "cleared", "session_id": session_id}
    return {"status": "not_found", "session_id": session_id}


@app.post("/api/evaluate")
def run_evaluation_endpoint():
    """Runs the golden benchmark evaluation suite and returns metrics."""
    metrics = run_evaluation()
    return metrics
