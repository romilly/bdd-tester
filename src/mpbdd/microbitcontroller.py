from time import sleep

from mpbdd.helpers import event_message, DEFAULT_NAME
from mpbdd.microbit_port import MicrobitPort
from mpbdd.monitors import LoggingMonitor

DOWN = 'down'
UP = 'up'
BUTTON_A = 'button_a'
BUTTON_B = 'button_b'

class MicrobitController():
    def __init__(self):
        self.id = 'Controller'
        self.monitor = LoggingMonitor(self, '../../logs/testing.log')
        self.port = MicrobitPort(self.monitor)

    def run(self, *targets):
        self.monitor.info('starting')
        self.port.open(targets)

    def close(self):
        self._publish_command('END', '*')
        self.port.close()
        self.monitor.info('finished')

    def press(self, button, target=DEFAULT_NAME, duration_ms=200):
        self._publish_command(button, DOWN, target)
        sleep(duration_ms/1000.0)
        self._publish_command(button, UP, target)

    def _publish_command(self, command, value='', target=DEFAULT_NAME):
        self.port.publish(event_message(command, value, target))

    def read_event(self):
        return self.port.read_event()

