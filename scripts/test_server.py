#  Copyright (c) 2020 Xcodz.
#  All Rights Reserved.

import socket
import argparse
import secrets

if __name__ == "__main__":
    parser = argparse.ArgumentParser("test server")
    parser.add_argument("-a", "--ip", action="store", help="Ip Adress for test hosting", required=False,
                        default="127.0.0.1")
    parser.add_argument("-p", "--port", action="store", help="Port for test hosting", required=False, default=3000,
                        type=int)
    args = parser.parse_args()

    s = socket.socket()
    s.bind((args.ip, args.port))
    s.listen(5)

    while True:
        c, addr = s.accept()
        print(d := c.recv(1000))
        if d == b'bytes_token':
            c.sendall(secrets.token_bytes(100))
        if d == b"status":
            c.sendall(b"working")
        c.close()
