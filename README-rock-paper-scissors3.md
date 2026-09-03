# Rock-Paper-Scissors Game

A command-line Rock-Paper-Scissors game built in Python. Play against the computer across multiple rounds, with automatic score tracking and a friendly, guided interface.

## Features

- Play Rock, Paper, or Scissors against a randomized computer opponent
- Accepts full words (`rock`, `paper`, `scissors`) or shortcuts (`r`, `p`, `s`)
- Input validation so invalid entries don't crash the game
- Clear round-by-round results showing both choices and the outcome
- Running score tracker (You / Computer / Ties)
- "Play again?" prompt to keep playing multiple rounds
- Final score summary and overall winner announcement when you quit
- Simple, dependency-free — uses only Python's standard library

## Requirements

- Python 3.6 or higher

No external packages are needed. The script only uses Python's built-in `random` module.

## Installation

Clone this repository:

```bash
git clone https://github.com/your-username/rock-paper-scissors.git
cd rock-paper-scissors
```

## Usage

Run the script from your terminal:

```bash
python3 rock_paper_scissors.py
```

You'll be prompted to:

1. Choose rock, paper, or scissors (or type r/p/s)
2. See your choice, the computer's choice, and the round result
3. View the running score
4. Choose whether to play another round (y/n)

When you stop playing, the game prints your final score and declares an overall winner.

### Example

```
========================================
   ROCK - PAPER - SCISSORS
========================================
Rules: Rock beats Scissors, Scissors beat Paper, Paper beats Rock.
Type 'rock', 'paper', 'scissors', or just r/p/s.

Choose rock, paper, or scissors (r/p/s): rock

You chose:      Rock
Computer chose: Scissors
Result: You win! Rock beats Scissors.

Score -> You: 1 | Computer: 0 | Ties: 0

----------------------------------------
Play again? (y/n): n

Final Score:
  You:      1
  Computer: 0
  Ties:     0

Congratulations, you won overall! 🎉

Thanks for playing!
```

## Game Rules

- Rock beats Scissors
- Scissors beat Paper
- Paper beats Rock
- Matching choices result in a tie

## License

This project is open source and available under the [MIT License](LICENSE).
