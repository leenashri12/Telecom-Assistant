"""
Builds a merged retriever across all three Chroma collections:
  - faq     : FAQ entries (1 row = 1 doc)
  - tickets : Resolved support tickets from SQLite (1 ticket = 1 doc)
  - guides  : PDF guide chunks (RecursiveCharacterTextSplitter)
"""
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document

CHROMA_DIR  = os.environ.get("CHROMA_DIR", "chroma_store")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def ensure_knowledge_base():
    """Auto-ingest data sources if running on a fresh cloud container where chroma_store is not present."""
    sqlite_file = os.path.join(CHROMA_DIR, "chroma.sqlite3")
    if not os.path.exists(CHROMA_DIR) or not os.path.exists(sqlite_file):
        print(f"Chroma store '{CHROMA_DIR}' not found. Auto-indexing data sources...")
        try:
            import ingest_faq
            import ingest_tickets
            import ingest_pdf
            ingest_faq.main()
            ingest_tickets.main()
            ingest_pdf.main()
            print("All knowledge collections indexed successfully!")
        except Exception as err:
            print(f"Auto-ingest warning: {err}")


def build_retriever(
    k_faq: int = 3,
    k_tickets: int = 3,
    k_guides: int = 3,
) -> RunnableLambda:
    ensure_knowledge_base()
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBED_MODEL,
            model_kwargs={"local_files_only": True}
        )
    except Exception:
        embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    faq_store = Chroma(
        collection_name="faq",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
    tickets_store = Chroma(
        collection_name="tickets",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
    guides_store = Chroma(
        collection_name="guides",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    faq_retriever     = faq_store.as_retriever(search_kwargs={"k": k_faq})
    tickets_retriever = tickets_store.as_retriever(search_kwargs={"k": k_tickets})
    guides_retriever  = guides_store.as_retriever(search_kwargs={"k": k_guides})

    def retrieve(query: str) -> list[Document]:
        return (
            faq_retriever.invoke(query)
            + tickets_retriever.invoke(query)
            + guides_retriever.invoke(query)
        )

    return RunnableLambda(retrieve)
