import sys
from unittest import TestCase
from hamcrest import assert_that

from helpers import is_event
from mptdd.helpers import Target
from mptdd.microbitcontroller import MicrobitController

sys.path += '/home/romilly/git/active/bdd-tester/src'


class ControllerTest(TestCase):
    def setUp(self):
        self.controller = MicrobitController()

    def test_button_and_display(self):
        self.controller.run(Target('tests/e2e/button_print.py'))
        self.controller.publish_command('button_a')
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'Ouch!'))
        self.controller.close()