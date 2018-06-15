#
#  Synchronized publisher
#
import sys
import time
import zmq
from helpers.quber import Qber


class Publisher(Qber):
    def __init__(self, subscribers=1):
        Qber.__init__(self)
        self._subscribers = subscribers
        self.bind_publisher(5561)
        self.syncservice = self.context.socket(zmq.REP)
        self.syncservice.bind('tcp://*:5562')
        subscribers = 0
        while subscribers < self._subscribers:
            self.sync_recv()
            self.sync_send('%i' % subscribers)
            subscribers += 1
            print("+1 subscriber (%i/%i)" % (subscribers, self._subscribers))


    def run(self):

        print('a')
        self.publish('button_a')
        self.expect_display('Ouch!')
        print('a')
        self.publish('button_a')
        self.expect_display('Ouch!')
        print('done')
        self.publish('END')

    def sync_send(self, message):
        self.send(self.syncservice, message)

    def sync_recv(self):
        return self.recv(self.syncservice)

    def publish(self, message, id=0):
        self.send(self.publisher, '%i:%s' % (id, message))

    def bind_publisher(self, port):
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind('tcp://*:%i' % port)

    def expect_display(self, text, id=0, timeout=10000):
        try:
            if self.syncservice.poll(timeout=timeout):
                incoming = self.sync_recv()
                sender_id = int(incoming[0])
                msg = incoming[2:]
                self.sync_send('')
#                self.sync_send('')
                if msg == text and id == sender_id :
                    return
                else:
                    raise ValueError('Ugh! got %s from %i' % (msg, id))
        except KeyboardInterrupt:
            sys.exit(-1)
        raise Exception('Timed out waiting for %s to display' % text)


if __name__ == '__main__':
   Publisher().run()
