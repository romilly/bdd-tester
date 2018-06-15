#
#  Synchronized publisher
#
import time

import zmq

from spikes.quber import Qber

SUBSCRIBERS_EXPECTED = 1

class Publisher(Qber):
    def __init__(self):
        Qber.__init__(self)


    def run(self):

        # Socket to talk to clients
        self.bind_publisher(5561)

        # Socket to receive signals
        self.syncservice = self.context.socket(zmq.REP)
        self.syncservice.bind('tcp://*:5562')

        # Get synchronization from subscribers
        subscribers = 0
        while subscribers < SUBSCRIBERS_EXPECTED:
            # wait for synchronization request
            msg = self.sync_recv()
            # send synchronization reply
            self.sync_send('%i' % subscribers)
            subscribers += 1
            print("+1 subscriber (%i/%i)" % (subscribers, SUBSCRIBERS_EXPECTED))
        print('a')
        self.publish('button_a')
        time.sleep(1)
        print('a')
        self.publish('button_a')
        time.sleep(2)
        print('done')
        self.publish('END')

    def sync_send(self, message):
        self.send(self.syncservice, message)

    def sync_recv(self):
        return self.recv(self.syncservice)

    def publish(self, message):
        self.send(self.publisher, message)

    def bind_publisher(self, port):
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind('tcp://*:%i' % port)


if __name__ == '__main__':
   Publisher().run()
