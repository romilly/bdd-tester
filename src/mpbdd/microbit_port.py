import sys
import subprocess
import zmq
from mpbdd.helpers import event
from mpbdd.quber import Qber


class MicrobitPort(Qber):
    def __init__(self, monitor):
        Qber.__init__(self)
        self.monitor = monitor
        self.processes = []
        self.outputs = []

    def open(self, targets):
        self.bind_publisher(5561)
        self.bind_watcher('5562')
        self.start_microbits(targets)

    def bind_publisher(self, port):
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind('tcp://*:%i' % port)

    def bind_watcher(self, s):
        self.watcher = self.context.socket(zmq.REP)
        self.watcher.bind('tcp://*:%s' % s)

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

    def sync_send(self, message):
        self.send(self.watcher, message)

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

    def sync_recv(self):
        return self.recv(self.watcher)

    def publish(self, message):
        self.monitor.debug('sending %s' % message)
        self.send(self.publisher, message)

    def close(self):
        for process in self.processes:
            # TODO: terminate only if still running
            process.terminate()
            self.outputs += [process.communicate()[0].decode('utf8')]
        self.monitor.debug('outputs: %s' % self.outputs)