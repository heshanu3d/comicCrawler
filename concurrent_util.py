# coding:utf-8

# import io
# import sys
# import os
# import string
# import re
# import collections

from threading import Thread
from multiprocessing import Process
from time import sleep, ctime


def thread_loop(threads, thread_func, thread_args, thread_max_num):
    # print('threadLoop begin\n')
    wflag = True
    while wflag:
        if len(threads) < thread_max_num:
            t = Thread(target=thread_func, args=thread_args)
            t.start()
            threads.append(t)
            wflag = False
        for th in threads:
            if not th.is_alive():
                threads.remove(th)
            if wflag:
                sleep(0.2)


def process_loop(proceeds, process_func, process_args, process_max_num):
    wflag = True
    while wflag:
        if len(proceeds) < process_max_num:
            p = Process(target=process_func, args=process_args)
            p.start()
            proceeds.append(p)
            wflag = False
        for pr in proceeds:
            if not pr.is_alive():
                proceeds.remove(pr)
            if wflag:
                sleep(0.2)
