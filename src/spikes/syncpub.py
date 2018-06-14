#
#  Synchronized publisher
#
import zmq


SUBSCRIBERS_EXPECTED = 2

def main():
    context = zmq.Context()

    # Socket to talk to clients
    publisher = context.socket(zmq.PUB)
    publisher.bind('tcp://*:5561')

    # Socket to receive signals
    syncservice = context.socket(zmq.REP)
    syncservice.bind('tcp://*:5562')

    # Get synchronization from subscribers
    subscribers = 0
    while subscribers < SUBSCRIBERS_EXPECTED:
        # wait for synchronization request
        msg = syncservice.recv()
        print('got sync')
        # send synchronization reply
        syncservice.send_string('%i' % subscribers)
        subscribers += 1
        print("+1 subscriber (%i/%i)" % (subscribers, SUBSCRIBERS_EXPECTED))
    publisher.send_string('button_a')
    publisher.send_string('END')

if __name__ == '__main__':
    main()
