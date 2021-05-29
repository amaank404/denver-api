"""
##Big Data Transfer Protocol
###What does it do

This protocol sends big data on a address (IPv4,port)
without worrying about pipe errors.
"""

__author__ = "Xcodz"
__version__ = "2021.2.24"

import abc
import socket
import time
import typing

from . import thread_control

default_buffer_size = 100000


class _BaseSender(abc.ABC):
    @abc.abstractmethod
    def send(self, c):
        pass


class _BaseReceiver(abc.ABC):
    @abc.abstractmethod
    def recv(self, c):
        pass


class DataSenderHost(_BaseSender):
    """
    it is used for sending data as a host or in other words, server

    to create a new DataSenderHost please use function implementation for it
    """

    def __init__(self):
        self.data = b""
        self.address: tuple = ("", 0)
        self.data_send: int = 0
        self.buffer_size: int = default_buffer_size
        self.task = False

    def send(self, connected_socket: socket.socket = None):
        """
        use this function to initiate the connection and send the data. `connected_socket` can be
        supplied if you want to send over a already connected socket.
        """
        if connected_socket is None:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(self.address)
            s.listen(5)
            connection, _ = s.accept()
        else:
            connection = connected_socket

        if isinstance(self.data, bytes):
            for line in range(0, len(self.data), self.buffer_size):
                lts = self.data[line : line + self.buffer_size]
                connection.sendall(lts)
                self.data_send += self.buffer_size
        elif isinstance(self.data, typing.BinaryIO):
            while True:
                line = self.data.read(self.buffer_size)
                if line == b"":
                    break
                connection.sendall(line)
                self.data_send += self.buffer_size

        connection.send(b"")
        if connected_socket is None:
            connection.close()
            s.close()
        self.task = True


class DataSenderPort(_BaseSender):
    """
    it is used for sending data as a client

    to create a new DataSenderPort please use function implementation for it
    """

    def __init__(self):
        self.data: bytes = b""
        self.address: tuple = ("", 0)
        self.data_send: int = 0
        self.buffer_size: int = default_buffer_size
        self.task = False

    def send(self, connected_socket: socket.socket = None):
        """
        use this function to initiate the connection and send the data. `connected_socket` can be
        supplied if you want to send over a already connected socket.
        """
        if connected_socket is None:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(self.address)
        else:
            s = connected_socket

        if isinstance(self.data, bytes):
            for x in range(0, len(self.data), self.buffer_size):
                lts = self.data[x : x + self.buffer_size]
                s.sendall(lts)
                self.data_send += self.buffer_size
        elif isinstance(self.data, typing.BinaryIO):
            while True:
                line = self.data.read(self.buffer_size)
                if line == b"":
                    break
                s.sendall(line)
                self.data_send += self.buffer_size

        s.send(b"")
        if connected_socket is None:
            s.close()
        self.task = True


class DataReceiverHost(_BaseReceiver):
    """
    it is used for receiving data as a server or host

    to create a new DataReceiverHost please use function implementation for it
    """

    def __init__(self):
        self.address: tuple = ("", 0)
        self.data_recv: int = 0
        self.buffer_size: int = default_buffer_size
        self.data = b""
        self.task = False

    def recv(self, connected_socket: socket.socket = None):
        """
        use this function to initiate the connection and start receiving the data. `connected_socket` can be
        supplied if you want to receive over a already connected socket.
        """
        if connected_socket is None:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(self.address)
            s.listen(5)
            connection, _ = s.accept()
        else:
            connection = connected_socket
        recv_bytes = b"\0"

        while recv_bytes != b"":
            recv_bytes = connection.recv(self.buffer_size)
            self.data += recv_bytes
            self.data_recv += self.buffer_size

        if connected_socket is None:
            connection.close()
            s.close()
        self.task = True


class DataReceiverPort(_BaseReceiver):
    """
    it is used for receiving data as a client

    to create a new DataReceiverPort please use function implementation for it
    """

    def __init__(self):
        self.address: tuple = ("", 0)
        self.data_recv: int = 0
        self.buffer_size: int = default_buffer_size
        self.data = b""
        self.task = False

    def recv(self, connected_socket: socket.socket = None):
        """
        use this function to initiate the connection and start receiving the data. `connected_socket` can be
        supplied if you want to receive over a already connected socket.
        """
        if connected_socket is None:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(self.address)
            connection = s
        else:
            connection = connected_socket
        recv_bytes = b"\0"

        while recv_bytes != b"":
            recv_bytes = connection.recv(self.buffer_size)
            self.data += recv_bytes
            self.data_recv += self.buffer_size

        if connected_socket is None:
            connection.close()
        self.task = True


def new_send_data_host(data: bytes, addr: tuple = None, buffer_size=None):
    """
    Make a new `DataSenderHost` with provided arguments. It's better to not supply `addr` if you
    are going to use the object on existing connection. It is also not recommended to change
    `buffer_size` because this argument is supposed to be same at both the sender and receiver.

    You can then use the `send` method of the returned object to send the provided data.

    Example:

    ```python
    from denverapi import bdtp
    import socket

    # Without existing connection
    my_sender = bdtp.new_send_data_host(b"Some Data", ("127.0.0.1", 7575))
    my_sender.send()

    # With existing connection
    my_server = socket.socket()
    my_server.bind(("127.0.0.1", 1234))
    my_server.listen(5)

    my_connection, address = my_server.accept()

    my_sender = bdtp.new_send_data_host(b"Some Data")
    my_sender.send(my_connection)

    # With changed buffer size
    my_sender = bdtp.new_send_data_host(b"Some Data", ("127.0.0.1", 12345), 3)
    my_sender.send()
    ```
    """
    sender_object = DataSenderHost()
    sender_object.data = data
    sender_object.address = addr
    if buffer_size is not None:
        sender_object.buffer_size = buffer_size
    return sender_object


def new_send_data_port(data: bytes, addr: tuple = None, buffer_size=None):
    """
    Make a new `DataSenderPort` with provided arguments. It's better to not supply `addr` if you
    are going to use the object on existing connection. It is also not recommended to change
    `buffer_size` because this argument is supposed to be same at both the sender and receiver.

    You can then use the `send` method of the returned object to send the provided data.

    Example:

    ```python
    from denverapi import bdtp
    import socket

    # Without existing connection
    my_sender = bdtp.new_send_data_port(b"Some Data", ("127.0.0.1", 7575))
    my_sender.send()

    # With existing connection
    my_connection = socket.socket()
    my_connection.connect(("127.0.0.1", 1234))
    my_sender = bdtp.new_send_data_port(b"Some Data")
    my_sender.send(my_connection)

    # With changed buffer size
    my_sender = bdtp.new_send_data_host(b"Some Data", ("127.0.0.1", 12345), 3)
    my_sender.send()
    ```
    """
    sender_object = DataSenderPort()
    sender_object.data = data
    sender_object.address = addr
    if buffer_size is not None:
        sender_object.buffer_size = buffer_size
    return sender_object


def new_receive_data_host(addr: tuple = None, buffer_size=None):
    """
    Make a new `DataReceiverHost` object to receive data sent by sender. It is not recommended to
    supply `addr` if you are going to use it with existing connection. It is highly discouraged to use
    `buffer_size` argument as it is supposed to be kept same at both sender and receiver.

    You can use the returned object's `recv` method to start receiving data. Once receiving is complete.
    data will be stored in object's `data` attribute as bytes.

    ```python
    from denverapi import bdtp
    import socket

    # Without existing connection
    my_receiver = bdtp.new_receive_data_host(("127.0.0.1", 7575))
    my_receiver.recv()

    # With existing connection
    my_connection = socket.socket()
    my_connection.connect(("127.0.0.1", 1234))
    my_receiver = bdtp.new_receive_data_host()
    my_receiver.recv(my_connection)

    # With changed buffer size
    my_receiver = bdtp.new_receive_data_host(("127.0.0.1", 12345), 3)
    my_receiver.recv()
    ```
    """
    sender_object = DataReceiverHost()
    sender_object.address = addr
    if buffer_size is not None:
        sender_object.buffer_size = buffer_size
    return sender_object


def new_receive_data_port(addr: tuple, buffer_size=None):
    """
    Make a new `DataReceiverHost` object to receive data sent by sender. It is not recommended to
    supply `addr` if you are going to use it with existing connection. It is highly discouraged to use
    `buffer_size` argument as it is supposed to be kept same at both sender and receiver.

    You can use the returned object's `recv` method to start receiving data. Once receiving is complete.
    data will be stored in object's `data` attribute as bytes.

    ```python
    from denverapi import bdtp
    import socket

    # Without existing connection
    my_receiver = bdtp.new_receive_data_port(("127.0.0.1", 7575))
    my_receiver.recv()

    # With existing connection
    my_connection = socket.socket()
    my_connection.connect(("127.0.0.1", 1234))
    my_receiver = bdtp.new_receive_data_port()
    my_receiver.recv(my_connection)

    # With changed buffer size
    my_receiver = bdtp.new_receive_data_port(("127.0.0.1", 12345), 3)
    my_receiver.recv()
    ```
    """
    sender_object = DataReceiverPort()
    sender_object.address = addr
    if buffer_size is not None:
        sender_object.buffer_size = buffer_size
    return sender_object


def attach_speed_logger(data_object) -> typing.List[int]:
    """
    Attaches a speed logger that captures the speed of transfer for either receiver object
    or sender object. Returns a list that gets updated as the speed transfer continues.
    To get the average speed use `average_speed_log`.

    Example:

    ```python
    from denverapi import bdtp

    sender = bdtp.new_receive_data_port(b"Hello World"*10000, ("localhost", 8000))
    speed_log = bdtp.attach_speed_logger(sender)
    sender.send()

    speed = bdtp.average_speed_log(speed_log)
    ```
    """
    spl = []

    @thread_control.runs_parallel
    def sps(spl, d: _BaseSender):
        old = 0
        new = 0
        spl.append(d.buffer_size)
        while not d.task:
            time.sleep(0.01)
            new = d.data_send
            spl.append(new - old)
            old = new

    @thread_control.runs_parallel
    def spr(spl, d: _BaseReceiver):
        old = 0
        new = 0
        spl.append(d.buffer_size)
        while not d.task:
            time.sleep(0.01)
            new = d.data_recv
            spl.append(new - old)
            old = new

    (spr if isinstance(data_object, _BaseReceiver) else sps)(spl, data_object)
    return spl


def launch(data_object, connected_socket=None):
    """
    Just a simple function that starts a sender or receiver object. It is here because it looks good when using this.
    """
    if isinstance(data_object, _BaseSender):
        data_object.send(connected_socket)
    else:
        data_object.recv(connected_socket)


def average_speed_log(spl: list) -> int:
    """
    Finds average speed of the connection.
    It strips out 0 from the end and starting of `spl` and then finds the average and returns it
    """
    while spl[0] == 0:
        spl.pop(0)
    while spl[-1] == 0:
        spl.pop()
    return (sum(spl) / len(spl)) * 100


def main():
    """
    Nothing more than a test
    """
    print("Reading Data")
    datats = open(input("File > "), "r+b").read()
    print("Read Data")
    print("Making Classes")
    sc = new_send_data_port(datats, ("127.0.0.1", 4623))
    rc = new_receive_data_host(("127.0.0.1", 4623))
    spl = attach_speed_logger(rc)
    from threading import Thread

    Thread(target=launch, args=(sc,)).start()
    rc.recv()
    print(len(spl))
    print(
        f"Data Send:\n\tlen: {len(sc.data)}\nData Received:\n\tlen: {len(rc.data)}\n\tis_equal: {rc.data == sc.data}"
    )
    print(f"Average Speed: {average_speed_log(spl)} bytes per second")


if __name__ == "__main__":
    main()
