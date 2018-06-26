import sys
import threading

import zmq

from mpbdd.handlers import Terminator, FilteringHandler, ButtonHandler, MissingHandlerException, DigitalPinHandler
from mpbdd.harness_port import CommandPort, RadioPort
from mpbdd.helpers import event_message, event
from mpbdd.microbitcontroller import DOWN
from mpbdd.monitors import LoggingMonitor


class Harness():
    def __init__(self, monitor=None):
        self.id = ''
        if not monitor:
            monitor = LoggingMonitor(self, 'logs/testing.log')
        self.monitor = monitor
        self.port = CommandPort(monitor)
        self.port.open(5561, 5562)
        self.id = self.port.id
        self.radio_port = RadioPort(monitor)
        # TODO: code smell!
        self.radio_port.id = self.id
        radio_thread = threading.Thread(target=self.radio_port.run, daemon=True)
        radio_thread.start()
        self._callbacks = {}
        self.monitor.info('Harness created')
        self.handler_chain = Terminator(self, FilteringHandler(self, ButtonHandler(self, DigitalPinHandler(self))))

    def add_callback(self, key, object):
        self._callbacks[key] = object

    def run(self):
        self.monitor.debug('Harness running')
        while True:
            self.monitor.debug('checking for message')
            if self.incoming():
                command = self.receive_command()
                if not self.handler_chain.command(command):
                    self.monitor.error('No handler for %s' % str(event))
                    raise MissingHandlerException('No handler for %s' % str(event))

    def incoming(self):
        return self.port.poll()

    def button_event(self, event):
        button = self.callback(event.e_type)
        button._set_pressed(event.message == DOWN)

    def read_digital_event(self, event):
        pin = self.callback(event.e_type)
        pin._state = event.message

    def callback(self, key):
        return self._callbacks[key]

    def end(self):
        self.monitor.info('done')
        self.monitor.shutdown()
        self.port.close()
        self.radio_port.close()
        sys.exit(0)

    def receive_command(self):
        return self.port.receive_command()

    def send_message(self, e_type, message):
        return self.port.send_message(e_type, message)

    def send_radio_message(self, message):
        self.radio_port.send_radio_message(message)

    def next_radio_message(self):
        return self.radio_port.next_message()


_harness = Harness()

