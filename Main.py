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

with open('cleanPrompt.txt', 'r') as file:
    clean_instructions = file.read()

query_prompt = input("How can I help? ")

while "EXIT" not in query_prompt:
    output = agent.run(system_instructions, query_prompt)
    output = ast.literal_eval(output)
    unformated_result = orchestrator.run(output)

    formated_result = agent.run(clean_instructions, unformated_result)
    print(formated_result)
    query_prompt = input("How can I help? ")

