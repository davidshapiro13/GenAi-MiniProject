import requests
from llmproxy import LLMProxy
import random
from Orchestrator import Orchestrator
import ast
from AI import AI

client = LLMProxy()
orchestrator = Orchestrator()
agent = AI()

system_instructions = ""

with open('calendarPrompt.txt', 'r') as file:
    system_instructions = file.read()

model_name = '4o-mini'
temperature_value = 0.0
last_queries = 4
session_id_value = 'conversation-' + str(random.random())
rag_enabled = False
no_action = True

query_prompt = input("what would you like to do?")

while "EXIT" not in query_prompt:
    output = agent.run(system_instructions, query_prompt)
    print(output)
    output = ast.literal_eval(output)
    result = orchestrator.run(output)
    print(output['response'])
    query_prompt = input("Tell me more: ") + "Prev result: " + str(result)

