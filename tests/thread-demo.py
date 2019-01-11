#!/usr/bin/python3

import _thread
import time


# Define a function for the thread
def print_time(thread_name, delay):
    count = 0
    while count < 3:
        time.sleep(delay)
        count += 1
        print("%s: %s" % (thread_name, time.ctime(time.time())))


# Create two threads as follows
try:
    _thread.start_new_thread(print_time, ("Thread-1", 1))
    _thread.start_new_thread(print_time, ("Thread-2", 3))
except:
    print("Error: unable to start thread")

while 1:
    pass

# from time import sleep
# import msvcrt
# i=0
# while True:
#     if msvcrt.kbhit():
#         print(msvcrt.getch())
#     print(i)
#     sleep(1)
#     i = i + 1

# try:
#     i = 0
#     while True:
#         print(i)
#         sleep(1)
#         i = i + 1
# except KeyboardInterrupt:
#     pass
