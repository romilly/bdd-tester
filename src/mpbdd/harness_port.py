from queue import Queue
from time import sleep

import zmq
from mpbdd.helpers import event_message, event
from mpbdd.quber import Qber


class HarnessPort(Qber):
    def __init__(self, monitor):
        Qber.__init__(self, monitor)

    def open(self, subscriber_port, sync_port):
        self.subscribe(subscriber_port)
        self.sync_response = self.sync(sync_port)

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
        self.sync_send(msg)
        result = self.sync_recv()
        return result

    def subscribe(self, port):
        self.subsock = self.context.socket(zmq.SUB)
        self.subsock.connect('tcp://localhost:%i' % port)
        self.subsock.setsockopt(zmq.SUBSCRIBE, b'')

    def receive_command(self):
        incoming = self.sub_recv()
        return event(incoming)

    def poll(self):
        return self.subsock.poll()

    def close(self):
        self.syncclient.close()
        self.subsock.close()


class CommandPort(HarnessPort):
    def __init__(self, monitor):
        HarnessPort.__init__(self, monitor)

    def open(self, subscriber_port, sync_port):
        HarnessPort.open(self, subscriber_port, sync_port)
        self.id = self.sync_response
        # self.monitor.debug('my name is %s' % self.id)


class RadioPort(HarnessPort):
    def __init__(self, monitor):
        HarnessPort.__init__(self, monitor)
        self.messages_in = Queue()
        self.messages_out = Queue()

    def run(self):
        self.id = self.monitor.target.id
        self.open(5563, 5564)
        self.poller = zmq.Poller()
        self.poller.register(self.subsock, zmq.POLLIN)
        while True:
            if self.poller.poll(10):
                command = self.receive_command()
                if command.id != self.id:
                    self.messages_in.put(command)
            if not self.messages_out.empty():
                command = self.messages_out.get()
                self.send_message('radio', command)
            sleep(0.01)

    def next_message(self):
        if self.messages_in.empty():
            return None
        incoming = self.messages_in.get()
        self.monitor.debug('getting radio message <%s> from %s' % (incoming.message, incoming.id))
        return incoming.message

    def send_radio_message(self, message):
        self.messages_out.put(message)

    def close(self):
        self.poller.unregister(self.subsock)
        HarnessPort.close(self)








