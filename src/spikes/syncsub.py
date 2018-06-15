#
#  Synchronized subscriber
#
import sys

import time

import zmq

from spikes.quber import Qber


class Subscriber(Qber):
    def __init__(self, button_a):
        Qber.__init__(self)
        self.subsock = None
        self.button_a = button_a
        # First, connect our subscriber socket
        self.subscribe(5561)
        time.sleep(1)
        # Second, synchronize with publisher
        self.sync(5562)
        # Initialize poll set
        self.poller = zmq.Poller()
        # poller.register(self.syncclient, zmq.POLLIN)
        self.poller.register(self.subsock, zmq.POLLIN)
        print('polling away')


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
            msg = self.sub_recv()
            # process weather update
        else:
            return
        print(msg)
        if msg == 'button_a':
            self.button_a._pressed = True
        if msg == 'END':
            print('done')
            sys.exit(0)

    def sub_recv(self):
        return self.recv(self.subsock)

    def sync(self, port):
        self.syncclient = self.context.socket(zmq.REQ)
        self.syncclient.connect('tcp://localhost:%i' % port)

        # send a synchronization request
        self.sync_send('')

        # wait for synchronization reply
        id = self.sync_recv()
        print('my id is %i' % int(id))

    def sync_recv(self):
        return self.recv(self.syncclient)

    def sync_send(self, message):
        self.send(self.syncclient, message)

    def subscribe(self, port):
        self.subsock = self.context.socket(zmq.SUB)
        self.subsock.connect('tcp://localhost:%i' % port)
        self.subsock.setsockopt(zmq.SUBSCRIBE, b'')
