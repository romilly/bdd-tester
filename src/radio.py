from mpbdd.harness import _harness



def on():
    pass


def send(message):
    _harness.send_radio_message(message)

def receive():
    return _harness.next_radio_message()