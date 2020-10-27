"""
This module provides you with basic logging facilities which
can be used by your programs to get developed easily. while
debugging you can keep the configurations on and while
releasing you can switch of error, warnings, debug or you
can also change the file to a new file which can contain
the log.
"""
__version__ = "2020.6.4"
__author__ = "Xcodz"

import sys, os, time

conf = {
    "debug": True,
    "error": True,
    "warning": True,
}

formatables = ["name", "error", "msg", "asctime", "pid", "ppid", "level"]


class Logger:
    def __init__(self, name, conf=conf, file=sys.stderr):
        self.name = name
        self.conf = conf
        self.format = "{level}:{name}:{msg}\n"
        self.file = file

    def debug(self, info, error=None):
        if self.conf["debug"]:
            self.file.write(
                self.format.format(
                    name=self.name,
                    error=error,
                    pid=os.getpid(),
                    level="DEBUG",
                    ppid=os.getppid(),
                    msg=info,
                    asctime=time.asctime(),
                )
            )
            self.file.flush()

    def error(self, info, error=None):
        if self.conf["error"]:
            self.file.write(
                self.format.format(
                    name=self.name,
                    error=error,
                    pid=os.getpid(),
                    level="ERROR",
                    ppid=os.getppid(),
                    msg=info,
                    asctime=time.asctime(),
                )
            )
            self.file.flush()

    def warning(self, info, error=None):
        if self.conf["warning"]:
            self.file.write(
                self.format.format(
                    name=self.name,
                    error=error,
                    pid=os.getpid(),
                    level="WARNING",
                    ppid=os.getppid(),
                    msg=info,
                    asctime=time.asctime(),
                )
            )
            self.file.flush()
