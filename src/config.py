import os


class Config:
    # Network settings
    DEFAULT_PORT = int(os.getenv('DEFAULT_PORT', 27993))
    TLS_PORT = int(os.getenv('TLS_PORT', 27994))

    # Game settings
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 500))

    # Other constants
    BUFFER_SIZE = int(os.getenv('BUFFER_SIZE', 1024))

    @classmethod
    def get_port(cls, use_tls=False):
        return cls.TLS_PORT if use_tls else cls.DEFAULT_PORT
