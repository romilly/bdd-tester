#
#  Synchronized subscriber
#
import sys

import time

import zmq

from helpers.quber import Qber

# TODO: change sequence so we know id before we subscribe and use subscription filter properly!
class Harness(Qber):
    def __init__(self):
        Qber.__init__(self)
        self.subsock = None
        self._callbacks = {}
        # First, connect our subscriber socket
        self.subscribe(5561)
        time.sleep(1)
        # Second, synchronize with publisher
        self.id = int(self.sync(5562))
        # Initialize poll set
        self.poller = zmq.Poller()
        # poller.register(self.syncclient, zmq.POLLIN)
        self.poller.register(self.subsock, zmq.POLLIN)

    def add_callback(self, key, object):
        self._callbacks[key] = object


    def run(self):
        print('run')
        # msg = self.sub_recv()
        # Process messages from both sockets
        # while True:
        try:
            socks = dict(self.poller.poll())
        except KeyboardInterrupt:
             sys.exit(-1)

            # if receiver in socks:
            #     message = receiver.recv()
                # process task

        if self.subsock in socks:
            msg = self.pub_receive()
        else:
            return
        if msg == 'END':
            print('done')
            sys.exit(0)
        if msg in ['button_a', 'button_b']:
            self.callback(msg)._pressed = True

    def sub_recv(self):
        return self.recv(self.subsock)

    def sync(self, port):
        self.syncclient = self.context.socket(zmq.REQ)
        self.syncclient.connect('tcp://localhost:%i' % port)

        # send a synchronization request
        self.sync_send('')

        # wait for synchronization reply
        return self.sync_recv()

    def sync_recv(self):
        return self.recv(self.syncclient)

    def sync_send(self, message):
        self.send(self.syncclient, message)

    def send_message(self, message):
        self.sync_send('%i:%s' % (self.id, message))
        return self.sync_recv()

    def subscribe(self, port):
        self.subsock = self.context.socket(zmq.SUB)
        self.subsock.connect('tcp://localhost:%i' % port)
        self.subsock.setsockopt(zmq.SUBSCRIBE, b'')

    def callback(self, key):
        return self._callbacks[key]

    def pub_receive(self):
        incoming = self.sub_recv()
        target_id =incoming[0]
        msg = incoming[2:]
        if target_id == str(self.id) or target_id == '*':
            return msg
        else:
            return None

_harness = Harness()
