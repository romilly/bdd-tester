from unittest import TestCase

from hamcrest import assert_that

from helpers import is_event
from mpbdd.handlers import Terminator, FilteringHandler, MissingHandlerException, ButtonHandler
from mpbdd.helpers import Event
from mpbdd.microbitcontroller import BUTTON_A, DOWN
from mpbdd.monitors import Monitor

DONT_CARE = 'xxx'


class MockHarness():
    def __init__(self, id='one'):
        self.monitor = Monitor()
        self.terminated = False
        self.event = None
        self.id = id

    def end(self):
        self.terminated = True

    def button_event(self, event):
        self.event = event


class HandlerTest(TestCase):
    def setUp(self):
        self.harness = MockHarness()

    def test_terminator_ends_session(self):
        handler = Terminator(self.harness)
        handler.command(Event('END', DONT_CARE, DONT_CARE))
        self.assertTrue(self.harness.terminated)

    def test_filter_tries_to_pass_on_relevant_events(self):
        handler = FilteringHandler(self.harness)
        self.assertFalse(handler.command(Event(DONT_CARE, DONT_CARE, 'one')))

    def test_filter_handles_irrelevant_events(self):
        handler = FilteringHandler(self.harness)
        self.assertTrue(handler.command(Event(DONT_CARE, DONT_CARE, 'not one')))

    def test_button_handler_handles_button_events(self):
        handler = ButtonHandler(self.harness)
        handler.command(Event(BUTTON_A, DOWN, DONT_CARE))
        assert_that(self.harness.event, is_event(DONT_CARE, BUTTON_A, DOWN))

    def test_handlers_chain_correctly(self):
        handler = Terminator(self.harness, FilteringHandler(self.harness, ButtonHandler(self.harness)))
        handler.command(Event('END', DONT_CARE, DONT_CARE))
        self.assertTrue(self.harness.terminated)
        self.assertTrue(handler.command(Event(DONT_CARE, DONT_CARE, 'not one')))
        handler.command(Event(BUTTON_A, DOWN, 'one'))
        assert_that(self.harness.event, is_event('one', BUTTON_A, DOWN))



