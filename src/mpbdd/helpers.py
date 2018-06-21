import json
from collections import namedtuple

DEFAULT_NAME = 'microbit 1'

Event = namedtuple('Event',['e_type','message', 'id'])

def event(incoming):
    return Event(*json.loads(incoming))


def event_message(e_type, message, id):
    return json.dumps(Event(e_type, message, id))


class Target():
    def __init__(self, script, id=DEFAULT_NAME):
        self.script = script
        self.id = id

