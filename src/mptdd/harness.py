#
#  Synchronized subscriber
#
import sys
from abc import ABCMeta, abstractmethod

import zmq
import logging

from mptdd.helpers import event_message, event
from mptdd.quber import Qber


class CommandHandler(metaclass=ABCMeta):
    def __init__(self, harness, successor=None):
        self._harness = harness
        self._successor = successor

    def command(self, event):
        if self.handle_command(event):
            return
        if self._successor:
            self._successor.handle_command(event)
        raise Exception('No handler for %s' % event)

    @abstractmethod
    def handle_command(self, event):
        pass


class Terminator(CommandHandler):
    def handle_command(self, event):
        if event.e_type == 'END':
            logging.info('done')
            logging.shutdown()
            sys.exit(0)
        else:
            return False


class ButtonHandler(CommandHandler):
    def handle_command(self, event):
        if event.e_type.startswith('button'):
            self._harness.callback(event.e_type)._pressed = True
            return True



class Harness(Qber):
    def __init__(self):
        Qber.__init__(self)
        self.subsock = None
        self._callbacks = {}
        logging.basicConfig(filename='logs/testing1.log', level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info('Starting test run')
        self.subscribe(5561)
        self.id = self.sync(5562)
        logging.debug('my id is %s' % self.id)
        self.handler_chain = ButtonHandler(self, Terminator(self))

    def add_callback(self, key, object):
        self._callbacks[key] = object

    def run(self):
        logging.debug('run')
        try:
            if self.subsock.poll():
                command = self.receive_command()
            else:
                return
            self.handler_chain.command(command)
        except Exception as e:
            logging.exception(e)
            logging.shutdown()
            sys.exit(-2)

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
        self.sync_send(event_message(e_type, message, self.id))
        return self.sync_recv()

    def subscribe(self, port):
        self.subsock = self.context.socket(zmq.SUB)
        self.subsock.connect('tcp://localhost:%i' % port)
        self.subsock.setsockopt(zmq.SUBSCRIBE, b'')

    def callback(self, key):
        return self._callbacks[key]

    def receive_command(self):
            incoming = self.sub_recv()
            logging.debug(incoming)
            logging.debug('bit %s got %s' % (self.id, incoming))
            return event(incoming)




_harness = Harness()
