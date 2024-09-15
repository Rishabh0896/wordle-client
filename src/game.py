import json
import logging
import sys
from collections import Counter
from typing import List, Set, Dict
from src.config import Config


class Game:
    """
    A class to represent and solve a Wordle game.

    This class implements the logic for playing and solving a Wordle game,
    including maintaining game state, processing guesses, and determining
    the next best guess based on current information.

    Attributes:
        sock: The socket connection to the game server.
        username (str): The username for the game.
        game_id (str): The unique identifier for the current game.
        word_list (List[str]): A list of all possible Wordle words.
        possible_words (Set[str]): The set of words that are still possible solutions.
        must_contain (Set[str]): Set of letters that must be in the solution.
        position_constraints (List[Set[str]]): Constraints for each position in the word.
        logger (logging.Logger): Logger for the game.
    """
    def __init__(self, sock, username: str, log_level: int = logging.DEBUG):
        self.sock = sock
        self.username = username
        self.game_id = ""
        self.word_list = self._load_word_list()
        self.possible_words = set(self.word_list)
        self.must_contain: Set[str] = set()
        self.position_constraints: List[Set[str]] = [set('abcdefghijklmnopqrstuvwxyz') for _ in range(5)]
        self.logger = self._setup_logger(log_level)

    def _setup_logger(self, level: int = logging.DEBUG) -> logging.Logger:
        """
        Set up and configure the logger.

        Args:
            level (int): The logging level.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger('App')
        logger.setLevel(level)
        file_handler = logging.FileHandler(Config.LOG_FILE, 'w')
        file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    @staticmethod
    def _load_word_list() -> List[str]:
        """
        Load the word list from a file.

        Returns:
            List[str]: List of words loaded from the file.
        """
        with open('word_list.txt', 'r') as f:
            return [word.strip() for word in f]

    def start_game(self) -> None:
        """
        Start and play the Wordle game until completion.
        """
        self._send_recv_hello_message()
        guess = self._get_initial_guess()

        while True:
            response = self._guess_word(word=guess)
            if response["type"] == "bye":
                print(response["flag"])
                self.sock.disconnect()  # Close the connection
                break
            guess = self._get_next_guess(response)

    def _get_next_guess(self, response: Dict) -> str:
        """
        Determine the next guess based on the game's response.

        Args:
            response (Dict): The game's response to the previous guess.

        Returns:
            str: The next word to guess.
        """
        last_guess = response["guesses"][-1]
        marks = last_guess["marks"]
        guess = last_guess["word"]

        self.logger.info(f"Processing guess: {guess} with marks: {marks}")
        self._update_constraints(guess, marks)
        self._filter_possible_words()

        if len(self.possible_words) <= 2:
            next_guess = next(iter(self.possible_words))
            self.logger.info(f"Only {len(self.possible_words)} words left. Choosing {next_guess}")
            return next_guess

        next_guess = self._choose_best_guess()
        self.logger.info(f"Chose next guess: {next_guess} based on letter frequency")
        return next_guess

    def _update_constraints(self, guess: str, marks: List[int]) -> None:
        """
        Update the game constraints based on the latest guess and its marks.

        Args:
            guess (str): The last guessed word.
            marks (List[int]): The marks received for the last guess.
        """
        for i, (letter, mark) in enumerate(zip(guess, marks)):
            if mark == 2:  # Correct letter and position
                self.position_constraints[i] = {letter}
                self.must_contain.add(letter)
            elif mark == 1:  # Correct letter, wrong position
                self.position_constraints[i].discard(letter)
                self.must_contain.add(letter)
            elif mark == 0:  # Letter not in word
                self.position_constraints[i].discard(letter)

        self._log_current_state(guess)

    def _log_current_state(self, guess: str) -> None:
        """
        Log the current state of the game after processing a guess.

        Args:
            guess (str): The last guessed word.
        """
        self.logger.info(f"Current state after processing guess {guess}:")
        self.logger.info(f"Must contain letters: {self.must_contain}")
        for i, constraint in enumerate(self.position_constraints):
            self.logger.info(f"Position {i} can have letters: {constraint}")

    def _filter_possible_words(self) -> None:
        """
        Filter the possible words based on current constraints.
        """
        old_possible_words = set(self.possible_words)
        self.possible_words = {
            word for word in self.possible_words
            if all(letter in word for letter in self.must_contain) and
               all(word[i] in constraint for i, constraint in enumerate(self.position_constraints))
        }
        removed_words = old_possible_words - self.possible_words
        self.logger.debug(f"Removed words: {removed_words}")

        if not self.possible_words:
            self.logger.error("No possible words left! Current constraints may be too restrictive.")

    def _choose_best_guess(self) -> str:
        """
        Choose the best next guess based on letter frequency.

        Returns:
            str: The best word to guess next.
        """
        letter_freq = Counter(letter for word in self.possible_words for letter in set(word))
        return max(self.possible_words, key=lambda word: sum(letter_freq[letter] for letter in set(word)))

    def _send_recv_hello_message(self) -> None:
        """
        Send a hello message to the game server and receive the game ID.
        If an error occurs, close the connection and exit the program.
        """
        try:
            msg = json.dumps({"type": "hello", "northeastern_username": self.username}) + '\n'
            encoded_msg = msg.encode(Config.DEFAULT_ENCODING)
            self.sock.send_msg(encoded_msg)
            msg_recv = self.sock.recv_msg()
            response_dict = json.loads(msg_recv)

            if response_dict['type'] == "error":
                print(f"Error from server: {response_dict['message']}")
                raise ValueError(response_dict['message'])

            self.game_id = response_dict['id']

        except ValueError as e:
            print(f"Error returned from server : {str(e)}")
            self.sock.disconnect()
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error occurred: {str(e)}")
            self.sock.disconnect()
            sys.exit(1)

    def _guess_word(self, word: str = "salet") -> Dict:
        msg = json.dumps({"type": "guess", "id": self.game_id, "word": word}) + '\n'
        encoded_msg = msg.encode(Config.DEFAULT_ENCODING)
        self.sock.send_msg(encoded_msg)
        msg_recv = self.sock.recv_msg()
        return json.loads(msg_recv)

    def _get_initial_guess(self):
        """
        Get the initial guess for the game.

        Returns:
            str: The initial guess word.
        """
        return Config.INITIAL_GUESS
