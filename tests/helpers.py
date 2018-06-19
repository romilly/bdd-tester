from hamcrest.core.base_matcher import BaseMatcher

from mptdd.helpers import Event


class EventMatcher(BaseMatcher):
    def describe_to(self, description):
        description.append('an event from %i of type %s with value %s' % (self.id, self.e_type, self.value))

    def __init__(self, id, e_type, value):
        self.id = id
        self.e_type = e_type
        self.value = value

    def _matches(self, item):
        if not isinstance(item, Event):
            return False
        return item.id == self.id and item.e_type == self.e_type and item.value == self.value


def is_event(id, e_type, value):
    return EventMatcher(id, e_type, value)