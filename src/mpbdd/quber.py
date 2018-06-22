import zmq

class Qber():
    def __init__(self, monitor):
        self.context = zmq.Context()
        self.monitor = monitor

    def recv(self, socket):
        return socket.recv().decode('utf8')

    def send(self, socket, message):
        socket.send_string(message)

