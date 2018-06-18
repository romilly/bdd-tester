import sys
from unittest import TestCase

from mptdd.controller import Controller

sys.path += '/home/romilly/git/active/bdd-tester/src'

# TODO: rename to MicrobitController
class ControllerTest(TestCase):
    def setUp(self):
        self.controller = Controller()

    def test_button_and_display(self):
        self.controller.run('tests/e2e/button_print.py')
        self.controller.publish('button_a')
        self.controller.expect_display('Ouch!') # TODO: replace with hamcrest test
        self.controller.publish('END', '*')