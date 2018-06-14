from oo_quizmaster import PublicFace, Participant


class Payload():
    def __init__(self, sender):
        self.sender = sender

    def apply_to(self, interface):
        raise NotImplementedError()


class ButtonEvent(Payload):
    def apply_to(self, interface):
        if interface.id == self.sender:
            interface.press(self.button)


    def __init__(self, sender, button):
        Payload.__init__(self, sender)
        self.button = button


class RadioMessage(Payload):
    def __init__(self, sender, message):
        Payload.__init__(self, sender)
        self.message = message




class Controller():
    def __init__(self):
        self.interfaces = [MockInterface(id, self) for id in range(5)]
        self.participants = [Participant(interface) for interface in self.interfaces]

    def event(self, payload):
        for interface in self.interfaces:
            interface.event(payload)


class MockInterface(PublicFace):
    def __init__(self, id, controller):
        self.id = id
        self.controller = controller

    def wait_for_event(self):
        pass

    def say(self, text):
        self.controller.event()

    def a_pressed(self):
        pass


    def b_pressed(self):
        pass

    def c_pressed(self):
        pass

    def d_pressed(self):
        pass

    def send(self, text):
        pass

    def receive(self):
        pass

    def reset(self):
        pass

    def event(self, payload):
        payload.apply_to(self)



