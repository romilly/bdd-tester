from abc import ABCMeta, abstractmethod

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


class FilteringHandler(CommandHandler):
    def handle_command(self, event):
        remove = event.id != self._harness.id
        if remove:
            self.monitor.debug('filter filtering out %s' % str(event))
        else:
            self.monitor.debug('filter passing on %s'  % str(event))
        return remove


class Terminator(CommandHandler):
    def handle_command(self, event):
        if event.e_type == 'END':
            self._harness.end()
            return True
        else:
            return False


class ButtonHandler(CommandHandler):
    def handle_command(self, event):
        self.monitor.debug('checking button event')
        if event.e_type in [BUTTON_A, BUTTON_B]:
            self._harness.button_event(event)
            return True
        return False

