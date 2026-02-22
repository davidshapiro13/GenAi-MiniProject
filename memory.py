from __future__ import annotations

import json
from llmproxy import LLMProxy
from ai_prompts import MEMORY_EXTRACTOR_SYSTEM
from config import MODEL


def extract_and_store_memory(
    client: LLMProxy,
    user_msg: str,
    bot_msg: str,
    memory_session: str,
    chat_session: str,
) -> None:
    prompt = f"""
CHAT SNIPPET:
User: {user_msg}
Assistant: {bot_msg}

Extract ONE memory item at most.
""".strip()

    raw = client.generate(
        model=MODEL,
        system=MEMORY_EXTRACTOR_SYSTEM,
        query=prompt,
        temperature=0.0,
        lastk=0,
        session_id=chat_session,
        rag_usage=False,
    )

    try:
        data = json.loads(raw)
    except Exception:
        return

    if not data.get("should_store"):
        return

    mem = (data.get("memory_text") or "").strip()
    if not mem:
        return

    client.upload_text(
        text=mem,
        session_id=memory_session,
        strategy="fixed",
    )