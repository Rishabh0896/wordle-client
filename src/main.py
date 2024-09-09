from src.MySocket import MySocket
import argparse


def _happy_test(self):
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("proj1.4700.network", 27993))

    s.send(b'{"type": "hello", "northeastern_username": "gupta.risha" }\n')

    buffer_size = 1024
    msg_parts = []

    while True:
        part = s.recv(buffer_size)
        if not part:
            # Connection closed
            break
        msg_parts.append(part)
        if b'\n' in part:
            # This would tell us when to close the connection and stop receiving
            break

    msg = b''.join(msg_parts)
    msg = msg.decode("ascii")
    print(msg)



