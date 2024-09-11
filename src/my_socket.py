import socket
import ssl

from src.config import Config


class MySocket:
    """
    Socket class
    """

    def __init__(self):
        self.sock = None

    def connect(self, host, port, use_tls=False):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if use_tls:
            context = ssl.create_default_context()
            self.sock = context.wrap_socket(self.sock, server_hostname=host)
        try:
            self.sock.connect((host, port))
        except (ssl.SSLError, socket.error) as e:
            raise ConnectionError(f"Failed to connect to {host}:{port}. Error: {e}")

    def send_msg(self, msg):
        if not self.sock:
            raise RuntimeError("Socket is not connected")
        sent = self.sock.send(msg)
        if sent == 0:
            raise RuntimeError("Socket connection broken")

    def recv_msg(self):
        if not self.sock:
            raise RuntimeError("Socket is not connected")
        chunks = []
        while True:
            part = self.sock.recv(Config.BUFFER_SIZE)
            if not part:
                # Connection closed
                break
            chunks.append(part)
            if b'\n' in part:
                # This would tell us when to close the connection and stop receiving
                break

        return b''.join(chunks).decode(Config.DEFAULT_ENCODING)
