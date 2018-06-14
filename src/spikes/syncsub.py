#
#  Synchronized subscriber
#
import time

import zmq

class Subscriber():
    def __init__(self):
        self.context = zmq.Context()
        self.subsock = None

    def run(self):

        # First, connect our subscriber socket
        self.subscribe(5561)

        time.sleep(1)

        # Second, synchronize with publisher
        self.sync()



        # Third, get our updates and report how many we got
        nbr = 0
        while True:
            msg = self.sub_recv()
            if msg == 'END':
                break
            nbr += 1

        print ('Received %d updates' % nbr)

    def sub_recv(self):
        return self.recv(self.subsock)

    def sync(self):
        self.syncclient = self.context.socket(zmq.REQ)
        self.syncclient.connect('tcp://localhost:5562')

        # send a synchronization request
        self.sync_send('')

        # wait for synchronization reply
        id = self.sync_recv()
        print('my id is %i' % int(id))

    def recv(self, socket):
        return socket.recv().decode('utf8')

    def sync_recv(self):
        return self.recv(self.syncclient)

    def sync_send(self, message):
        self.syncclient.send_string(message)

    def subscribe(self, port):
        self.subsock = self.context.socket(zmq.SUB)
        self.subsock.connect('tcp://localhost:%i' % port)
        self.subsock.setsockopt(zmq.SUBSCRIBE, b'')


if __name__ == '__main__':
   Subscriber().run()
