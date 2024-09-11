import json
import logging
import traceback
from collections import defaultdict, Counter


class Game:

    def __init__(self, sock, username, log_level):
        self.sock = sock
        self.username = username
        self.game_id = ""
        self.word_list = self.load_word_list()
        self.possible_words = set(self.word_list)

        # Initialize constraints
        self.must_contain = set()
        self.position_constraints = [set('abcdefghijklmnopqrstuvwxyz') for _ in range(5)]

        self.logger = self.setup_logger(log_level)

    def setup_logger(self, level=logging.DEBUG):
        logger = logging.getLogger('WordleSolver')
        logger.setLevel(level)
        fh = logging.FileHandler('../wordle_solver.log', 'w')
        fh.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def load_word_list(self):
        # Load words from file
        with open('word_list.txt', 'r') as f:
            return [word.strip() for word in f]

    def start_game(self):
        # Send the first hello message
        self.send_recv_hello_message()

        # Play game
        guess = "salet"
        tries = 1

        while True:
            tries += 1
            response = self.guess_word(word=guess)
            message_type = response["type"]
            if message_type == "bye":
                break
            guess = self.get_next_guess(response)

    def get_next_guess(self, response):
        last_guess = response["guesses"][-1]
        marks = last_guess["marks"]
        guess = last_guess["word"]

        self.logger.info(f"Processing guess: {guess} with marks: {marks}")
        # Process feedback
        for i, (letter, mark) in enumerate(zip(guess, marks)):
            if mark == 2:  # Correct letter and position
                self.position_constraints[i] = {letter}
                self.must_contain.add(letter)
                self.logger.info(f"Position {i} can have letters: {self.position_constraints[i]}")
            elif mark == 1:  # Correct letter, wrong position
                self.position_constraints[i].discard(letter)
                self.must_contain.add(letter)
                self.logger.debug(f"Letter {letter} is in the word but not at position {i}")
            elif mark == 0:  # Letter not in word
                self.position_constraints[i].discard(letter)

        # Log current state
        self.logger.info(f"Current state after processing guess {guess}:")
        self.logger.info(f"Must contain letters: {self.must_contain}")
        for i in range(len(self.position_constraints)):
            self.logger.info(f"Position {i} can have letters: {self.position_constraints[i]}")

        # Filter possible words
        old_possible_words = set(self.possible_words)
        self.possible_words = {
            word for word in self.possible_words
            if all(letter in word for letter in self.must_contain) and
               all(word[i] in constraint for i, constraint in enumerate(self.position_constraints))
        }
        removed_words = old_possible_words - self.possible_words
        self.logger.debug(f"Removed words: {removed_words}")

        if len(self.possible_words) == 0:
            self.logger.error(f"No possible words left! Response: {response}")
            self.logger.error("Current constraints may be too restrictive. Consider relaxing constraints.")

        try:
            if len(self.possible_words) <= 2:
                next_guess = next(iter(self.possible_words))
                self.logger.info(f"Only {len(self.possible_words)} words left. Choosing {next_guess}")
                return next_guess
        except Exception as e:
            traceback.print_exc()

        # Use letter frequency for scoring
        letter_freq = Counter(letter for word in self.possible_words for letter in set(word))
        next_guess = max(self.possible_words, key=lambda word: sum(letter_freq[letter] for letter in set(word)))
        self.logger.info(f"Chose next guess: {next_guess} based on letter frequency")
        return next_guess

    def send_recv_hello_message(self):
        msg = json.dumps({"type": "hello", "northeastern_username": self.username}) + '\n'
        encoded_msg = msg.encode('ascii')
        self.sock.send_msg(encoded_msg)
        msg_recv = self.sock.recv_msg()
        response_dict = json.loads(msg_recv)
        self.game_id = response_dict['id']

    def guess_word(self, word="salet"):
        msg = json.dumps({"type": "guess", "id": self.game_id, "word": word}) + '\n'
        encoded_msg = msg.encode('ascii')
        self.sock.send_msg(encoded_msg)
        msg_recv = self.sock.recv_msg()
        response_dict = json.loads(msg_recv)
        return response_dict
