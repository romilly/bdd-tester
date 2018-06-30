## micro:bit MicroPython Testing Framework

The framework uses an adapter interface to allow the test program to simulate
the effects of button presses and digital inputs on a micro:bit running MicroPython.

It also captures what is displayed and/or printed by the simulated system, and
handles the sending and receiving of radio messages

It replaces real hardware interactions by interactions with a
test harness.

The controller starts one additional process per micro:bit under test.

The micro:bit processes handle incoming and outgoing events and (in separate threads)
handle radio messages.

The framework is (just) past the proof-of-concept stage, but there's lots
to do before it can be considered complete.
I am currently using it to test a complex application with three micro:bits
linked by radio.

### 5 minute guide

##### Write a script for each micro:bit in the usual way.
Here's a simple example called *button_radio.py*:

```
from microbit import *
import radio

def run():
    radio.on()
    while True:
        # print('going to check button a')
        if button_a.is_pressed():
            print('button A pressed')
            radio.send('Ouch!')
            sleep(100)
        message = radio.receive()
        if message:
            display.scroll('signal received!')
        sleep(100)

run()
```

#### Create a unit test:


```  
import sys
from unittest import TestCase

from hamcrest import assert_that

from helpers import is_event
from mpbdd.helpers import Target
from mpbdd.microbitcontroller import MicrobitController, BUTTON_A

# You won't need the line below once the framework is in PiPi
# For now, adjust it to refer to the location of the cloned code on your computer
sys.path += '/home/romilly/git/active/bdd-tester/src'


class QuizTest(TestCase):
    def setUp(self):
        self.controller = MicrobitController()

    def test_button_and_display(self):
        # adjust these to reflect the relative or absolute path to the script to run on the microbit
        self.controller.run(Target('tests/e2e/button_radio.py'),Target('tests/e2e/button_radio.py','microbit 2'))
        self.controller.press(BUTTON_A)
        event = self.controller.read_event()
        assert_that(event, is_event('display', 'signal received!', 'microbit 2'))

    def tearDown(self):
        self.controller.close()
```

#### Run the test

Run the test in the usual way.

The test simulates two micro:bits, both running the same script.

The test will simulate the pressing of button A on the first micro:bit,
which then will then send a radio message.

When the second micro:bit receives rthe radi message, it displays 








 



