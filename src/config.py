import logging
import os


class Config:
    """
    Configuration class for the Wordle game client.

    This class manages all configuration settings for the game, including network settings,
    game parameters, and logging configurations. It uses environment variables with default
    values to allow for easy configuration changes without modifying the code.

    Attributes:
        DEFAULT_PORT (int): The default port for non-TLS connections.
        TLS_PORT (int): The default port for TLS connections.
        MAX_RETRIES (int): Maximum number of retry attempts for game operations.
        INITIAL_GUESS (str): The initial guess word for the Wordle game.
        BUFFER_SIZE (int): Size of the buffer for network operations.
        LOG_LEVEL (str): The logging level for the application.
        LOG_FILE (str): The file path for logging.
        DEFAULT_ENCODING (str): The default character encoding for string operations.
    """

    DEFAULT_PORT: int = int(os.getenv('DEFAULT_PORT', 27993))
    TLS_PORT: int = int(os.getenv('TLS_PORT', 27994))
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', 500))
    INITIAL_GUESS: str = os.getenv('INITIAL_GUESS', "salet")
    BUFFER_SIZE: int = int(os.getenv('BUFFER_SIZE', 1024))
    LOG_LEVEL: int = int(os.getenv('LOG_LEVEL', logging.WARN))
    LOG_FILE: str = os.getenv('LOG_FILE', 'wordle_solver.log')
    DEFAULT_ENCODING: str = 'ascii'
