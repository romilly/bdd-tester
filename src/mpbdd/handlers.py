from abc import ABCMeta, abstractmethod

from mpbdd.helpers import describe_command
from mpbdd.microbitcontroller import BUTTON_A, BUTTON_B, DOWN


class MissingHandlerException(Exception):
    pass


class CommandHandler(metaclass=ABCMeta):
    def __init__(self, harness, successor= None):
        self._harness = harness
        self.monitor = self._harness.monitor
        self._successor = successor

    def command(self, event):
        if self.handle_command(event):
            return True
        if self._successor:
            return self._successor.command(event)
        return False

    @abstractmethod
    def handle_command(self, event):
        pass


class DigitalPinHandler(CommandHandler):
    def handle_command(self, event):
        # self.monitor.debug('checking for pin event %s' % str(event))
        if event.e_type in range(1,17):
            self._harness.read_digital_event(event)
            return True
        return False



class FilteringHandler(CommandHandler):
    def handle_command(self, event):
        remove = event.id != self._harness.id
        return remove


class LoggingHandler(CommandHandler):
    def handle_command(self, event):
        self.monitor.debug('got %s' % describe_command(event))
        return False


class Terminator(CommandHandler):
    def handle_command(self, event):
        if event.e_type == 'END':
            self._harness.end()
            return True
        else:
            return False


class ButtonHandler(CommandHandler):
    def handle_command(self, event):
        if event.e_type in [BUTTON_A, BUTTON_B]:
            self._harness.button_event(event)
            return True
        return False

