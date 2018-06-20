from mpbdd.helpers import event, event_message, DEFAULT_NAME
from mpbdd.microbit_port import MicrobitPort
import logging


class MicrobitController():
    def __init__(self, log_level=logging.DEBUG):
        logging.basicConfig(filename='../../logs/testing.log', level=log_level,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.port = MicrobitPort()

    def run(self, *targets):
        logging.info('Starting test run')
        self.port.open(targets)

    def close(self):
        self.publish_command('END', '*')
        self.port.close()

    def publish_command(self, command, value='', id=DEFAULT_NAME):
        self.port.publish(event_message(command, value, id))

    def read_event(self):
        return self.port.read_event()

