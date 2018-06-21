import sys
import zmq

from mpbdd.handlers import Terminator, FilteringHandler, ButtonHandler, MissingHandlerException
from mpbdd.helpers import event_message, event
from mpbdd.microbitcontroller import DOWN
from mpbdd.monitors import LoggingMonitor
from mpbdd.quber import Qber


class HarnessPort(Qber):
    def __init__(self, monitor):
        Qber.__init__(self)
        self.monitor = monitor
        self.subsock = None
        self.subscribe(5561)
        self.set_id(self.sync(5562))
        self.monitor.debug('my name is %s' % self.id)

    def set_id(self, id):
        self.id = id

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

    def receive_command(self):
        incoming = self.sub_recv()
        self.monitor.debug('got %s' % str(incoming))
        return event(incoming)


class Harness():
    def __init__(self, monitor=None):
        self.id = ''
        if not monitor:
            monitor = LoggingMonitor(self, 'logs/testing.log')
        self.monitor = monitor
        self.port = HarnessPort(monitor)
        self.id = self.port.id
        self._callbacks = {}
        self.monitor.info('Harness created')
        self.handler_chain = Terminator(self, FilteringHandler(self, ButtonHandler(self)))

    def add_callback(self, key, object):
        # self.monitor.debug('adding callback %s = %s' % (key, str(object)))
        self._callbacks[key] = object

    def run(self):
        self.monitor.debug('Harness running')
        while True:
            self.monitor.debug('checking for message')
            if self.incoming():
                self.monitor.debug('incoming message')
                command = self.receive_command()
                self.monitor.debug('command is %s' % str(command))
                if not self.handler_chain.command(command):
                    self.monitor.error('No handler for %s' % str(event))
                    raise MissingHandlerException('No handler for %s' % str(event))

    def incoming(self):
        return self.port.subsock.poll()

    def button_event(self, event):
        button = self.callback(event.e_type)
        button._set_pressed(event.message == DOWN)


    def callback(self, key):
        return self._callbacks[key]


    def end(self):
        self.monitor.info('done')
        self.monitor.shutdown()
        sys.exit(0)

    def receive_command(self):
        return self.port.receive_command()

    def send_message(self, e_type, message):
        return self.port.send_message(e_type, message)


_harness = Harness()

