"""
RAG Chain with Multi-Turn Chat Memory, 3-Source Attribution, and Qwen 3.8 27B on Groq.
Integrates:
  1. FAQs (CSV)
  2. Telecom User Guides (PDF)
  3. Resolved Support Tickets (SQLite)
"""
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_groq import ChatGroq

from retriever import build_retriever

load_dotenv()

SYSTEM_PROMPT = """You are a helpful and professional telecom customer care assistant.
Your job is to help customers resolve technical issues with their mobile service.

Use ONLY the context below to answer the customer's question.
The context comes from three verified knowledge sources:
1. Official FAQ entries (general policy, pricing, and how-to guides)
2. Telecom User Guide & Documentation (official technical manuals and specifications)
3. Past Resolved Support Tickets (real-world customer cases and technician resolutions)

When relevant, you may reference past ticket solutions (e.g. "According to past resolved support case #TK-001...") to provide practical, empirical troubleshooting steps.

If the context does not contain enough information to answer confidently, state so clearly and recommend calling 611 or using the MyTelecom app.

Context:
{context}
"""


def format_docs(docs: List[Document]) -> str:
    """Formats retrieved documents with clear source attribution tags."""
    sections = []
    for doc in docs:
        src = doc.metadata.get("source", "unknown").upper()
        if src == "TICKET":
            ticket_id = doc.metadata.get("ticket_id", "N/A")
            cat = doc.metadata.get("category", "")
            sections.append(f"[RESOLVED SUPPORT TICKET #{ticket_id} | Category: {cat}]\n{doc.page_content}")
        elif src == "FAQ":
            faq_id = doc.metadata.get("faq_id", "")
            cat = doc.metadata.get("category", "")
            sections.append(f"[OFFICIAL FAQ #{faq_id} | Category: {cat}]\n{doc.page_content}")
        elif src == "GUIDE":
            chunk_idx = doc.metadata.get("chunk_index", "")
            sections.append(f"[TELECOM USER GUIDE | Chunk #{chunk_idx}]\n{doc.page_content}")
        else:
            sections.append(f"[{src}]\n{doc.page_content}")
    return "\n\n---\n\n".join(sections)


def extract_source_attributions(docs: List[Document]) -> List[Dict[str, Any]]:
    """Extracts clean metadata and snippets for UI and API citation."""
    attributions = []
    for doc in docs:
        src = doc.metadata.get("source", "unknown").capitalize()
        if src.lower() == "ticket":
            src_label = "Support Ticket"
            ref = f"#{doc.metadata.get('ticket_id', 'N/A')}"
        elif src.lower() == "faq":
            src_label = "FAQ"
            ref = f"Entry #{doc.metadata.get('faq_id', 'N/A')}"
        elif src.lower() == "guide":
            src_label = "User Guide"
            ref = f"Chunk #{doc.metadata.get('chunk_index', '0')}"
        else:
            src_label = src
            ref = "Doc"

        attributions.append({
            "source_type": src_label,
            "reference": ref,
            "category": doc.metadata.get("category", "General"),
            "snippet": doc.page_content[:200] + ("..." if len(doc.page_content) > 200 else ""),
            "full_content": doc.page_content
        })
    return attributions


def build_llm():
    """Instantiates the Groq Chat model with active Qwen 3.8 27B."""
    return ChatGroq(
        model="qwen/qwen3.8-27b",
        temperature=0,
        max_tokens=None,
        reasoning_format="parsed",
        timeout=None,
        max_retries=2,
    )


def build_chain():
    """Builds the single-turn RAG chain."""
    retriever = build_retriever()
    llm = build_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def build_conversational_chain():
    """
    Builds a multi-turn conversational RAG chain that supports chat history.
    Takes inputs: {"question": str, "chat_history": List[BaseMessage]}
    """
    retriever = build_retriever()
    llm = build_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])

    def get_context(input_dict: dict) -> str:
        query = input_dict["question"]
        docs = retriever.invoke(query)
        return format_docs(docs)

    chain = (
        {
            "context": get_context,
            "question": lambda x: x["question"],
            "chat_history": lambda x: x.get("chat_history", []),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
