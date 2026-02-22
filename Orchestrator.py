from Calendar import Calendar
from AI import AI
from ai_prompts import DELETE_PROMPT, APPROVAL_PROMPT, YES_NO_PROMPT, CALENDAR_PROMPT
import ast

class Orchestrator():
    def __init__(self, agent):
        self.calendar = Calendar()
        self.agent = agent

    def run(self, json):

        if json['action'] == 'create':
            return self.check_approval(json, self.calendar.create_event)
        elif json['action'] == 'update':
            return self.check_approval(json, self.calendar.update_event)
        elif json['action'] == 'delete':
            return self.check_approval(json, self.delete_function)
        elif json['action'] == 'list':
            return self.calendar.get_events()
        elif json['action'] == 'mass-create':
            return self.check_approval(json, self.calendar.mass_create_events)
        else:
            return "ACTION NOT FOUND"
        
    def check_approval(self, json, alteration_function):
        approval_question = self.agent.run(APPROVAL_PROMPT, json, self.agent.chat_session)
        response = input(approval_question)
        decision = self.agent.run(YES_NO_PROMPT, response, "General")
        if decision == "yes":
            if type(json) == str:
                json = ast.literal_eval(json)
            return alteration_function(json['params'])
        if decision == "change":
            update = self.agent.run(CALENDAR_PROMPT, str(json), self.agent.chat_session)
            return self.check_approval(update, alteration_function)
        else:
            print("No problem. I'll leave the calendar as is.")
            return "No change to event"
    
    def delete_function(self, json):
        event_list = self.calendar.get_events()
        event_list.append(json['keywords'])
        json = self.agent.run(DELETE_PROMPT, event_list, "General")
        if type(json) == str:
            json = ast.literal_eval(json)
        return self.calendar.delete_event(json['params'])