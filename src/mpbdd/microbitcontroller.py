import threading

from time import sleep

from mpbdd.helpers import event_message, DEFAULT_NAME
from mpbdd.microbit_port import MicrobitPort, RadioPort
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
        self.radio_port = RadioPort(self.monitor)

    def run(self, *targets):
        self.monitor.info('starting')
        self.port.open(targets)
        self.radio_thread = threading.Thread(target=self.radio_port.run, args=[len(targets)], daemon=True)
        self.radio_thread.start()

    def close(self):
        self._publish_command('END', '*')
        self.port.close()
        self.radio_port.running = False
        self.monitor.info('finished')

    def press(self, button, target=DEFAULT_NAME, duration_ms=200):
        self._publish_command(button, DOWN, target)
        sleep(duration_ms/1000.0)
        self._publish_command(button, UP, target)

    def _publish_command(self, command, value='', target=DEFAULT_NAME):
        self.port.publish(event_message(command, value, target))

    def read_event(self):
        return self.port.read_event()

