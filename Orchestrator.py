from Calendar import Calendar

class Orchestrator():
    def __init__(self):
        self.calendar = Calendar()

    def run(self, json):
        if json['action'] == 'create':
            return self.calendar.create_event(json['params'])
        elif json['action'] == 'update':
            return self.calendar.update_event(json['params'])
        elif json['action'] == 'delete':
            event_list = self.calendar.get_events(json['params'])
            return self.calendar.delete_event(json['params'])
        elif json['action'] == 'list':
            return self.calendar.get_events(json['params'])
        else:
            return "ACTION NOT FOUND"