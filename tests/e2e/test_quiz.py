import sys

from time import sleep

from controller_test import AbstractControllerTest
from helpers import see
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import MicrobitController, BUTTON_A, BUTTON_B

QUIZ_RUNNER = 'QuizRunner'
TEAM1 = 'Team 1'
TEAM2 = 'Team 2'


BUTTON_C = 8
BUTTON_D = 16

sys.path += '/home/romilly/git/active/bdd-tester/src'


class QuizTest(AbstractControllerTest):
    def test_button_and_display(self):
        self.controller.run(Target(QUIZ_RUNNER, 'tests/e2e/quizmaster.py'),
                            Target(TEAM1, 'tests/e2e/quizmaster.py'),
                            Target(TEAM2, 'tests/e2e/quizmaster.py'))
        self.controller.press(QUIZ_RUNNER, BUTTON_A)
        self.expect(see(QUIZ_RUNNER, 'runner'))
        self.expect(see(TEAM1, 'checking in'),
                    see(TEAM2, 'checking in'))
        self.controller.press(TEAM1, BUTTON_B)
        self.expect(see(TEAM1, 'check'))
        self.expect(see(QUIZ_RUNNER, 'team 1 checked in'))
        self.expect(see(TEAM1, 'team: 1'))
        sleep(0.1) # otherwise team 2 might get team 1's message after the button press!
        self.controller.press(TEAM2, BUTTON_B)
        self.expect(see(TEAM2, 'check'))
        self.expect(see(QUIZ_RUNNER, 'team 2 checked in'))
        self.controller.press(QUIZ_RUNNER, BUTTON_B)
        self.expect(see(TEAM2, 'team: 2'),
                    see(QUIZ_RUNNER, 'all checked in'))
        sleep(0.1) # as there will be more radio messages to process
        self.expect(see(QUIZ_RUNNER, 'Play time!'))
        ## play a round
        self.expect(
            see(QUIZ_RUNNER, 'round 1'),
            see(TEAM1, 'round 1'),
            see(TEAM2, 'round 1'))
        self.controller.press(TEAM1, BUTTON_A)
        self.expect(
            see(QUIZ_RUNNER, 'team 1 buzzing'),
            see(TEAM1, 'team 1 buzzing'))
        self.controller.press(QUIZ_RUNNER, BUTTON_B)
        self.controller.press(TEAM2, BUTTON_A)
        self.expect(
            see(QUIZ_RUNNER, 'team 2 buzzing'),
            see(TEAM2, 'team 2 buzzing'))
        self.controller.press(QUIZ_RUNNER, BUTTON_A)
        self.expect(
            see(QUIZ_RUNNER, 'round over'),
            see(TEAM1, 'round over'),
            see(TEAM2, 'round over'))
        # play another round
        self.expect(
            see(QUIZ_RUNNER, 'round 2'),
            see(TEAM1, 'round 2'),
            see(TEAM2, 'round 2'))
        self.controller.press(TEAM2, BUTTON_A)
        self.expect(
            see(QUIZ_RUNNER, 'team 2 buzzing'),
            see(TEAM2, 'team 2 buzzing'))
        self.controller.press(QUIZ_RUNNER, BUTTON_B)
        self.controller.press(TEAM1, BUTTON_A)
        self.expect(
            see(QUIZ_RUNNER, 'team 1 buzzing'),
            see(TEAM1, 'team 1 buzzing'))
        self.controller.press(QUIZ_RUNNER, BUTTON_B)
        self.controller.press_extra(QUIZ_RUNNER, BUTTON_C)
        self.expect(
            see(QUIZ_RUNNER, 'round over'),
            see(TEAM1, 'round over'),
            see(TEAM2, 'round over'))
        sleep(1.0) # allow radio stuff  to clear


