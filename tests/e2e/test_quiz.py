import sys
import time

from time import sleep
from unittest import TestCase
from hamcrest import assert_that

from helpers import is_event, see
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import MicrobitController, BUTTON_A, BUTTON_B

QUIZ_RUNNER = 'QuizRunner'
TEAM1 = 'Team 1'
TEAM2 = 'Team 2'

sys.path += '/home/romilly/git/active/bdd-tester/src'


class ControllerTest(TestCase):
    def setUp(self):
        self.controller = MicrobitController()

    def test_button_and_display(self):
        self.controller.run(Target('tests/e2e/quizmaster.py', QUIZ_RUNNER)
                            , Target('tests/e2e/quizmaster.py', TEAM1)
                            , Target('tests/e2e/quizmaster.py', TEAM2))
        self.controller.press(QUIZ_RUNNER, BUTTON_A)
        self.check_display(QUIZ_RUNNER, 'runner')
        self.expect_events(see(TEAM1, 'checking in'), see(TEAM2, 'checking in'))
        self.controller.press(TEAM1, BUTTON_B)
        self.check_display(TEAM1, 'check')
        self.check_display(QUIZ_RUNNER, 'team 1 checked in')
        self.check_display(TEAM1, 'team: 1')
        sleep(0.1) # otherwise team 2 might get team 1's message after the button press!

        self.controller.press(TEAM2, BUTTON_B)
        self.check_display(TEAM2, 'check')
        self.check_display(QUIZ_RUNNER, 'team 2 checked in')
        self.controller.press(QUIZ_RUNNER, BUTTON_B)
        self.expect_events(see(TEAM2, 'team: 2'), see(QUIZ_RUNNER, 'all checked in'))
        sleep(1.0) # as there will be more radio messages to process
        self.check_display(QUIZ_RUNNER, 'Play time!')
        ## play a round
        self.expect_events(
            see(QUIZ_RUNNER, 'round 1'),
            see(TEAM1, 'round 1'),
            see(TEAM2, 'round 1'))
        self.controller.press(TEAM1, BUTTON_A)
        self.expect_events(
            see(QUIZ_RUNNER, 'team 1 buzzing'),
            see(TEAM1, 'team 1 buzzing'))
        self.controller.press(QUIZ_RUNNER, BUTTON_B)
        self.controller.press(TEAM2, BUTTON_A)
        self.expect_events(
            see(QUIZ_RUNNER, 'team 2 buzzing'),
            see(TEAM2, 'team 2 buzzing'))
        self.controller.press(QUIZ_RUNNER, BUTTON_A)
        self.expect_events(
            see(QUIZ_RUNNER, 'round over'),
            see(TEAM1, 'round over'),
            see(TEAM2, 'round over'))
        # play another round
        self.expect_events(
            see(QUIZ_RUNNER, 'round 2'),
            see(TEAM1, 'round 2'),
            see(TEAM2, 'round 2'))
        self.controller.press(TEAM2, BUTTON_A)
        self.expect_events(
            see(QUIZ_RUNNER, 'team 2 buzzing'),
            see(TEAM2, 'team 2 buzzing'))





    def check_display(self, microbit, message):
        event = self.controller.read_event()
        assert_that(event, see(microbit, message))

    def tearDown(self):
        self.controller.close()

    def expect_events(self, *event_matchers, timeout_ms=100):
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

    def event_is_ok(self, event_set, next_event):
        for possible in event_set:
            if possible.matches(next_event):
                event_set.remove(possible)
                return True
        return False
