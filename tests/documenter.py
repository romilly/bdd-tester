from unittest import TestCase


class AbstractControllerTest(TestCase):


    def run_scripts(self, *targets):
        pass

    def expect(self, *events):
        for event in events:
            print('Expect %s displayed on %s' % (event.message, event.id))

    def press(self, mbit, button):
        print('Press %s on %s' % (button, mbit))

    def press_extra(self, mbit, button):
        self.press(mbit, button)