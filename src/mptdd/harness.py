#
#  Synchronized subscriber
#
import sys
import zmq
import logging

from mptdd.quber import Qber


class Harness(Qber):
    def __init__(self):
        Qber.__init__(self)
        self.subsock = None
        self._callbacks = {}
        logging.basicConfig(filename='testing1.log', level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info('Starting test run')
        self.subscribe(5561)
        self.id = int(self.sync(5562))
        print('my id is %i' % self.id)
        self.re_subscribe()
        self.poller = zmq.Poller()
        self.poller.register(self.subsock, zmq.POLLIN)

    def add_callback(self, key, object):
        self._callbacks[key] = object


    def run(self):
        print('run')
        try:
            socks = dict(self.poller.poll())
        except KeyboardInterrupt:
             sys.exit(-1)

        if self.subsock in socks:
            msg = self.pub_receive()
        else:
            return
        if msg == 'END':
            logging.info('done')
            sys.exit(0)
        if msg in ['button_a', 'button_b']:
            self.callback(msg)._pressed = True

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
        logging.debug(incoming)
        print('bit %i got %s' % (self.id, incoming))
        target_id =incoming[0]
        msg = incoming[2:]
        if target_id == str(self.id) or target_id == '*':
            return msg
        else:
            return None

    def re_subscribe(self):
        logging.debug('id set to %i' % self.id)
        self.subsock.setsockopt(zmq.UNSUBSCRIBE, b'')
        self.subsock.setsockopt(zmq.SUBSCRIBE, b'*') # radio messages
        self.subsock.setsockopt(zmq.SUBSCRIBE, str(self.id).encode('utf8'))



_harness = Harness()
