"""
Rock-Paper-Scissors Game
-------------------------
Play Rock-Paper-Scissors against the computer, with score tracking
across multiple rounds.
"""

import random

CHOICES = ["rock", "paper", "scissors"]

# Maps each choice to the choice it beats
BEATS = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
}

# Shorthand letters users can type instead of full words
SHORTCUTS = {"r": "rock", "p": "paper", "s": "scissors"}


def get_user_choice():
    """Prompt the user for rock, paper, or scissors (accepts r/p/s too)."""
    while True:
        raw = input("Choose rock, paper, or scissors (r/p/s): ").strip().lower()
        if raw in CHOICES:
            return raw
        if raw in SHORTCUTS:
            return SHORTCUTS[raw]
        print("Invalid choice. Please type 'rock', 'paper', 'scissors' (or r/p/s).\n")


def get_computer_choice():
    """Randomly select rock, paper, or scissors for the computer."""
    return random.choice(CHOICES)


def determine_winner(user_choice, computer_choice):
    """Return 'user', 'computer', or 'tie' based on the game rules."""
    if user_choice == computer_choice:
        return "tie"
    if BEATS[user_choice] == computer_choice:
        return "user"
    return "computer"


def display_round_result(user_choice, computer_choice, winner):
    """Print the choices made and the outcome of the round."""
    print(f"\nYou chose:      {user_choice.capitalize()}")
    print(f"Computer chose: {computer_choice.capitalize()}")

    if winner == "tie":
        print("Result: It's a tie!\n")
    elif winner == "user":
        print(f"Result: You win! {user_choice.capitalize()} beats {computer_choice.capitalize()}.\n")
    else:
        print(f"Result: You lose! {computer_choice.capitalize()} beats {user_choice.capitalize()}.\n")


def display_score(scores):
    """Print the current running score."""
    print(f"Score -> You: {scores['user']} | Computer: {scores['computer']} | Ties: {scores['ties']}\n")
    print("-" * 40)


def ask_play_again():
    """Ask the user if they'd like to play another round."""
    while True:
        answer = input("Play again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def main():
    print("=" * 40)
    print("   ROCK - PAPER - SCISSORS")
    print("=" * 40)
    print("Rules: Rock beats Scissors, Scissors beat Paper, Paper beats Rock.")
    print("Type 'rock', 'paper', 'scissors', or just r/p/s.\n")

    scores = {"user": 0, "computer": 0, "ties": 0}

    while True:
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()
        winner = determine_winner(user_choice, computer_choice)

        if winner == "tie":
            scores["ties"] += 1
        else:
            scores[winner] += 1

        display_round_result(user_choice, computer_choice, winner)
        display_score(scores)

        if not ask_play_again():
            break
        print()

    print("\nFinal Score:")
    print(f"  You:      {scores['user']}")
    print(f"  Computer: {scores['computer']}")
    print(f"  Ties:     {scores['ties']}")

    if scores["user"] > scores["computer"]:
        print("\nCongratulations, you won overall! 🎉")
    elif scores["user"] < scores["computer"]:
        print("\nThe computer won overall. Better luck next time!")
    else:
        print("\nOverall, it's a tie!")

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
