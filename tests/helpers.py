from hamcrest.core.base_matcher import BaseMatcher

from mptdd.helpers import Event, DEFAULT_NAME


class EventMatcher(BaseMatcher):
    def describe_to(self, description):
        description.append('an event from %s of type %s with message %s' % (self.id, self.e_type, self.message))

    def __init__(self, e_type, message, id):
        self.e_type = e_type
        self.message = message
        self.id = id

    def _matches(self, item):
        if not isinstance(item, Event):
            return False
        return item.id == self.id and item.e_type == self.e_type and item.message == self.message


def is_event(e_type, message='', id=DEFAULT_NAME):
    return EventMatcher(e_type, message, id)