from collections import namedtuple

import subprocess
import sys
import zmq
from mptdd.quber import Qber
import logging

Event = namedtuple('Event',['id','e_type','value'])

# TODO: rename to MicrobitController
class Controller(Qber):
    def __init__(self, log_level=logging.DEBUG):
        Qber.__init__(self)
        self.processes = []
        self.outputs = []
        logging.basicConfig(filename='testing.log', level=log_level,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def run(self, *scripts):
        logging.info('Starting test run')
        micro_count = len(scripts)
        self.bind_publisher(5561)
        self.watcher = self.context.socket(zmq.REP)
        self.watcher.bind('tcp://*:5562')
        id = 0
        logging.debug('Waiting for %i micro%s' % (micro_count, '' if micro_count == 1 else 's'))
        self.start_scripts(scripts)
        while id < micro_count:
            self.sync_recv() # wait for micro
            self.sync_send('%i' % id)
            id += 1
            logging.debug("+1 micro (%i/%i)" % (id, micro_count))

    def start_scripts(self, scripts):
        for script in scripts:
            print(script)
            self.processes.append(subprocess.Popen(['python'] + [script],
                                              cwd='/home/romilly/git/active/bdd-tester',
                                              stdout=subprocess.PIPE))


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

    # TODO: move to event-based system
    def read_event(self, timeout=10000):
        try:
            if self.watcher.poll(timeout=timeout):
                incoming = self.sync_recv()
                logging.debug('incoming %s' % incoming)
                sender_id = int(incoming[0])
                msg = incoming[2:]
                self.sync_send('')
                return Event(sender_id, 'display', msg)
        except KeyboardInterrupt:
            sys.exit(-1)
        raise Exception('Timed out waiting for %s to display' % text)

    def close(self):
        self.publish('END', '*')
        for process in self.processes:
            process.wait()
            self.outputs += [process.communicate()]
        logging.info('finished test run')

