from microbit import *
import radio


def run():
    radio.on()
    while True:
        if button_a.is_pressed():
            print('button A pressed')
            radio.send('Ouch!')
            sleep(100)
        message = radio.receive()
        if message:
            display.scroll('signal received!')
        sleep(100)

run()