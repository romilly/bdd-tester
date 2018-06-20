from time import sleep

from mpbdd.helpers import event, event_message, DEFAULT_NAME
from mpbdd.microbit_port import MicrobitPort
import logging

DOWN = 'down'
UP = 'up'
BUTTON_A = 'button_a'
BUTTON_B = 'button_b'

class MicrobitController():
    def __init__(self, log_level=logging.DEBUG):
        logging.basicConfig(filename='../../logs/testing.log', level=log_level,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.port = MicrobitPort()

    def run(self, *targets):
        logging.info('Starting test run')
        self.port.open(targets)

    def close(self):
        self._publish_command('END', '*')
        self.port.close()

    def press(self, button, target=DEFAULT_NAME, duration_ms=50):
        self._publish_command(button, DOWN, target)
        sleep(duration_ms/1000.0)
        self._publish_command(button, UP, target)

    def _publish_command(self, command, value='', target=DEFAULT_NAME):
        self.port.publish(event_message(command, value, target))

    def read_event(self):
        return self.port.read_event()

