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

During development, I encountered and overcame several challenges:

1. TLS Implementation: Initial attempts to connect to the TLS port resulted in SSL Certification version mismatch errors. This was resolved by updating the Python SSL API in the virtual environment.

2. Efficient Word Filtering: Developing an algorithm to efficiently filter possible words based on game feedback proved challenging. While the current implementation is functional, there's room for optimization.

3. JSON Parsing: Ensuring robust parsing of JSON messages, particularly handling potential inconsistencies in field order, required careful implementation.

4. Error Handling: Implementing comprehensive error handling for network issues and unexpected server responses was crucial for creating a robust client.

## Guessing Strategy

The client employs a letter frequency-based guessing strategy:

1. Initial guess: The game begins with the predefined word "salet" (This can be modified through the config file).
2. Constraint updating: After each guess, the client updates constraints based on server feedback:
   - Letters that must be in the word
   - Position-specific constraints for each letter
3. Word filtering: The list of possible words is filtered using these constraints.
4. Letter frequency scoring: Subsequent guesses are chosen based on the frequency of their letters in the remaining possible words.
5. Endgame strategy: When two or fewer words remain, the client selects the first available word.

This approach balances exploration of new letters with leveraging known information, efficiently narrowing down possibilities.

## Testing Approach

The project includes two main test scripts:

1. `test_arg_parser.py`: This script thoroughly tests the argument parsing functionality, ensuring the code handles all possible input argument combinations correctly.

2. `test_wordle_game.py`: This comprehensive test simulates the game for every word in the word list, assuming each as the target word. It assesses the algorithm's performance, outputting an efficiency chart that asserts:
   - Correctness (100% success rate)
   - Average guesses (should be less than 10)
   - Number of failed words (should be 0)

These tests ensure the robustness of both the input handling and the core game logic.

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
