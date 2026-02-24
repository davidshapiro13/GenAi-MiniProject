from Calendar import Calendar
from AI import AI
from ai_prompts import DELETE_PROMPT, APPROVAL_PROMPT, YES_NO_PROMPT, CHANGE_PROMPT, CREATE_PROMPT, UPDATE_PROMPT, LIST_PROMPT, DELETE_STEP1_PROMPT
import ast

class Orchestrator():
    def __init__(self, agent):
        self.calendar = Calendar()
        self.agent = agent

    def run(self, action, context, query):
        event_list = self.calendar.get_events()
        context = context + " EVENTS: " + str(event_list)
        if action == 'create':
            output = self.get_info(CREATE_PROMPT, context, query)
            return self.check_approval(output, self.create_function)
        elif action == 'update':
            output = self.get_info(UPDATE_PROMPT, context, query)
            return self.check_approval(output, self.calendar.update_event)
        elif action == 'delete':
            output = self.get_info(DELETE_PROMPT, context, query)
            return self.check_approval(output, self.delete_function)
        elif action == 'list':
            output = self.get_info(LIST_PROMPT, context, query)
            return self.calendar.get_events()
        else:
            return "ACTION NOT FOUND"
        
    def check_approval(self, json, alteration_function):
        approval_question = self.agent.run(APPROVAL_PROMPT, json, self.agent.memory_session)
        print("Bot: ", approval_question)
        response = input("You: ")
        decision = self.agent.run(YES_NO_PROMPT, response, "General")
        if decision == "yes":
            if type(json) == str:
                json = ast.literal_eval(json)
            return alteration_function(json['params'])
        elif decision == "change":
            update = self.agent.run(CHANGE_PROMPT, str(json) + " " + response, self.agent.memory_session)
            return self.check_approval(update, alteration_function)
        else:
            print("Bot: No problem. I'll leave the calendar as is.")
            return "No change to event"
    
    def delete_function(self, json):
        event_list = self.calendar.get_events()
        event_list.append(json['keywords'])
        json = self.agent.run(DELETE_PROMPT, event_list, "General")
        if type(json) == str:
            json = ast.literal_eval(json)
        return self.calendar.delete_event(json['params'])
    
    def create_function(self, json):
        result = ""
        for item in json:
            result += self.calendar.create_event(item)
        return "successfully added!" + result
    
    def get_info(self, prompt, context, query):
        output = self.agent.run(prompt + " " + context, query, session=self.agent.memory_session)
        while output.startswith("RESPONSE:"):
            print("Bot: ", output[10:])
            context = context + query
            query = input("You: ")
            output = self.agent.run(prompt + " " + context, query, session=self.agent.memory_session)
        output = ast.literal_eval(output)
        return output