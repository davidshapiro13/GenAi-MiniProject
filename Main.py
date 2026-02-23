from llmproxy import LLMProxy
from Orchestrator import Orchestrator
import ast
from AI import AI
import random
from ai_prompts import SCHEDULER_SYSTEM, CLEAN_PROMPT, GET_SYLLABUS, build_scheduler_prompt
import time
from config import (
    MODEL,
    COURSE_RAG_THRESHOLD,
    COURSE_RAG_K,
    MEM_RAG_THRESHOLD,
    MEM_RAG_K,
    login,
    chat_session_for
)
from rag import retrieve_ctx, rag_to_text

client = LLMProxy()

print("Welcome to the PlannerAI - Your personal schedule planner.")

memory_session, user_id, previous_user = login()
course_session = None

agent = AI(memory_session=memory_session, chat_session=memory_session)
orchestrator = Orchestrator(agent)

def first_time_run():
    prompt = "Do you have a syllabus to add?"
    while True:
        print(prompt)
        query_prompt = input("You: ")
        output = agent.run(GET_SYLLABUS, query_prompt, session=memory_session)
        output = ast.literal_eval(output)
        if output['path'] != "":
            agent.upload_rag(output['path'])
            time.sleep(4)
            return
        prompt = output['response']
        
if not previous_user:
    first_time_run()

query_prompt = input("How can I help? ")
while "EXIT" not in query_prompt:

    course_rag = retrieve_ctx(
        client,
        query=query_prompt,
        session_id=course_session,
        threshold=COURSE_RAG_THRESHOLD,
        k=COURSE_RAG_K,
    )
    mem_rag = retrieve_ctx(
        client,
        query=query_prompt,
        session_id=memory_session,
        threshold=MEM_RAG_THRESHOLD,
        k=MEM_RAG_K,
    )

    system = build_scheduler_prompt(SCHEDULER_SYSTEM, rag_to_text(course_rag), rag_to_text(mem_rag))
    output = agent.run(system, query_prompt, session=memory_session)
    if output.startswith(("create", "update", "delete", "list")):
        action = output.split(":")[0]
        unformated_result = orchestrator.run(action, rag_to_text(course_rag) + " " + rag_to_text(mem_rag) + output.split(":", 1)[1], query_prompt)
        formated_result = agent.run(CLEAN_PROMPT, unformated_result, session=memory_session)
        print(formated_result)
    else: 
        print(output)   
    query_prompt = input("You: ")