import sys
from unittest import TestCase
from hamcrest import assert_that

from helpers import is_display
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import MicrobitController, BUTTON_A, BUTTON_B

sys.path += '/home/romilly/git/active/bdd-tester/src'


class ControllerTest(TestCase):
    def setUp(self):
        self.controller = MicrobitController()

    def test_button_and_display(self):
        self.controller.run(Target('tests/e2e/button_print.py','microbit 1'),Target('tests/e2e/button_print.py','microbit 2'))
        self.controller.press('microbit 1', BUTTON_A)
        event = self.controller.read_event()
        assert_that(event, is_display('microbit 1','Ouch!'))
        self.controller.press('microbit 2', BUTTON_A)
        event = self.controller.read_event()
        assert_that(event, is_display('microbit 2', 'Ouch!'))
        self.controller.press('microbit 1', BUTTON_B)
        event = self.controller.read_event()
        assert_that(event, is_display('microbit 1','That hurt!'))

    def test_digital_inputs(self):
        self.controller.run(Target('tests/e2e/digital_read.py'))
        print('controller has started microbit')
        self.controller.set_digital_input(8, 'microbit 1')
        event = self.controller.read_event()
        assert_that(event, is_display('microbit 1','Ouch!'))
        self.controller.set_digital_input(8, 0, 'microbit 1')
        self.controller.set_digital_input(16, 'microbit 1')
        event = self.controller.read_event()
        assert_that(event, is_display('microbit 1','That hurt!'))

    def tearDown(self):
        self.controller.close()