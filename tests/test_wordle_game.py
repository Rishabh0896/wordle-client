import unittest
import logging
from collections import defaultdict
from unittest.mock import patch, mock_open
from src.game import Game


class TestWordleGame(unittest.TestCase):
    def setUp(self):
        self.all_words = set(self.load_word_list())

    def load_word_list(self):
        # Load words from file
        with open('word_list.txt', 'r') as f:
            return [word.strip() for word in f]

    def create_marks_array(self, target_word, guess):
        marks = [0] * 5
        target_chars = defaultdict(int)

        for i in range(5):
            if guess[i] == target_word[i]:
                marks[i] = 2
            else:
                target_chars[target_word[i]] += 1

        for i in range(5):
            if marks[i] == 0 and guess[i] in target_chars and target_chars[guess[i]] > 0:
                marks[i] = 1
                target_chars[guess[i]] -= 1

        return marks

    def simulate_game(self, game, target_word):
        guesses = []
        guess = 'salet'
        marks = self.create_marks_array(target_word, guess)
        guesses.append({"word": guess, "marks": marks})

        for _ in range(50):
            guess = game.get_next_guess({"guesses": guesses})
            marks = self.create_marks_array(target_word, guess)
            guesses.append({"word": guess, "marks": marks})

            if guess == target_word:
                return len(guesses)

        return None

    def test_game_simulation(self):
        all_words = set(self.load_word_list())
        total_words = len(all_words)
        successful_guesses = 0
        total_attempts = 0
        failed_words = []

        print(f"Starting test simulation for {total_words} words...")

        for i, word_to_guess in enumerate(all_words, 1):
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

        success_rate = (successful_guesses / total_words) * 100
        average_attempts = total_attempts / successful_guesses if successful_guesses > 0 else 0

        print("\nTest completed:")
        print(f"Total words tested: {total_words}")
        print(f"Successful guesses: {successful_guesses}")
        print(f"Success rate: {success_rate:.2f}%")
        print(f"Average attempts for successful guesses: {average_attempts:.2f}")
        print(f"Failed words: {failed_words}")

        self.assertGreaterEqual(success_rate, 100, f"Success rate ({success_rate:.2f}%) is below 100%")
        self.assertLessEqual(average_attempts, 7, f"Average attempts ({average_attempts:.2f}) is above 7")
        self.assertEqual(len(failed_words), 0, f"Failed to guess words: {failed_words}")


class WordleTestResult(unittest.TextTestResult):
    def startTest(self, test):
        super().startTest(test)
        if self.showAll:
            self.stream.write(f"Running {test._testMethodName}... ")
            self.stream.flush()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWordleGame)
    runner = unittest.TextTestRunner(resultclass=WordleTestResult, verbosity=2)
    runner.run(suite)
