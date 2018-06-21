import logging

class Monitor():
    def info(self, message):
        pass

    def debug(self, message):
        pass

    def warning(self, message):
        pass

    def error(self, message):
        pass

    def exception(self, message):
        pass

    def shutdown(self):
        pass




class LoggingMonitor():
    def __init__(self, target, filename):
        self.target = target
        # TODO: set width of level field
        # TODO: add module info?
        logging.basicConfig(filename=filename, level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def prefix(self, message):
        return '%s %s' % (self.target.id, message)

    def info(self, message):
        logging.info(self.prefix(message))

    def debug(self, message):
        logging.debug(self.prefix(message))

    def warning(self, message):
        logging.warning(self.prefix(message))

    def error(self, message):
        logging.error(self.prefix(message))

    def exception(self, message):
        logging.exception(self.prefix(message))

    def shutdown(self):
        logging.shutdown()