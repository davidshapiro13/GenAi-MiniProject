#Code for working with RAG storage

from llmproxy import LLMProxy
from typing import Any, List, Dict


def retrieve_ctx(
    client: LLMProxy,
    query: str,
    session_id: str,
    threshold: float,
    k: int,
):
    return client.retrieve(
        query=query,
        session_id=session_id,
        rag_threshold=threshold,
        rag_k=k,
    )


def rag_to_text(rag: Any) -> str:
    if not rag:
        return ""

    parts: List[str] = []
    for i, collection in enumerate(rag, start=1):
        doc_summary = collection.get("doc_summary", "")
        chunks = collection.get("chunks", [])
        block_lines: List[str] = []
        if doc_summary:
            block_lines.append(f"#{i} {doc_summary}".strip())
        for j, c in enumerate(chunks, start=1):
            c = (c or "").strip()
            if c:
                block_lines.append(f"#{i}.{j} {c}")
        if block_lines:
            parts.append("\n".join(block_lines))

    return "\n\n".join(parts).strip()


def course_has_docs(client: LLMProxy, course_session: str) -> bool:
    hits = retrieve_ctx(
        client,
        query="syllabus grading policies assignments office hours late policy",
        session_id=course_session,
        threshold=0.2,
        k=3,
    )
    return bool(hits)