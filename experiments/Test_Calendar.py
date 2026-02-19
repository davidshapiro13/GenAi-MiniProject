from Calendar import Calendar

calendar = Calendar()

def test_create():
    #Test JSON
    json = {
        'summary': "Homework",
        'location': "126 Pwoderhouse Blvd, Somerville MA",
        'description': "The grind",
        'start': {
            'dateTime': '2026-05-28T09:00:00-07:00' ,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': '2026-05-29T09:00:00-07:00',
            'timeZone': 'America/New_York',
            },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
    }
    calendar.create_event(json)

def test_list():
    json = {
        'start_date': '2015-05-28T09:00:00-07:00',
        'num_results': 10,
    }
    events = calendar.get_events(json)
    reduced_events = []
    for event in events:
        reduced_json = {
            'summary': event['summary'],
            'event_id': event['id'],
            'description': event['description'],
            'location': event['location'],
            'start': {
                'dateTime': event['start']['dateTime'] ,
                'timeZone': event['start']['timeZone'],
            },
            'end': {
                'dateTime': event['end']['dateTime'],
                'timeZone': event['end']['timeZone'],
                },
        }
        reduced_events.append(reduced_json)
    for e in reduced_events:
        print(e['event_id'])
    return reduced_events

def test_delete():
    json = {
        'event_id': '6taf675t2a5ngf9juinnuv9bko_20260529T160000Z'
    }
    calendar.delete_event(json)

def test_update():
    json = {
        'event_id': '6taf675t2a5ngf9juinnuv9bko_20260529T160000Z',
        'body': { 'summary': "DAVID TEST" }
    }
    calendar.update_event(json)

test_update()

