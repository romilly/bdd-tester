import sys
from unittest import TestCase

from hamcrest import assert_that

from helpers import is_event
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import MicrobitController, BUTTON_A

# You won't need the line below once the framework is in PiPi
# For now, adjust it to refer to the location of the cloned code on your computer
sys.path += '/home/romilly/git/active/bdd-tester/src'


class ControllerTest(TestCase):
    def setUp(self):
        self.controller = MicrobitController()

    def test_button_and_display(self):
        # adjust these to reflect the relative or absolute path to the script to run on the microbit
        self.controller.run(Target('tests/e2e/button_radio.py'),Target('tests/e2e/button_radio.py','microbit 2'))
        self.controller.press(BUTTON_A)
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'signal received!', 'microbit 2'))

    def tearDown(self):
        self.controller.close()