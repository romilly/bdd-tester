#
#  Synchronized subscriber
#
import time

import zmq


def main():
    context = zmq.Context()

    # First, connect our subscriber socket
    subscriber = context.socket(zmq.SUB)
    subscriber.connect('tcp://localhost:5561')
    subscriber.setsockopt(zmq.SUBSCRIBE, b'')

    time.sleep(1)

    # Second, synchronize with publisher
    syncclient = context.socket(zmq.REQ)
    syncclient.connect('tcp://localhost:5562')

    # send a synchronization request
    syncclient.send_string('')

    # wait for synchronization reply
    id = syncclient.recv().decode('utf8')
    print('my id is %i' % int(id))


    # Third, get our updates and report how many we got
    nbr = 0
    while True:
        msg = subscriber.recv().decode('utf8')
        if msg == 'END':
            break
        nbr += 1

    print ('Received %d updates' % nbr)

if __name__ == '__main__':
    main()
