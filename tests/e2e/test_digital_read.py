import sys
from unittest import TestCase
from hamcrest import assert_that

from helpers import is_event
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import MicrobitController, BUTTON_A, BUTTON_B

sys.path += '/home/romilly/git/active/bdd-tester/src'


class ControllerTest(TestCase):
    def setUp(self):
        self.controller = MicrobitController()

    def test_digital_inputs(self):
        self.controller.run(Target('tests/e2e/digital_read.py'))
        print('controller has started microbit')
        self.controller.set_digital_input(8)
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'Ouch!'))
        self.controller.set_digital_input(8, 0)
        self.controller.set_digital_input(16)
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'That hurt!'))

    def tearDown(self):
        self.controller.close()