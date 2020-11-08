import functools
import argparse
import sys
try:
    from . import ctext
except ImportError:
    import ctext

print = ctext.print
input = ctext.input


# noinspection PyCallByClass
class BuildTasks:
    def __init__(self):
        self.ignored_tasks = []
        self.accomplished = []
        self.tasks = []

    def task(self, *dependencies, forced=False, ignored=False, uses_commandline=False):
        def decorator(function):
            @functools.wraps(function)
            def wrapper_function(arguments=None):
                print(f'-------------{function.__name__}-------------', fore="green")
                for x in dependencies:
                    if x not in self.accomplished:
                        print(f"Running Task {x.__name__} (from {function.__name__})", fore="magenta")
                        if x not in self.ignored_tasks:
                            self.accomplished.append(x)
                        if not uses_commandline:
                            x()
                        else:
                            x(arguments)
                    else:
                        print(f"Skipped Task {x.__name__} (from {function.__name__})", fore="cyan")
                function()
                print(ctext.ColoredText.escape(
                    f"{{fore_yellow}}----{{back_red}}end{{reset_all}}{{style_bright}}{{fore_yellow}}------{function.__name__}-------------"
                ))

            if forced:
                self.ignored_tasks.append(wrapper_function)

            if not ignored:
                self.tasks.append(wrapper_function)

            return wrapper_function

        return decorator

    def interact(self, arguments=None):
        if arguments is None:
            arguments = sys.argv[1:]
        parser = argparse.ArgumentParser()
        parser.add_argument("sub_arguments", nargs="*", default=[])
        command = parser.add_subparsers(dest="command_")
        for x in self.tasks:
            command.add_parser(x.__name__, description=x.__doc__)
        args = parser.parse_args(arguments)
        for x in self.tasks:
            if args.command_ == x.__name__:
                x(args.sub_arguments)


auto = BuildTasks()


@auto.task()
def build_app():
    print("Building App")


@auto.task(build_app)
def package_wheel():
    print("Making Python Wheel")


@auto.task(build_app)
def package_source():
    print("Packaging Source")


@auto.task()
def cleanup():
    print("Cleaning Up")


@auto.task(package_wheel, package_source, cleanup)
def build_all():
    print("Building All")


if __name__ == "__main__":
    auto.interact()
