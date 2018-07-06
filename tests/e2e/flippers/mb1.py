from microbit import *
import radio

__version__=0.1

radio.on()
while True:
    if button_a.is_pressed():
        radio.send('ouch')
        display.scroll('That hurt!')
        sleep(1000)
    message = radio.receive()
    if message:
        display.scroll('Poor you!')
    sleep(10)

