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
            print("Tried to connect to " + host + ":" + str(port))
            self.sock.connect((host, port))
        except ssl.SSLError as e:
            print(f"SSL error: {e}")
            raise
        except Exception as e:
            print(f"Exception: {e}")
            raise

    def send_msg(self, msg):
        sent = self.sock.send(msg)
        if sent == 0:
            raise RuntimeError("socket connection broken")

    def recv_msg(self):
        chunks = []

        while True:
            part = self.sock.recv(Config.BUFFER_SIZE)
            if not part:
                # Connection closed
                print("socket connection closed while receiving response")
                break
            chunks.append(part)
            if b'\n' in part:
                # This would tell us when to close the connection and stop receiving
                break

        return b''.join(chunks).decode('ascii')
