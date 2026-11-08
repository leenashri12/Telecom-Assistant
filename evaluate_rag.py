"""
Automated RAG Evaluation Suite for Telecom Customer Assistant.
Tests retrieval precision, answer grounding, and latency across:
  1. FAQ Knowledge Base
  2. Support Tickets Database (SQLite)
  3. Telecom User Guide (PDF)
  4. Out-of-Domain Guardrails

Run with: python evaluate_rag.py
"""
import sys
import time
import json
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from retriever import build_retriever
from rag_chain import build_chain, extract_source_attributions

TEST_SET = [
    {
        "id": "TEST-01",
        "category": "FAQ - Roaming",
        "question": "What are the roaming charges in the EU without a bundle?",
        "expected_source": "FAQ",
        "key_facts": ["$10", "1.50", "bundle"],
    },
    {
        "id": "TEST-02",
        "category": "FAQ - SIM",
        "question": "How long does SIM activation typically take?",
        "expected_source": "FAQ",
        "key_facts": ["15 minutes", "1 hour"],
    },
    {
        "id": "TEST-03",
        "category": "FAQ - Billing",
        "question": "When is my bill payment due after generation?",
        "expected_source": "FAQ",
        "key_facts": ["14 days"],
    },
    {
        "id": "TEST-04",
        "category": "Ticket - APN Issue",
        "question": "How was the 'No internet access' issue resolved in past customer cases?",
        "expected_source": "Support Ticket",
        "key_facts": ["APN", "airplane mode", "internet.telecom.example"],
    },
    {
        "id": "TEST-05",
        "category": "Ticket - Data Sync",
        "question": "What steps were taken when a customer's data balance was not updating?",
        "expected_source": "Support Ticket",
        "key_facts": ["sync delay", "session token", "cache"],
    },
    {
        "id": "TEST-06",
        "category": "Ticket - Signal Drop",
        "question": "What compensation was given for intermittent signal drops due to a faulty tower antenna?",
        "expected_source": "Support Ticket",
        "key_facts": ["500 MB", "antenna", "replacement"],
    },
    {
        "id": "TEST-07",
        "category": "Guide - Fair Use",
        "question": "To what exact speed is mobile internet throttled when the high-speed data cap is reached?",
        "expected_source": "User Guide",
        "key_facts": ["512 kbps"],
    },
    {
        "id": "TEST-08",
        "category": "Guide - Voice",
        "question": "How does VoLTE provide HD voice calling over 4G?",
        "expected_source": "User Guide",
        "key_facts": ["VoLTE", "4G", "HD"],
    },
    {
        "id": "TEST-09",
        "category": "Guardrail - Out of Scope",
        "question": "How do I cancel my residential fiber optic broadband plan?",
        "expected_source": "Any",
        "key_facts": ["611", "MyTelecom"],
    },
]


def run_evaluation() -> Dict[str, Any]:
    print("=" * 70)
    print(" [RUNNING RAG EVALUATION SUITE: TELECOM CUSTOMER ASSISTANT]")
    print("=" * 70)

    retriever = build_retriever()
    chain = build_chain()

    results = []
    total_retrieval_hits = 0
    total_grounding_hits = 0
    total_latency = 0.0

    for idx, test in enumerate(TEST_SET, 1):
        q = test["question"]
        print(f"\n[{idx}/{len(TEST_SET)}] Evaluating: {q}")

        start_time = time.time()

        # 1. Evaluate Retrieval
        retrieved_docs = retriever.invoke(q)
        attributions = extract_source_attributions(retrieved_docs)
        retrieved_sources = [a["source_type"] for a in attributions]

        if test["expected_source"] == "Any":
            retrieval_hit = True
        else:
            retrieval_hit = any(test["expected_source"].lower() in s.lower() for s in retrieved_sources)

        if retrieval_hit:
            total_retrieval_hits += 1

        # 2. Evaluate Generation
        answer = chain.invoke(q)
        elapsed = time.time() - start_time
        total_latency += elapsed

        # 3. Evaluate Grounding (Key Facts Coverage)
        grounding_hits = [k for k in test["key_facts"] if k.lower() in answer.lower()]
        grounding_score = len(grounding_hits) / len(test["key_facts"])
        if grounding_score >= 0.5:
            total_grounding_hits += 1

        test_result = {
            "id": test["id"],
            "category": test["category"],
            "question": q,
            "retrieval_hit": retrieval_hit,
            "sources_retrieved": list(set(retrieved_sources)),
            "grounding_score": round(grounding_score * 100, 1),
            "latency_seconds": round(elapsed, 2),
            "generated_answer": answer[:150] + "..."
        }
        results.append(test_result)

        hit_str = "[PASS]" if retrieval_hit else "[FAIL]"
        print(f"   -> Retrieval Hit: {hit_str} (Sources: {', '.join(set(retrieved_sources))})")
        print(f"   -> Grounding: {round(grounding_score * 100, 1)}% | Latency: {round(elapsed, 2)}s")

    # Metrics Summary
    num_tests = len(TEST_SET)
    summary = {
        "total_tests": num_tests,
        "retrieval_accuracy": round((total_retrieval_hits / num_tests) * 100, 1),
        "grounding_accuracy": round((total_grounding_hits / num_tests) * 100, 1),
        "average_latency_sec": round(total_latency / num_tests, 2),
        "test_results": results
    }

    print("\n" + "=" * 70)
    print(" [EVALUATION SUMMARY]")
    print("=" * 70)
    print(f" Total Tests Run      : {summary['total_tests']}")
    print(f" Retrieval Accuracy   : {summary['retrieval_accuracy']}%")
    print(f" Grounding / Quality  : {summary['grounding_accuracy']}%")
    print(f" Average Latency      : {summary['average_latency_sec']} seconds")
    print("=" * 70)

    # Save report
    with open("rag_evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(" Report saved to 'rag_evaluation_report.json'\n")

    return summary


if __name__ == "__main__":
    run_evaluation()
