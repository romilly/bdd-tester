import sys
from unittest import TestCase
from hamcrest import assert_that

from helpers import see
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import MicrobitController, BUTTON_A, BUTTON_B

sys.path += '/home/romilly/git/active/bdd-tester/src'


class ControllerTest(TestCase):
    def setUp(self):
        self.controller = MicrobitController()

    def test_button_and_display(self):
        self.controller.run(Target('microbit 1', 'tests/e2e/button_print.py'),
                            Target('microbit 2', 'tests/e2e/button_print.py'))
        self.controller.press('microbit 1', BUTTON_A)
        event = self.controller.read_event()
        assert_that(event, see('microbit 1', 'Ouch!'))
        self.controller.press('microbit 2', BUTTON_A)
        event = self.controller.read_event()
        assert_that(event, see('microbit 2', 'Ouch!'))
        self.controller.press('microbit 1', BUTTON_B)
        event = self.controller.read_event()
        assert_that(event, see('microbit 1', 'That hurt!'))

    def test_digital_inputs(self):
        self.controller.run(Target('microbit 1', 'tests/e2e/digital_read.py'))
        self.controller.set_digital_input('microbit 1', 8)
        event = self.controller.read_event()
        assert_that(event, see('microbit 1', 'Ouch!'))
        self.controller.set_digital_input('microbit 1', 8, 0)
        self.controller.set_digital_input('microbit 1', 16)
        event = self.controller.read_event()
        assert_that(event, see('microbit 1', 'That hurt!'))

    def tearDown(self):
        self.controller.close()