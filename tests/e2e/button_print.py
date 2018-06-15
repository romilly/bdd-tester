from microbit import *

def run():
    while True:
        if button_a.is_pressed():
            print('Ouch!')
            sleep(1000)

run()