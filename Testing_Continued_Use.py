import requests
from llmproxy import LLMProxy
import random
from Orchestrator import Orchestrator
import ast

client = LLMProxy()
orchestrator = Orchestrator()

system_instructions = ""

with open('calendarPrompt.txt', 'r') as file:
    calendar_instructions = file.read()

with open('calendarPrompt.txt', 'r') as file:
    calendar_instructions = file.read()

model_name = '4o-mini'
temperature_value = 0.0
last_queries = 4
session_id_value = 'conversation-' + str(random.random())
rag_enabled = False
no_action = True

query_prompt = input("what would you like to do?")
check_if_time_was_accurate()

while "EXIT" not in query_prompt:
    output = client.generate(
            model = model_name,
            system = system_instructions,
            query = query_prompt,
            temperature = temperature_value,
            lastk = last_queries,
            session_id = session_id_value,
            rag_usage = rag_enabled,
    )['result']
    print(output)
    output = ast.literal_eval(output)
    result = orchestrator.run(output)
    print(output['response'])
    query_prompt = input("Tell me more: ") + "Prev result: " + str(result)

def check_if_time_was_accurate():
    output = client.generate(
            model = model_name,
            system = system_instructions,
            query = query_prompt,
            temperature = temperature_value,
            lastk = last_queries,
            session_id = session_id_value,
            rag_usage = rag_enabled,
    )['result']