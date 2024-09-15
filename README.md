# Wordle Client

## High-level Approach

This project implements a Wordle game client in Python, designed to interact with a server via both non-encrypted and TLS-encrypted connections. The implementation is structured across four main files:

1. `client.py`: The entry point of the program, functioning as a shell script. It processes command-line arguments and initiates the game.
2. `arg_parser.py`: Handles and validates input arguments using Python's `argparse` module.
3. `game.py`: Contains the core game logic, including the guessing strategy and server communication.
4. `config.py`: Centralizes configuration settings for easy management.

The client establishes a two-way communication with the server using sockets, allowing processes on different machines to interact. The hostname specifies the server's network location, while the port identifies the specific process to connect to.

Socket communication is encapsulated in a `MySocket` class, which manages both non-encrypted and TLS-encrypted connections. This abstraction simplifies the main game logic and improves code modularity.

## Challenges Faced

During development, I encountered some challenges:

1. TLS Implementation: Initial attempts to connect to the TLS port resulted in SSL Certification version mismatch errors. This was resolved by updating the Python SSL API in the virtual environment.

2. Efficient Word Filtering: Developing an algorithm to efficiently filter possible words based on game feedback proved challenging. While the current implementation is functional, there's room for optimization.

## Guessing Strategy

The client employs a letter frequency-based guessing strategy:

1. Initial guess: The game begins with the predefined word "salet" (This can be modified through the config file).
2. Constraint updating: After each guess, the client updates constraints based on server feedback. This narrows down the possible words based on the information received. The feedback for each letter in the guess can be one of three types:

   a. Correct letter and position (marked as 2):
      - The letter is added to the 'must_contain' set.
      - The position constraint for this letter is updated to only include this letter.

   b. Correct letter, wrong position (marked as 1):
      - The letter is added to the 'must_contain' set.
      - The letter is removed from the position constraint for its current position.

   c. Letter not in word (marked as 0):
      - The letter is removed from all position constraints.

   ```
   Example:
   If the guess is "salet" and the feedback is [1, 2, 0, 1, 0], the constraints would be updated as follows:
   - 's' is in the word but not in the first position
   - 'a' is in the word and in the second position
   - 'l' is not in the word
   - 'e' is in the word but not in the fourth position
   - 't' is not in the word

   Resulting constraints:
   - must_contain = {'s', 'a', 'e'}
   - position_constraints = [
       {'a', 'b', 'c', 'd', ...'z'}, # first position (s removed)
       {'a'},                   # second position (only a)
       {'a', 'b', 'c', 'd', ...'z'}, # third position (l removed)
       {'a', 'b', 'c', 'd', ...'z'}, # fourth position (e removed)
       {'a', 'b', 'c', 'd', ...'z'}  # fifth position (t removed)
     ]
   ```

3. Word filtering: The list of all possible words is filtered using these constraints.
4. Letter frequency scoring: Subsequent guesses are chosen based on the frequency of their letters in the remaining possible words. This process works as follows: \
   a. Calculate the frequency of each letter across all remaining possible words. \
   b. For each possible word, calculate a score based on the sum of its unique letter frequencies. \
   c. Choose the word with the highest score as the next guess.
   
   ```
   Example:
   If the possible words are {'barat', 'barit', 'karat'}:
   - Letter frequencies: {'t': 3, 'r': 3, 'a': 3, 'b': 2, 'i': 1, 'k': 1}
   - Word scores:
     * score(barat) = 11   [2 (b) + 3 (a) + 3 (r) + 3 (t)]
     * score(barit) = 12   [2 (b) + 3 (a) + 3 (r) + 1 (i) + 3 (t)]
     * score(karat) = 10   [1 (k) + 3 (a) + 3 (r) + 3 (t)]
   - 'barit' would be chosen as it has the highest score.
   ```
5. Endgame strategy: When two or fewer words remain, the client selects the first available word.

## Testing Approach

The project includes two main test scripts:

1. `test_arg_parser.py`: This script tests the argument parsing functionality, ensuring the code handles all possible input argument combinations correctly.

2. `test_wordle_game.py`: This is a comprehensive test that simulates the game for every word in the word list, assuming each as the target word. It assesses the algorithm's performance, outputting an efficiency chart that asserts:
   - Correctness (100% success rate)
   - Average guesses (should be less than 10)
   - Number of failed words (should be 0)


## Efficiency of the algorithm
   The test file `test_wordle_game.py` also produces a chart of how efficiently the algorithm guesses the words sampled over all the words in the word list.
   ```
   Total words tested: 15918
   Successful guesses: 15918
   Success rate: 100.00%
   Average attempts for successful guesses: 6.29
   Failed words: []
   ```

## Additional Notes
1. Future Improvements: 
   - Implement a more sophisticated guessing strategy, possibly using information theory concepts as explored in the 3Blue1Brown video on Wordle.
