import sys
import zmq
from mptdd.quber import Qber
import logging


class Controller(Qber):
    def __init__(self, micro_count=2, log_level=logging.DEBUG):
        Qber.__init__(self)
        logging.basicConfig(filename='testing.log', level=log_level,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._micro_count = micro_count
        logging.info('Starting test run')
        self.bind_publisher(5561)
        self.watcher = self.context.socket(zmq.REP)
        self.watcher.bind('tcp://*:5562')
        id = 0
        logging.debug('Waiting for %i micro%s' % (micro_count, '' if micro_count == 1 else 's'))
        while id < self._micro_count:
            self.sync_recv() # wait for micro
            self.sync_send('%i' % id)
            id += 1
            logging.debug("+1 micro (%i/%i)" % (id, self._micro_count))

    def run(self):
        self.publish('button_a')
        self.expect_display('Ouch!')
        self.publish('button_a', 1)
        self.expect_display('Ouch!', 1)
        # self.publish('button_a')
        # self.expect_display('Ouch!')
        self.publish('END','*')
        logging.info('finished test run')

    def sync_send(self, message):
        self.send(self.watcher, message)

    def sync_recv(self):
        return self.recv(self.watcher)

    def publish(self, message, id='0'):
        text = '%s:%s' % (id, message)
        logging.debug(text)
        self.send(self.publisher, text)

    def bind_publisher(self, port):
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind('tcp://*:%i' % port)

    def expect_display(self, text, id=0, timeout=10000):
        try:
            if self.watcher.poll(timeout=timeout):
                incoming = self.sync_recv()
                logging.debug('incoming %s' % incoming)
                sender_id = int(incoming[0])
                msg = incoming[2:]
                self.sync_send('')
                if msg == text and id == sender_id :
                    return
                else:
                    raise ValueError('Ugh! got %s from %i' % (msg, sender_id))
        except KeyboardInterrupt:
            sys.exit(-1)
        raise Exception('Timed out waiting for %s to display' % text)


if __name__ == '__main__':
   Controller(log_level=logging.DEBUG).run()
