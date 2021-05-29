"""
Thread Control - A simpler, cleaner interface for beginners
"""

__version__ = "2021.5.29"
__author__ = "Xcodz"

import functools
from threading import Thread


def runs_parallel(_func=None, assure_finish=False):
    """
    use this function decorator to make it run as a thread when called. If
    `assure_finish` is True then make sure python does not quit without the functions completion

    Example:

    ```python
    import time
    from denverapi.thread_control import runs_parallel

    @runs_parallel
    def long_function(arg):
        while True:
            print(arg)
            time.sleep(1.5)


    @runs_parallel(assure_finish=True)  # If you set it to False, The function will terminate before it is finished
    def long_function_2():
        for x in range(5):
            print(x)
            time.sleep(2)

    def main():
        long_function("Hello")
        lonf_function_2()

    main()
    ```
    """

    def wrap_around_decorator(function):
        @functools.wraps(function)
        def thread_func(*args, **kwargs):
            thread = Thread(
                target=function,
                args=args,
                kwargs=kwargs,
                daemon=not assure_finish,
                name=function.__name__,
            )
            thread.start()

        return thread_func

    if _func is None:
        return wrap_around_decorator
    else:
        return wrap_around_decorator(_func)
