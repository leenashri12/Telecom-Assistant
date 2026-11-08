"""
CLI entry point for Telecom Customer Assistant.
Features:
  - 3 Knowledge Sources: FAQ + Support Tickets + Technical Guides
  - Source Attribution display
  - Interactive Streaming Responses
Usage: python main.py
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

from dotenv import load_dotenv
from retriever import build_retriever
from rag_chain import build_chain, extract_source_attributions

load_dotenv()


def main():
    print("=" * 65)
    print("      TELECOM CUSTOMER ASSISTANT (ENTERPRISE RAG)")
    print(" Active Sources: FAQ (CSV) + Support Tickets (SQLite) + User Guide (PDF)")
    print("=" * 65)
    print("Type your question and press Enter. Type 'quit' to exit.\n")

    retriever = build_retriever()
    chain = build_chain()

    while True:
        try:
            question = input("\nCustomer: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        # Retrieve source attributions
        docs = retriever.invoke(question)
        citations = extract_source_attributions(docs)

        print("\nAssistant: ", end="", flush=True)
        for chunk in chain.stream(question):
            print(chunk, end="", flush=True)
        print("\n")

        # Display source citations
        unique_sources = set()
        for c in citations:
            unique_sources.add(f"{c['source_type']} {c['reference']} ({c['category']})")
        print("  [Sources Cited]:", " | ".join(unique_sources))


if __name__ == "__main__":
    main()
