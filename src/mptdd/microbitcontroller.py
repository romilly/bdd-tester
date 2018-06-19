import subprocess
import sys
import zmq

from mptdd.helpers import event, event_message
from mptdd.quber import Qber
import logging


class MicrobitController(Qber):
    def __init__(self, log_level=logging.DEBUG):
        Qber.__init__(self)
        self.processes = []
        self.outputs = []
        logging.basicConfig(filename='../../logs/testing.log', level=log_level,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def run(self, *scripts):
        logging.info('Starting test run')
        self.bind_publisher(5561)
        self.bind_watcher('5562')
        self.start_microbits(scripts)

    def start_microbits(self, scripts):
        micro_count = len(scripts)
        logging.debug('Waiting for %i micro%s' % (micro_count, '' if micro_count == 1 else 's'))
        for (id, script) in enumerate(scripts):
            self.processes.append(subprocess.Popen(['python'] + [script],
                                                   cwd='/home/romilly/git/active/bdd-tester',
                                                   stdout=subprocess.PIPE))
            self.sync_recv()  # wait for micro
            self.sync_send('%i' % id)  # tell it its id
            logging.debug("+1 micro (%i/%i)" % (id, micro_count))

    def bind_watcher(self, s):
        self.watcher = self.context.socket(zmq.REP)
        self.watcher.bind('tcp://*:%s' % s)

    def sync_send(self, message):
        self.send(self.watcher, message)

    def sync_recv(self):
        return self.recv(self.watcher)

    def publish(self, message):
        logging.debug(message)
        self.send(self.publisher, message)

    def bind_publisher(self, port):
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind('tcp://*:%i' % port)

    def read_event(self, timeout=1000):
        try:
            if self.watcher.poll(timeout=timeout):
                incoming = self.sync_recv()
                logging.debug('incoming event %s' % incoming)
                self.sync_send('')
                return event(incoming)
        except KeyboardInterrupt:
            sys.exit(-1)
        except TimeoutError:
            logging.error('Timed out waiting for event')
            self.close()
            sys.exit(-2)


    def close(self):
        self.publish_command('END', '*')
        for process in self.processes:
            process.wait()
            self.outputs += [process.communicate()]
        logging.info('finished test run')

    def publish_command(self, command, to='0', value=''):
        self.publish(event_message(to, command, value))

