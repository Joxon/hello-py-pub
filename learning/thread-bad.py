# coding=utf-8
import threading
import time


def input_thread(pressed):
    input()
    pressed.append(True)


def loop_thread(pressed):
    i = 0
    while not pressed:
        time.sleep(1)
        print(i)
        i += 1


pressed = []
i = threading.Thread(target=input_thread(pressed), args=(pressed,))
i.run()
l = threading.Thread(target=loop_thread(pressed), args=(pressed,))
l.run()
