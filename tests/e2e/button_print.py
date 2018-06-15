from microbit import *


def run():
    while True:
        if button_a.is_pressed():
            print('button A pressed')
            display.scroll('Ouch!')
            sleep(10)

run()