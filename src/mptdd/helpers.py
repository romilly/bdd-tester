import json
from collections import namedtuple

Event = namedtuple('Event',['id','e_type','value'])


def event(incoming):
    return Event(*json.loads(incoming))


def event_message(id, e_type, message):
    return json.dumps(Event(id, e_type, message))


