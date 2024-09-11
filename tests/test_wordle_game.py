import unittest
import logging
from collections import defaultdict

from src.config import Config
from src.game import Game


class TestWordleGame(unittest.TestCase):
    """
    A test suite for the Wordle game implementation.
    This class tests the game's ability to guess words efficiently.
    """

    def setUp(self):
        """Initialize the test environment by loading the word list."""
        self.all_words = self.load_word_list()

    @staticmethod
    def load_word_list():
        """
        Load the word list from a file.

        Returns:
            set: A set of all valid words for the game.
        """
        with open('word_list.txt', 'r') as f:
            return set(word.strip() for word in f)

    @staticmethod
    def create_marks_array(target_word, guess):
        """
        Create a marks array based on the target word and the guess.

        Args:
            target_word (str): The word to be guessed.
            guess (str): The current guess.

        Returns:
            list: An array of marks (0, 1, or 2) for each letter in the guess.
        """
        marks = [0] * 5
        target_chars = defaultdict(int)

        # Mark correct positions
        for i in range(5):
            if guess[i] == target_word[i]:
                marks[i] = 2
            else:
                target_chars[target_word[i]] += 1

        # Mark correct letters in wrong positions
        for i in range(5):
            if marks[i] == 0 and guess[i] in target_chars and target_chars[guess[i]] > 0:
                marks[i] = 1
                target_chars[guess[i]] -= 1

        return marks

    def simulate_game(self, game, target_word):
        """
        Simulate a game for a given target word.

        Args:
            game (Game): The game instance.
            target_word (str): The word to be guessed.

        Returns:
            int or None: The number of attempts taken to guess the word, or None if failed.
        """
        guesses = []
        initial_guess = Config.INITIAL_GUESS

        for _ in range(50):  # Maximum 50 attempts
            if not guesses:
                guess = initial_guess
            else:
                guess = game._get_next_guess({"guesses": guesses})

            marks = self.create_marks_array(target_word, guess)
            guesses.append({"word": guess, "marks": marks})

            if guess == target_word:
                return len(guesses)

        return None  # Failed to guess within 50 attempts

    def test_game_simulation(self):
        """
        Test the game's performance by simulating games for all words in the word list.
        """
        total_words = len(self.all_words)
        successful_guesses = 0
        total_attempts = 0
        failed_words = []

        print(f"Starting test simulation for {total_words} words...")

        for i, word_to_guess in enumerate(self.all_words, 1):
            game = Game(None, "test_user", log_level=logging.WARN)
            attempts = self.simulate_game(game, word_to_guess)

            if attempts is not None:
                successful_guesses += 1
                total_attempts += attempts
                result = f"guessed in {attempts} attempts"
            else:
                failed_words.append(word_to_guess)
                result = "not guessed within 50 attempts"

            # Print progress every 100 words or for the last word
            if i % 100 == 0 or i == total_words:
                progress = (i / total_words) * 100
                print(f"Progress: {progress:.2f}% - Word {i}/{total_words}: '{word_to_guess}' {result}")

        self.report_results(total_words, successful_guesses, total_attempts, failed_words)

    def report_results(self, total_words, successful_guesses, total_attempts, failed_words):
        """
        Report the results of the game simulation and perform assertions.

        Args:
            total_words (int): Total number of words tested.
            successful_guesses (int): Number of words successfully guessed.
            total_attempts (int): Total number of attempts for successful guesses.
            failed_words (list): List of words that weren't guessed successfully.
        """
        success_rate = (successful_guesses / total_words) * 100
        average_attempts = total_attempts / successful_guesses if successful_guesses > 0 else 0

        print("\nTest completed:")
        print(f"Total words tested: {total_words}")
        print(f"Successful guesses: {successful_guesses}")
        print(f"Success rate: {success_rate:.2f}%")
        print(f"Average attempts for successful guesses: {average_attempts:.2f}")
        print(f"Failed words: {failed_words}")

        self.assertGreaterEqual(success_rate, 100, f"Success rate ({success_rate:.2f}%) is below 100%")
        self.assertLessEqual(average_attempts, 10, f"Average attempts ({average_attempts:.2f}) is above 10")
        self.assertEqual(len(failed_words), 0, f"Failed to guess words: {failed_words}")


class WordleTestResult(unittest.TextTestResult):
    """Custom test result class to provide more detailed output."""

    def startTest(self, test):
        super().startTest(test)
        if self.showAll:
            self.stream.write(f"Running {test._testMethodName}... ")
            self.stream.flush()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWordleGame)
    runner = unittest.TextTestRunner(resultclass=WordleTestResult, verbosity=2)
    runner.run(suite)