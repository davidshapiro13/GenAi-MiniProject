from llmproxy import LLMProxy
from Orchestrator import Orchestrator
import ast
from AI import AI
import random
from ai_prompts import SCHEDULER_SYSTEM, CLEAN_PROMPT, GET_SYLLABUS, WORK_TIME, build_scheduler_prompt
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
    print("To better understand you, I have a few questions about your work process: ")
    paper_response = input("Roughly how many hours would it take you to write a 4-page research paper? ")
    math_response = input("Roughly how long would it take you to solve 10 Calculus questions? ")
    most_time = input("What is the max amount of time you like to work in one sitting? ")
    work_time = agent.run(WORK_TIME, "Time for 4-page paper: " + paper_response + "; 10 calculus questions: " + math_response + "; Max time per sitting: " + most_time, session=memory_session)
    #Hunter, can you incorportate this work time in somehow?

    prompt = "Do you have a syllabus to add? What's the name of the course? "
    while True:
        query_prompt = input(prompt)
        output = agent.run(GET_SYLLABUS, query_prompt, session=memory_session)
        output = ast.literal_eval(output)
        if output['path'] != "" and output['name'] != "":
            agent.upload_rag(output['path'])
            time.sleep(4)
            return(output['name'])
        prompt = output['response']
        
if not previous_user:
    course_session = first_time_run()

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
    action = output.split(" ", 1)[0]
    if action in ["create", "update", "delete", "list"]:
        unformated_result = orchestrator.run(action, rag_to_text(course_rag) + " " + rag_to_text(mem_rag) + output.split(" ", 1)[1], query_prompt)
        formated_result = agent.run(CLEAN_PROMPT, unformated_result, session=memory_session)
        print(formated_result)
    else: 
        print(output)   
    query_prompt = input("You: ")