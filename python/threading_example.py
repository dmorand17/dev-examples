#!/usr/bin/python3

from threading import Thread, current_thread
import concurrent.futures
import threading
from queue import Queue
import logging
import os
import time
import random

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MyThread(threading.Thread):
    def __init__(self, threadID=None,name=None, counter=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        pass

    def run(self):
        simple_exec(7)

# Without extending Thread class
class NoThread():
    def sayHi(self,msg):
        for i in range(12):
            logger.info(f"{current_thread().getName()}: {msg}")
            time.sleep(0.3)

def thread_decorator(func):
    # Decorator to print messages before/after calling function
    def wrapper():
        print(f"\n{style.GREEN}Starting [{func.__name__}]{style.RESET}")
        start = time.time()
        func()
        end = time.time()
        print(f"{style.GREEN}Finished [{func.__name__}]{style.RESET} in {end-start:.4f} seconds \n")
    return wrapper

def simple_exec(cnt):
    logger.info(f"{current_thread().getName()}: running {cnt} times")
    for i in range(cnt):
        logger.info(f"{current_thread().getName()}: child executing...")
        time.sleep(0.2)

@thread_decorator
def basic_thread():
    t = Thread(target=simple_exec,args=(5,))
    logger.info(f"{current_thread().getName()}: Starting")
    t.start() # execute the thread
    t.join() # ensure the threads wait to complete before continuing
    logger.info(f"{current_thread().getName()}: Finished")

@thread_decorator
def thread_class():
    t = MyThread(threadID=7,name="DougieThread")
    t.start()
    t.join()
    time.sleep(2) # sleep for 2 seconds

@thread_decorator
def without_extending_thread():
    myobj = NoThread()
    t1 = Thread(target=myobj.sayHi,args=("Yo yo yo",))
    t2 = Thread(target=myobj.sayHi,args=("waddup waddup",))

    # Start both threads
    t1.start()
    t2.start()

    t1.join() # wait until thread1 finishes
    t2.join() # wait until thread2 finishes

    time.sleep(2)
    logger.info("All done...")

@thread_decorator
def thread_executor():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        #executor.map(simple_exec(random.randint(1,12)), range(3))
        for idx in range(3):
            executor.submit(simple_exec(random.randint(1,9)))
    logging.info(f"Completed!")

def main():
    basic_thread()
    thread_class()
    without_extending_thread()
    thread_executor()

if __name__ == '__main__':
    main()