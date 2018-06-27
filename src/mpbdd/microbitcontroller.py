from threading import Event

import threading

from time import sleep

from mpbdd.helpers import event_message, DEFAULT_NAME
from mpbdd.microbit_port import MicrobitPort, ControllerRadioPort
from mpbdd.monitors import LoggingMonitor

DOWN = 'down'
UP = 'up'
BUTTON_A = 'button_a'
BUTTON_B = 'button_b'


class RadioController():
    def __init__(self, monitor):
        self.monitor = monitor
        self.radio_port = None
        self.running = True

    def run(self, count, sync_event):
        self.radio_port = ControllerRadioPort(self.monitor)
        self.radio_port.sync(count)
        sync_event.set()
        while self.running:
            # self.monitor.debug('checking for radio to resend')
            if self.poll(10):
                # self.monitor.debug('incoming radio message' )
                incoming = self.radio_recv()
                self.monitor.debug('incoming radio message %s' % incoming)
                self.sync_send('')
                self.publish(incoming)
        self.monitor.debug('closing radio port')
        self.radio_port.close()

    def poll(self, timeout):
        return self.radio_port.poll(timeout)

    def radio_recv(self):
        return self.radio_port.sync_recv()

    def sync_send(self, message):
        self.radio_port.sync_send(message)

    def publish(self, message):
        self.radio_port.publish(message)

    def close(self):
        self.running = False


class MicrobitController():
    def __init__(self):
        self.id = 'Controller'
        self.monitor = LoggingMonitor(self, 'logs/testing.log')
        self.port = MicrobitPort(self.monitor)
        self.radio_controller = RadioController(self.monitor)

    def run(self, *targets):
        self.monitor.info('starting')
        self.port.open(targets)
        sync_event = Event()
        self.radio_thread = threading.Thread(target=self.radio_controller.run, args=[len(targets), sync_event], daemon=True)
        self.radio_thread.start()
        sync_event.wait()

    def close(self):
        self._publish_command('END', '*')
        self.radio_controller.close()
        self.radio_thread.join()
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

    def set_digital_input(self, number, state=1, target=DEFAULT_NAME):
        self._publish_command(number, state, target)

