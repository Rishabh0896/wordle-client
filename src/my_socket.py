import socket
import ssl

from src.config import Config


class MySocket:
    """
    A custom socket class that handles both standard and TLS-encrypted connections.

    This class provides a simplified interface for creating a socket connection,
    sending messages, and receiving responses. It supports both regular TCP
    connections and TLS-encrypted connections.
    """

    def __init__(self):
        """
        Initialize the MySocket instance.

        The socket object (self.sock) is initially set to None and will be
        created when the connect method is called.
        """
        self.sock = None

    def connect(self, host, port, use_tls=False):
        """
        Establish a connection to the specified host and port.

        Args:
            host (str): The hostname or IP address to connect to.
            port (int): The port number to connect to.
            use_tls (bool): Whether to use TLS encryption for the connection.

        Raises:
            ConnectionError: If the connection attempt fails.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if use_tls:
            context = ssl.create_default_context()
            self.sock = context.wrap_socket(self.sock, server_hostname=host)
        try:
            self.sock.connect((host, port))
        except (ssl.SSLError, socket.error) as e:
            raise ConnectionError(f"Failed to connect to {host}:{port}. Error: {e}")

    def send_msg(self, msg):
        """
        Send a message through the socket.

        Args:
            msg (bytes): The message to send.

        Raises:
            RuntimeError: If the socket is not connected or if the send operation fails.
        """
        if not self.sock:
            raise RuntimeError("Socket is not connected")
        sent = self.sock.send(msg)
        if sent == 0:
            raise RuntimeError("Socket connection broken")

    def recv_msg(self):
        """
        Receive a message from the socket.

        This method reads data from the socket until a newline character is
        encountered or the connection is closed.

        Returns:
            str: The received message, decoded using the default encoding.

        Raises:
            RuntimeError: If the socket is not connected.
        """
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
