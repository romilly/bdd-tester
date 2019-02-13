import sys

from hamcrest import contains_string, all_of
from time import sleep
from controller_test import AbstractControllerTest
#from documenter import AbstractControllerTest
from helpers import see
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import BUTTON_A, BUTTON_B

QUIZ_RUNNER = 'QuizRunner'
TEAM1 = 'Team 1'
TEAM2 = 'Team 2'


BUTTON_C = 8
BUTTON_D = 16

sys.path += '/home/romilly/git/active/bdd-tester/src'


class QuizRunner(AbstractControllerTest):
    def setUp(self):
        AbstractControllerTest.setUp(self)

    def test_forced_game_end(self):
        self.start_quiz()
        self.expect(see(QUIZ_RUNNER, 'Play time!'))
        ## play a round
        self.expect(
            see(QUIZ_RUNNER, 'round 1'),
            see(TEAM1, 'round 1'),
            see(TEAM2, 'round 1'))
        self.press(TEAM2, BUTTON_A)
        self.press(QUIZ_RUNNER, BUTTON_B)
        self.expect(
            see(QUIZ_RUNNER, 'team 2 buzzing'),
            see(TEAM2, 'team 2 buzzing'))
        self.press_extra(QUIZ_RUNNER, BUTTON_D)
        self.expect(
            see(QUIZ_RUNNER, 'game over'),
            see(QUIZ_RUNNER, all_of(contains_string("that's all"),
                                    contains_string('1:0'),
                                    contains_string('2:0'))))
        sleep(1.0)  # wait for cool-down

    def start_quiz(self):
        self.run_scripts(Target(QUIZ_RUNNER, '/home/romilly/git/active/bbc-microbit-nsp/src/quizrunner/quizrunner.py'),
                         Target(TEAM1, '/home/romilly/git/active/bbc-microbit-nsp/src/quizrunner/quizrunner.py'),
                         Target(TEAM2, '/home/romilly/git/active/bbc-microbit-nsp/src/quizrunner/quizrunner.py'))
        self.press(QUIZ_RUNNER, BUTTON_A)
        self.expect(see(QUIZ_RUNNER, 'runner'))
        self.expect(see(TEAM1, 'checking in'),
                    see(TEAM2, 'checking in'))
        self.press(TEAM1, BUTTON_B)
        self.expect(see(TEAM1, 'check'))
        self.expect(see(QUIZ_RUNNER, 'team 1 checked in'))
        self.expect(see(TEAM1, 'team: 1'))
        sleep(0.1)  # otherwise team 2 might get team 1's message after the button press!
        self.press(TEAM2, BUTTON_B)
        self.expect(see(TEAM2, 'check'))
        self.expect(see(QUIZ_RUNNER, 'team 2 checked in'))
        self.press(QUIZ_RUNNER, BUTTON_B)
        self.expect(see(TEAM2, 'team: 2'),
                    see(QUIZ_RUNNER, 'all checked in'))
        sleep(0.1)  # as there will be more radio messages to process

    def test_button_and_display(self):
        self.start_quiz()
        self.expect(see(QUIZ_RUNNER, 'Play time!'))
        ## play a round
        self.expect(
            see(QUIZ_RUNNER, 'round 1'),
            see(TEAM1, 'round 1'),
            see(TEAM2, 'round 1'))
        self.press(TEAM1, BUTTON_A)
        self.expect(
            see(QUIZ_RUNNER, 'team 1 buzzing'),
            see(TEAM1, 'team 1 buzzing'))
        self.press(QUIZ_RUNNER, BUTTON_B)
        self.press(TEAM2, BUTTON_A)
        self.expect(
            see(QUIZ_RUNNER, 'team 2 buzzing'),
            see(TEAM2, 'team 2 buzzing'))
        self.press(QUIZ_RUNNER, BUTTON_A)
        self.expect(
            see(QUIZ_RUNNER, 'round over'),
            see(TEAM1, 'round over'),
            see(TEAM2, 'round over'))
        # play another round
        self.expect(
            see(QUIZ_RUNNER, 'round 2'),
            see(TEAM1, 'round 2'),
            see(TEAM2, 'round 2'))
        self.press(TEAM2, BUTTON_A)
        self.expect(
            see(QUIZ_RUNNER, 'team 2 buzzing'),
            see(TEAM2, 'team 2 buzzing'))
        self.press(QUIZ_RUNNER, BUTTON_B)
        self.press(TEAM1, BUTTON_A)
        self.expect(
            see(QUIZ_RUNNER, 'team 1 buzzing'),
            see(TEAM1, 'team 1 buzzing'))
        self.press(QUIZ_RUNNER, BUTTON_B)
        self.press_extra(QUIZ_RUNNER, BUTTON_C)
        self.expect(
            see(QUIZ_RUNNER, 'round over'),
            see(TEAM1, 'round over'),
            see(TEAM2, 'round over'))
        sleep(1.0) # allow radio stuff  to clear
        self.expect(
            see(QUIZ_RUNNER, 'round 3'),
            see(TEAM1, 'round 3'),
            see(TEAM2, 'round 3'))
        self.press_extra(QUIZ_RUNNER, BUTTON_D)
        self.expect(
            see(QUIZ_RUNNER, 'game over'),
            see(QUIZ_RUNNER, all_of(contains_string("that's all"),
                                    contains_string('1:0'),
                                    contains_string('2:1'))))
        sleep(1.0) # wait for cool-down

    def tearDown(self):
        AbstractControllerTest.tearDown(self)



