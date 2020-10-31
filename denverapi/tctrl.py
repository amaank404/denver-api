"""
Thread Control
"""

__version__ = '2020.10.31'
__author__ = "Xcodz"

from threading import Thread
import functools


def runs_parallel(_func=None, *, assure_finish=False):
    def wrap_around_decorator(function):
        @functools.wraps(function)
        def thread_func(*args, **kwargs):
            thread = Thread(target=function, args=args, kwargs=kwargs, daemon=assure_finish, name=function.__name__)
            thread.start()
        return thread_func
    if _func is None:
        return wrap_around_decorator
    else:
        return wrap_around_decorator(_func)
