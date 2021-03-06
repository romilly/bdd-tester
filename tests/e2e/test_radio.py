import sys
from unittest import TestCase

from hamcrest import assert_that, none, not_none

from controller_test import AbstractControllerTest
from helpers import is_event, see
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import MicrobitController, BUTTON_A

# You won't need the line below once the framework is in PiPi
# For now, adjust it to refer to the location of the cloned code on your computer
sys.path += '/home/romilly/git/active/bdd-tester/src'


class RadioTest(AbstractControllerTest):
    def setUp(self):
        super(RadioTest,self).setUp()

    def tearDown(self):
        super(RadioTest,self).tearDown()

    def test_button_and_display(self):
        # adjust these to reflect the relative or absolute path to the script to run on the microbit
        self.run_scripts(Target('microbit 1', 'tests/e2e/button_radio.py'),
                            Target('microbit 2', 'tests/e2e/button_radio.py'))
        self.press('microbit 1', BUTTON_A)
        self.expect(see('microbit 2', 'signal received!'))

    def test_filter_own_own_transmissions(self):
        self.controller.run(Target('microbit 1', 'tests/e2e/button_radio.py'),
                            Target('microbit 2', 'tests/e2e/button_radio.py'))
        self.controller.press('microbit 1', BUTTON_A)
        event = self.controller.read_event() # checked in test above
        assert_that(event, not_none())
        event = self.controller.read_event() # should be no other event
        assert_that(event, none())
