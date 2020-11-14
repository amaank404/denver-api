"""
Thread Control
"""

__version__ = '2020.11.11'
__author__ = "Xcodz"

from threading import Thread, Lock
import functools
import random
import time


def runs_parallel(_func=None, *, assure_finish=False):
    def wrap_around_decorator(function):
        @functools.wraps(function)
        def thread_func(*args, **kwargs):
            thread = Thread(target=function, args=args, kwargs=kwargs, daemon=not assure_finish, name=function.__name__)
            thread.start()
        return thread_func
    if _func is None:
        return wrap_around_decorator
    else:
        return wrap_around_decorator(_func)


class ThreadManager:
    def __init__(self, initial_threads: list = None):
        if initial_threads is None:
            initial_threads = []
        self.thread_pool = initial_threads

    def add(self, function, *args, **kwargs):
        self.thread_pool.append((function, args, kwargs))

    def start_execution(self, maximum_thread_count=20):
        currently_executing = []
        while len(self.thread_pool) > 0:
            if len(currently_executing) < maximum_thread_count:
                function_to_use = self.thread_pool.pop(0)
                new_thread = Thread(target=function_to_use[0], args=tuple(function_to_use[1]),
                                    kwargs=function_to_use[2], name=function_to_use[0].__name__, daemon=False)
                new_thread.start()
                currently_executing.append(new_thread)
            for x in currently_executing:
                if not x.is_alive():
                    currently_executing.remove(x)


if __name__ == '__main__':
    print_lock = Lock()

    def create_files(number):
        time.sleep(random.randint(3, 10) // 4)
        with print_lock:
            print(f"Created File {number}")

    manager = ThreadManager()
    for x in range(1000):
        manager.add(create_files, x)
    manager.start_execution(1000)
