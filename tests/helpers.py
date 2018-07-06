from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from mpbdd.helpers import Event, DEFAULT_NAME


class EventMatcher(BaseMatcher):
    def describe_to(self, description):
        description.append('an event from %s of type %s with message %s' % (self.id, self.e_type, self.message))

    def __init__(self, e_type, message, id):
        self.e_type = wrap_matcher(e_type)
        self.message = wrap_matcher(message)
        self.id = wrap_matcher(id)

    def _matches(self, item):
        if not isinstance(item, Event):
            return False
        return (self.id.matches(item.id) and
                self.e_type.matches(item.e_type) and
                self.message.matches(item.message))


# TODO: get rid of default name
def is_event(e_type, message='', id=DEFAULT_NAME):
    return EventMatcher(e_type, message, id)

def see(microbit, message):
    return is_event('display', message, microbit)
