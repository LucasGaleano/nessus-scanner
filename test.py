from concurrent.futures import ThreadPoolExecutor
import time
import threading
import random


def task():
    print(f'My name is {threading.current_thread().name} and just waiting...')
    time.sleep(random.randint(5,15))
    print(f'My name is {threading.current_thread().name} and i go away...')

def main():
    executor = ThreadPoolExecutor(max_workers=2,thread_name_prefix="lala")
    for _ in range(5):
        executor.submit(task)



main()
