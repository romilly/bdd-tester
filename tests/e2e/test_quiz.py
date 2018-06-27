import sys
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
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'checking in','Team 1'))
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'checking in','Team 2'))
        sleep(0.1)
        self.controller.press(BUTTON_B,'Team 1')
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'check','Team 1'))
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'team 1 checked in','QuizRunner'))





    def tearDown(self):
        self.controller.close()