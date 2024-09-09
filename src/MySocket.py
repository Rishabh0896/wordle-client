import socket


class MySocket:
    """
    Socket class
    """

    def __init__(self, sock=None):
        self.buffer_size = 1024
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def connect_with_tls(self, host, port):
        # TODO
        pass

    def send_msg(self, msg):
        sent = self.sock.send(msg)
        if sent == 0:
            raise RuntimeError("socket connection broken")

    def recv_msg(self):
        self.buffer_size = 1024
        chunks = []

        while True:
            part = self.sock.recv(self.buffer_size)
            if not part:
                # Connection closed
                break
            chunks.append(part)
            if b'\n' in part:
                # This would tell us when to close the connection and stop receiving
                break

        return b''.join(chunks).decode('ascii')
