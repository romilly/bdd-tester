from microbit import *


def run():
    while True:
        # print('going to check button a')
        if button_a.is_pressed():
            print('button A pressed')
            display.scroll('Ouch!')
            sleep(100)
        # print('going to check button b')
        if button_b.is_pressed():
            print('button B pressed')
            display.scroll('That hurt!')
            sleep(100)


run()