import sys
import time

from time import sleep
from unittest import TestCase
from hamcrest import assert_that

from helpers import is_event
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import MicrobitController, BUTTON_A, BUTTON_B

QUIZ_RUNNER = 'QuizRunner'

sys.path += '/home/romilly/git/active/bdd-tester/src'


def is_display(message, microbit):
    return is_event('display', message, microbit)


class ControllerTest(TestCase):
    def setUp(self):
        self.controller = MicrobitController()

    def test_button_and_display(self):
        self.controller.run(Target('tests/e2e/quizmaster.py', QUIZ_RUNNER)
                            ,Target('tests/e2e/quizmaster.py','Team 1')
                            ,Target('tests/e2e/quizmaster.py','Team 2'))
        self.controller.press(BUTTON_A, QUIZ_RUNNER)
        self.check_display(QUIZ_RUNNER, 'runner')
        self.expect_events(is_display('checking in', 'Team 1'), is_display('checking in', 'Team 2'))
        self.controller.press(BUTTON_B,'Team 1')
        self.check_display('Team 1', 'check')
        self.check_display(QUIZ_RUNNER, 'team 1 checked in')
        self.check_display('Team 1', 'team: 1')
        sleep(0.1) # otherwise team 2 might get team 1's message after the button press!

        self.controller.press(BUTTON_B,'Team 2')
        self.check_display('Team 2', 'check')
        self.check_display(QUIZ_RUNNER, 'team 2 checked in')
        self.controller.press(BUTTON_B, QUIZ_RUNNER)
        self.expect_events(is_display('team: 2', 'Team 2'), is_display('all checked in', QUIZ_RUNNER))
        sleep(1.0) # as there will be more radio messages to process
        self.check_display(QUIZ_RUNNER, 'Play time!')
        ## play a round
        self.expect_events(
            is_display('round 1', QUIZ_RUNNER),
            is_display('round 1', 'Team 1'),
            is_display('round 1', 'Team 2'))
        self.controller.press(BUTTON_A, 'Team 1')
        self.expect_events(
            is_display('team 1 buzzing', QUIZ_RUNNER),
            is_display('team 1 buzzing', 'Team 1'))
        self.controller.press(BUTTON_B, QUIZ_RUNNER)
        self.controller.press(BUTTON_A, 'Team 2')
        self.expect_events(
            is_display('team 2 buzzing', QUIZ_RUNNER),
            is_display('team 2 buzzing', 'Team 2'))




    def check_display(self, microbit, message):
        event = self.controller.read_event()
        assert_that(event, is_display(message, microbit))

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
