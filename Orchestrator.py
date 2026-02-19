from Calendar import Calendar
from AI import AI
import ast

class Orchestrator():
    def __init__(self):
        self.calendar = Calendar()
        self.agent = AI()

    def run(self, json):
        delete_prompt = ""
        with open('deletePrompt.txt', 'r') as file:
            delete_prompt = file.read()

        if json['action'] == 'create':
            return self.calendar.create_event(json['params'])
        elif json['action'] == 'update':
            return self.calendar.update_event(json['params'])
        elif json['action'] == 'delete':
            event_list = self.calendar.get_events()
            event_list.append(json['keywords'])

            json = self.agent.run(delete_prompt, event_list)
            json = ast.literal_eval(json)
            return self.calendar.delete_event(json['params'])
        elif json['action'] == 'list':
            return self.calendar.get_events()
        else:
            return "ACTION NOT FOUND"