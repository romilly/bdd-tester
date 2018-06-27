import sys
import time

from time import sleep
from unittest import TestCase
from hamcrest import assert_that

from helpers import is_event
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import MicrobitController, BUTTON_A, BUTTON_B

sys.path += '/home/romilly/git/active/bdd-tester/src'


class ControllerTest(TestCase):
    def setUp(self):
        self.controller = MicrobitController()

    def test_button_and_display(self):
        self.controller.run(Target('tests/e2e/quizmaster.py', 'QuizRunner')
                            ,Target('tests/e2e/quizmaster.py','Team 1')
                            ,Target('tests/e2e/quizmaster.py','Team 2'))
        self.controller.press(BUTTON_A, 'QuizRunner')
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'runner','QuizRunner'))
        self.expect_events(is_event('display', 'checking in','Team 1'),is_event('display', 'checking in','Team 2'))
        self.controller.press(BUTTON_B,'Team 1')
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'check','Team 1'))
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'team 1 checked in','QuizRunner'))
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'team: 1','Team 1'))
        sleep(0.1) # otherwise team 2 might get team 1's message after the button press!
        self.controller.press(BUTTON_B,'Team 2')
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'check','Team 2'))
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'team 2 checked in','QuizRunner'))
        self.controller.press(BUTTON_B,'QuizRunner')
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'all checked in','QuizRunner'))
        sleep(1.0) # as there will be more radio messages to process




    def tearDown(self):
        self.controller.close()

    def expect_events(self, *event_matchers, timeout_ms=100):
        start = time.perf_counter()
        event_set = set(event_matchers)
        while len(event_set):
            if time.perf_counter() - start > 1000.0 * timeout_ms:
                raise TimeoutError()
            next_event = self.controller.read_event()
            if next_event:
                if self.event_is_ok(event_set, next_event):
                    continue
                self.fail('unexpected event %s' % str(next_event))

    def event_is_ok(self, event_set, next_event):
        for possible in event_set:
            if possible.matches(next_event):
                event_set.remove(possible)
                return True
        return False
