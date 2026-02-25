import os
from llmproxy import LLMProxy

from config import (
    USER_ID,
    MODEL,
    COURSE_RAG_THRESHOLD,
    COURSE_RAG_K,
    MEM_RAG_THRESHOLD,
    MEM_RAG_K,
    normalize_course_id,
    memory_session_for_user,
    course_session_for_course,
    chat_session_for,
)
from rag import retrieve_ctx, rag_to_text, course_has_docs
from ingest import upload_pdf_to_course
from prompts import SCHEDULER_SYSTEM, build_scheduler_prompt
from memory import extract_and_store_memory


def main():
    client = LLMProxy()

    memory_session = memory_session_for_user(USER_ID)

    current_course_id = None
    course_session = None
    chat_session = f"chat_{normalize_course_id(USER_ID)}"

    print("Scheduler chatbot (LLMProxy)")
    print("Commands:")
    print("  /course <course_name>        switch course")
    print("  /upload <path_to_pdf>        upload syllabus or assignment PDF to current course")
    print("  /quit                        exit\n")
    print("Bot: Which course is this for? (example: COMP 160)\n")

    while True:
        user_msg = input("You: ").strip()
        if not user_msg:
            continue
        if user_msg.lower() == "/quit":
            break

        if user_msg.lower().startswith("/course "):
            raw_course = user_msg[8:].strip()
            if not raw_course:
                print("\nBot: Please provide a course name after /course.\n")
                continue

            current_course_id = normalize_course_id(raw_course)
            course_session = course_session_for_course(current_course_id)
            chat_session = chat_session_for(USER_ID, current_course_id)

            client.upload_text(
                text=f"Current course is {raw_course}",
                session_id=memory_session,
                strategy="fixed",
            )

            print(f"\nBot: Got it, we will use {raw_course}.\n")
            continue

        if current_course_id is None:
            raw_course = user_msg
            current_course_id = normalize_course_id(raw_course)
            course_session = course_session_for_course(current_course_id)
            chat_session = chat_session_for(USER_ID, current_course_id)

            client.upload_text(
                text=f"Current course is {raw_course}",
                session_id=memory_session,
                strategy="fixed",
            )

            if not course_has_docs(client, course_session):
                bot_msg = (
                    f"Got it, {raw_course}.\n"
                    "I do not have your syllabus or assignment documents yet.\n"
                    "Please upload your syllabus PDF so I can plan accurately.\n\n"
                    "Use:\n"
                    "/upload /path/to/syllabus.pdf"
                )
                print(f"\nBot: {bot_msg}\n")
                extract_and_store_memory(client, user_msg, bot_msg, memory_session, chat_session)
                continue

            bot_msg = f"Got it, {raw_course}. What assignment do you want to plan?"
            print(f"\nBot: {bot_msg}\n")
            extract_and_store_memory(client, user_msg, bot_msg, memory_session, chat_session)
            continue

        # Course is set from here
        assert course_session is not None

        if user_msg.lower().startswith("/upload "):
            path = user_msg[8:].strip().strip('"').strip("'")
            if not path:
                print("\nBot: Please provide a PDF path after /upload.\n")
                continue

            try:
                upload_pdf_to_course(client, path, course_session)
            except FileNotFoundError:
                print("\nBot: I cannot find that file path. Please check it and try again.\n")
                continue

            bot_msg = "Uploaded. Tell me which assignment (or due date) you want to plan."
            print(f"\nBot: {bot_msg}\n")
            extract_and_store_memory(client, user_msg, bot_msg, memory_session, chat_session)
            continue

        if not course_has_docs(client, course_session):
            bot_msg = (
                "I still do not have your syllabus or assignment docs for this course.\n"
                "Please upload your syllabus PDF first:\n"
                "/upload /path/to/syllabus.pdf"
            )
            print(f"\nBot: {bot_msg}\n")
            extract_and_store_memory(client, user_msg, bot_msg, memory_session, chat_session)
            continue

        course_rag = retrieve_ctx(
            client,
            query=user_msg,
            session_id=course_session,
            threshold=COURSE_RAG_THRESHOLD,
            k=COURSE_RAG_K,
        )
        mem_rag = retrieve_ctx(
            client,
            query=user_msg,
            session_id=memory_session,
            threshold=MEM_RAG_THRESHOLD,
            k=MEM_RAG_K,
        )

        prompt = build_scheduler_prompt(user_msg, rag_to_text(course_rag), rag_to_text(mem_rag))

        bot_msg = client.generate(
            model=MODEL,
            system=SCHEDULER_SYSTEM,
            query=prompt,
            temperature=0.2,
            lastk=8,
            session_id=chat_session,
            rag_usage=False,
        )

        print(f"\nBot: {bot_msg}\n")
        extract_and_store_memory(client, user_msg, bot_msg, memory_session, chat_session)


if __name__ == "__main__":
    main()