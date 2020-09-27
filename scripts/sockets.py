#  Copyright (c) 2020 Xcodz.
#  All Rights Reserved.
import socket
import denver.bcli
import denver.bdtp
import argparse
import version_info

version_stat = f"Sockets {version_info.build_platform} [{version_info.build_version}]({version_info.build_time})"


class Script:
    def __init__(self, interactive=True):
        self.sockets = {}
        self.interactive = interactive
        self.cli = denver.bcli.new_cli()

    def print_var(self, name):
        if self.interactive:
            exec(f"self.cli.run(self.{name})")

    def print(self, value):
        self.cli.run(value)

    def target(self, name, target, connection_type="socket.AF_INET", connection_type2="socket.SOCK_STREAM"):
        self.sockets[name] = (socket.socket(eval(connection_type), eval(connection_type2)), eval(target))
        if self.interactive:
            self.cli.info(f"{{target}} target '{name}', address '{target}', connection_medium '{connection_type}', "
                          f"connection_type '{connection_type2}'")

    def connect(self, name):
        self.sockets[name][0].connect(self.sockets[name][1])
        if self.interactive:
            self.cli.good(f"{{connect}} target '{name}'")

    def send(self, name, data):
        self.sockets[name][0].sendall(eval(data))
        if self.interactive:
            self.cli.good(f"{{send}} data_size '{len(data)}'")

    def recv(self, name, variable, length):
        data = self.sockets[name][0].recv(int(length))
        exec(f"self.{variable} = {data}")
        if self.interactive:
            self.cli.good(f"{{recv}} buffer_length '{length}' data_size '{len(data)}' variable '{variable}'")

    def close(self, name):
        self.sockets[name][0].close()
        if self.interactive:
            self.cli.info(f"{{close}} target {name}")


def run_script(script: str, interactive: bool = True):
    script_instance = Script(interactive)
    parsed_script = compile_script(script)
    for command, args in parsed_script:
        # noinspection PyBroadException
        try:
            exec(f"script_instance.{command}(*args)")
        except NameError:
            script_instance.cli.bad(f"{command}: Failed, No such command")
        except Exception as e:
            script_instance.cli.bad(f"{command}: Failed with exception [{str(e)}]")


def purify_line(script: list):
    d = len(script)
    for x in range(0, d, 2):
        script[x] = None
    while None in script:
        script.remove(None)
    return script


def compile_script(script: str):
    mode = "c"
    lines = []
    cname = ""
    args = []
    argtemp = ""
    xi = 0
    started = False
    while True:
        try:
            x = script[xi]
        except IndexError:
            break
        xi += 1
        if mode == "c":
            if x not in " ;\n":
                cname += x
            elif x == ' ':
                mode = "a"
            elif x == "\n":
                pass
            elif x == ';':
                lines.append((cname, []))
                cname = ''
        if mode == "a":
            if x in "\\` ;\n":
                if x == "\\":
                    xi += 1
                    x = script[xi]
                    argtemp += x
                elif x == "\n":
                    if started:
                        argtemp += "\n"
                elif x == " ":
                    if started:
                        argtemp += ' '
                    else:
                        args.append(argtemp)
                        argtemp = ''
                elif x == ";":
                    if not started:
                        lines.append((cname, purify_line(args)))
                        cname = ''
                        args = []
                        argtemp = ''
                        mode = "c"
                    else:
                        argtemp += ';'
                else:
                    if started:
                        args.append(argtemp)
                        argtemp = ''
                    started = not started
            else:
                argtemp += x
    return lines


def interactive_session():
    print(version_stat)
    script_instance = Script(interactive=True)
    while True:
        try:
            parsed_script = compile_script(script_instance.cli.input(">"))
        except KeyboardInterrupt:
            print()
            script_instance.cli.bad("Session aborted")
            raise SystemExit(0)
        for command, args in parsed_script:
            # noinspection PyBroadException
            try:
                exec(f"script_instance.{command}(*args)")
            except NameError:
                script_instance.cli.bad(f"{command}: Failed, No such command")
            except Exception as e:
                script_instance.cli.bad(f"{command}: Failed with exception [{str(e)}]")


def main():
    parser = argparse.ArgumentParser("Sockets",
                                     description="Sockets program for scripting client socket program, supports "
                                                 "Denver BDTP")

    parser.add_argument("script", default=None, nargs="?", help="Provide a script to run, by default it is"
                                                                " interactive mode")
    parser.add_argument("-ni", "--not-interactive", action="store_false", help="Switches off Interactive Mode")
    args = parser.parse_args()
    if args.script is None:
        interactive_session()
    else:
        with open(args.script, "r") as f:
            script = f.read()
        run_script(script, interactive=args.not_interactive)


if __name__ == '__main__':
    main()
