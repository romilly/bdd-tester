import sys

from controller_test import AbstractControllerTest
from helpers import see
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import BUTTON_A

MB1 = 'Microbit 1'
MB2 = 'Microbit 2'
MB3 = 'Microbit 3'


sys.path += '/home/romilly/git/active/bdd-tester/src'


class QuizTest(AbstractControllerTest):
    def setUp(self):
        super(QuizTest,self).setUp()

    def tearDown(self):
        super(QuizTest,self).tearDown()

    def test_button_a_displays_a_message(self):
        self.run_scripts(Target(MB1, 'tests/e2e/flippers/mb.py'),
                            Target(MB2, 'tests/e2e/flippers/mb.py'),
                            Target(MB3, 'tests/e2e/flippers/mb.py'))
        self.press(MB1, BUTTON_A)
        self.expect(see(MB1, 'That hurt!'),
                    see(MB2, 'Poor you!'),
                    see(MB3, 'Poor you!')
                    )