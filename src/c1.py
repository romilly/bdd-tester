import multiprocessing
from unittest import TestCase
from time import sleep
import zmq
from hamcrest import assert_that, contains_string


def logname(id):
    return 'log%d.txt' % id


class Client():
    def __init__(self, id):
        self.id = id
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, str(self.id))
        self.socket.connect("tcp://localhost:5555")

    def close(self):
        pass

    def log(self, message):
        with open(logname(self.id),'a') as log:
            log.write(message+'\n')

    def run(self):
        while True:
            message = self.socket.recv_string()
            self.log(message)
            if message.index(Controller.STOP) > 0:
                break
        self.close()


class Controller():
    STOP = 'stop'

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:5555")


    def send(self, id, message):
        self.socket.send_string('%i %s' % (id, message))


def read(logfile):
    with open(logfile) as f:
        return f.read()


def run_client(id):
    Client(id).run()


class ControllerTest(TestCase):
    def test_closes_client(self):
        controller = Controller()
        threads = [multiprocessing.Process(None, run_client, args=(id,)) for id in range(3)]
        for thread in threads:
            thread.start()
        sleep(1) # ugh!
        for i in range(3):
            controller.send(i, Controller.STOP)
        for thread in threads:
            thread.join()
        for id in range(3):
            assert_that(read(logname(id)), contains_string(Controller.STOP))

