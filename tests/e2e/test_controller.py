import sys
from unittest import TestCase
from hamcrest import assert_that

from helpers import is_event
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import MicrobitController, BUTTON_A

sys.path += '/home/romilly/git/active/bdd-tester/src'


class ControllerTest(TestCase):
    def setUp(self):
        self.controller = MicrobitController()

    def test_button_and_display(self):
        self.controller.run(Target('tests/e2e/button_print.py'))
        self.controller.press(BUTTON_A)
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'Ouch!'))
        self.controller.close()