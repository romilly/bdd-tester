import sys
from time import sleep

import subprocess
from mpbdd.helpers import event
import zmq

from mpbdd.quber import Qber


class Port(Qber):
    def __init__(self, monitor, publisher_port, watcher_port):
        Qber.__init__(self, monitor)
        self.context = zmq.Context()
        self.monitor = monitor
        self.bind_publisher(publisher_port)
        self.bind_watcher(watcher_port)

    def bind_publisher(self, port):
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind('tcp://*:%i' % port)

    def bind_watcher(self, s):
        self.watcher = self.context.socket(zmq.REP)
        self.watcher.bind('tcp://*:%i' % s)

    def sync_send(self, message):
        self.send(self.watcher, message)

    def sync_recv(self):
        return self.recv(self.watcher)

    def publish(self, message):
        self.monitor.debug('sending %s' % message)
        self.send(self.publisher, message)


class RadioPort(Port):
    def __init__(self, monitor):
        Port.__init__(self, monitor, 5563, 5564)
        self.poller = zmq.Poller()
        self.poller.register(self.watcher, zmq.POLLIN)
        # self.running = True

    def run(self, count):
        self.monitor.debug('radio controller about to sync with %i clients' % count)
        for i in range(count):
            self.sync_recv()  # wait for micro
            self.sync_send('')  # reply
            self.monitor.debug('radio controller synced with client %i' % i)
        # while self.running:
        while True:
            # self.monitor.debug('checking for radio to resend')
            if self.poller.poll(10):
                self.monitor.debug('incoming radio message' )
                incoming = self.sync_recv()
                self.monitor.debug('incoming radio message %s' % incoming)
                self.sync_send('')
                self.publish(incoming)



class MicrobitPort(Port):
    def __init__(self, monitor):
        Port.__init__(self, monitor, 5561, 5562)
        self.processes = []
        self.outputs = []

    def open(self, targets):
        self.start_microbits(targets)

    def read_event(self, timeout=1000):
        try:
            if self.watcher.poll(timeout=timeout):
                incoming = self.sync_recv()
                self.monitor.debug('sees incoming event %s' % incoming)
                self.sync_send('')
                return event(incoming)
        except KeyboardInterrupt:
            sys.exit(-1)
        except TimeoutError:
            self.monitor.error('Timed out waiting for event')
            self.close()
            sys.exit(-2)

    def start_microbits(self, targets):
        micro_count = len(targets)
        self.monitor.debug('Waiting for %i micro%s' % (micro_count, '' if micro_count == 1 else 's'))
        for target in targets:
            self.processes.append(subprocess.Popen(['python'] + [target.script],
                                                   cwd='/home/romilly/git/active/bdd-tester',
                                                   stdout=subprocess.PIPE))
            self.sync_recv()  # wait for micro
            self.sync_send(target.id)  # tell it its id
            self.monitor.debug("added %s" % target.id)

    def close(self):
        for process in self.processes:
            if not process.poll():
                process.terminate()
            self.outputs += [process.communicate()[0].decode('utf8')]
        self.monitor.debug('outputs: %s' % self.outputs)