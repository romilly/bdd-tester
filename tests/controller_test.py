import time
from unittest import TestCase

from mpbdd.microbitcontroller import MicrobitController


class AbstractControllerTest(TestCase):
    def setUp(self):
        self.controller = MicrobitController()

    def tearDown(self):
        self.controller.close()

    def expect(self, *event_matchers, timeout_ms=100):
        start = time.perf_counter()
        event_set = set(event_matchers)
        while len(event_set):
            if time.perf_counter() - start > timeout_ms / 1000.0:
                raise TimeoutError()
            next_event = self.controller.read_event()
            if next_event:
                if self.event_is_ok(event_set, next_event):
                    continue
                self.fail('unexpected event %s' % str(next_event))

    @classmethod
    def event_is_ok(self, event_set, next_event):
        for possible in event_set:
            if possible.matches(next_event):
                event_set.remove(possible)
                return True
        return False

    def run_scripts(self, *scripts):
        self.controller.run(*scripts)

    def press(self, button, target, duration_ms=100):
        self.controller.press(button, target, duration_ms)

    def press_extra(self, target, pin_number, duration_ms=100):
        self.controller.press_extra(target, pin_number, duration_ms)