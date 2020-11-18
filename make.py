from denverapi.autopyb import *

auto = BuildTasks()

# Information
requires_version("1.1.0")


@auto.task()
def develop():
    pass
