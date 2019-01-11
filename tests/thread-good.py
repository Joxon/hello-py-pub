# coding=utf-8

import time
from _thread import start_new_thread


def input_thread(p):
    i = input()
    print('You entered: ' + i)
    p.append(True)


pressed = []
start_new_thread(input_thread, (pressed, ))
i = 0
while not pressed:
    time.sleep(1)
    print(i)
    i += 1
