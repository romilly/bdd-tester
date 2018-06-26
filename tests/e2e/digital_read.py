from microbit import *
import radio


def run():
    radio.on()
    while True:
        if pin8.read_digital():
            print('pin 8 high')
            display.scroll('Ouch!')
            sleep(100)
        if pin16.read_digital():
            print('pin 16 high')
            display.scroll('That hurt!')
            sleep(100)
        sleep(100)

run()