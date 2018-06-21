import sys
from abc import ABCMeta, abstractmethod
import zmq

from mpbdd.handlers import Terminator, FilteringHandler, ButtonHandler, MissingHandlerException
from mpbdd.helpers import event_message, event
from mpbdd.microbitcontroller import DOWN, BUTTON_A, BUTTON_B
from mpbdd.monitors import LoggingMonitor
from mpbdd.quber import Qber

class Harness(Qber):
    def __init__(self, harness_monitor=None):
        Qber.__init__(self)
        self.id = ''
        if not harness_monitor:
            harness_monitor = LoggingMonitor(self, 'logs/testing.log')
        self.monitor = harness_monitor
        self.monitor=harness_monitor
        self.subsock = None
        self._callbacks = {}
        self.monitor.info('Harness created')
        self.subscribe(5561)
        self.id = self.sync(5562)
        self.monitor.debug('my name is %s' % self.id)
        self.handler = Terminator(self, FilteringHandler(self, ButtonHandler(self)))

    def add_callback(self, key, object):
        # self.monitor.debug('adding callback %s = %s' % (key, str(object)))
        self._callbacks[key] = object

    def run(self):
        self.monitor.debug('Harness running')
        while True:
            self.monitor.debug('checking for message')
            if self.subsock.poll():
                self.monitor.debug('incoming message')
                command = self.receive_command()
                if not self.handler.command(command):
                    self.monitor.error('No handler for %s' % str(event))
                    raise MissingHandlerException('No handler for %s' % str(event))

    def button_event(self, event):
        button = self.callback(event.e_type)
        button._set_pressed(event.message == DOWN)

    def sub_recv(self):
        return self.recv(self.subsock)

    def sync(self, port):
        self.syncclient = self.context.socket(zmq.REQ)
        self.syncclient.connect('tcp://localhost:%i' % port)
        self.sync_send('')
        return self.sync_recv()

    def sync_recv(self):
        return self.recv(self.syncclient)

    def sync_send(self, message):
        self.send(self.syncclient, message)

    def send_message(self, e_type, message):
        msg = event_message(e_type, message, self.id)
        self.monitor.debug('sending %s' % msg)
        self.sync_send(msg)
        return self.sync_recv()

    def subscribe(self, port):
        self.subsock = self.context.socket(zmq.SUB)
        self.subsock.connect('tcp://localhost:%i' % port)
        self.subsock.setsockopt(zmq.SUBSCRIBE, b'')

    def callback(self, key):
        return self._callbacks[key]

    def receive_command(self):
        incoming = self.sub_recv()
        self.monitor.debug('got %s' % incoming)
        return event(incoming)

    def end(self):
        self.monitor.info('done')
        self.monitor.shutdown()
        sys.exit(0)


_harness = Harness()

