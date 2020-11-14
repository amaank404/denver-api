"""
This module uses bdtp for files hosting
using a single connection method with speed
ranging up to 2.0 MB/s or more if computer have
good powered CPU
"""

__version__ = "2020.6.4"
__author__ = "Xcodz"

import socket
import threading
import pickle
import os
from . import bdtp


def get(file: str, addr: tuple):
    assert type(file) == str or type(addr) == tuple, "Invalid Parameter Types"
    request = pickle.dumps(["get", file])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.sendall(request)
    data = bdtp.new_receive_data_port(("", 0))
    data.recv(s)
    data = data.data
    s.close()
    return data


def post(file: str, data: bytes, addr: tuple):
    assert (
        type(file) == str or type(addr) == tuple or type(data) == bytes
    ), "Invalid Parameter Types"
    request = pickle.dumps(["post", file])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.sendall(request)
    s.recv(1)
    data = bdtp.new_send_data_port(data, ("", 0))
    data.send(s)
    s.close()


def mkdir(name: str, addr: tuple):
    assert type(name) == str or type(addr) == tuple
    request = pickle.dumps(["mkdir", name])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.sendall(request)
    s.close()


def handle_request(connection: socket.socket, addr: tuple, hdir: str, shdir: str):
    req = pickle.loads(connection.recv(1000))
    if req[0] == "get":
        print(f'{addr} requested to get "{req[1]}"')
        try:
            data = open(os.path.join(hdir, req[1].replace("/", os.sep)), "r+b").read()
            d = bdtp.new_send_data_host(data, ("", 0))
            d.send(connection)
        except Exception as e:
            print(f"{addr} get request failed: {str(e)}")
    elif req[0] == "mkdir":
        print(f'{addr} requested to mkdir "{req[1]}"')
        try:
            os.mkdir(os.path.join(hdir, req[1].replace("/", os.sep)))
        except Exception as e:
            print(f"{addr} mkdir request failed: {str(e)}")
    elif req[0] == "listdir":
        print(f'{addr} requested to listdir "{req[1]}"')
        try:
            r = pickle.dumps(
                os.listdir(os.path.join(hdir, req[1].replace("/", os.sep)))
            )
            d = bdtp.new_send_data_host(r, ("", 0))
            d.send(connection)
        except Exception as e:
            print(f"{addr} listdir request failed: {str(e)}")
    elif req[0] == "post":
        print(f'{addr} requested to post "{req[1]}"')
        try:
            connection.sendall(b" ")
            d = bdtp.new_receive_data_host(("", 0))
            d.recv(connection)
            f = open(os.path.join(hdir, shdir, req[1].replace("/", os.sep)), "w+b")
            f.write(d.data)
            f.close()
            print(f"{addr} post request successful")
        except Exception as e:
            print(f"{addr} post request failed: {str(e)}")
    connection.close()


def listdir(dir_name: str, addr: tuple):
    if dir_name == "":
        dir_name = "."
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.sendall(pickle.dumps(["listdir", dir_name]))
    d = bdtp.new_receive_data_port(("", 0))
    d.recv(s)
    s.close()
    return pickle.loads(d.data)


def host(home_dir: str, addr: tuple, subdir_post: str = None):
    if subdir_post is None:
        subdir_post = home_dir
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen(5)
    while True:
        c, addr = s.accept()
        threading.Thread(
            target=handle_request, args=(c, addr, home_dir, subdir_post)
        ).start()
