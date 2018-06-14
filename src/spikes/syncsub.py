#
#  Synchronized subscriber
#
import time

import zmq

from spikes.quber import Qber


class Subscriber(Qber):
    def __init__(self):
        Qber.__init__(self)
        self.subsock = None

    def run(self):

        # First, connect our subscriber socket
        self.subscribe(5561)

        time.sleep(1)

        # Second, synchronize with publisher
        self.sync(5562)

        # Third, get our updates and report how many we got
        self.process_messages()

    def process_messages(self):
        while True:
            msg = self.sub_recv()
            print(msg)
            if msg == 'END':
                break

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


if __name__ == '__main__':
   Subscriber().run()
