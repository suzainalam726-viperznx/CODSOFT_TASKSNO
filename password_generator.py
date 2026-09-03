"""
Password Generator
-------------------
Generates a strong, random password based on a length and complexity
level chosen by the user.
"""

import random
import string


def build_character_pool(use_upper, use_lower, use_digits, use_symbols):
    """Combine the character sets the user wants to include."""
    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation
    return pool


def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """Generate a random password of the given length using the chosen character sets."""
    pool = build_character_pool(use_upper, use_lower, use_digits, use_symbols)

    if not pool:
        raise ValueError("At least one character type must be selected.")

    # Guarantee at least one character from each selected category,
    # so the password actually reflects the chosen complexity.
    guaranteed = []
    if use_upper:
        guaranteed.append(random.choice(string.ascii_uppercase))
    if use_lower:
        guaranteed.append(random.choice(string.ascii_lowercase))
    if use_digits:
        guaranteed.append(random.choice(string.digits))
    if use_symbols:
        guaranteed.append(random.choice(string.punctuation))

    if length < len(guaranteed):
        raise ValueError(f"Password length must be at least {len(guaranteed)} "
                          f"to include all selected character types.")

    remaining_length = length - len(guaranteed)
    password_chars = guaranteed + [random.choice(pool) for _ in range(remaining_length)]

    random.shuffle(password_chars)
    return "".join(password_chars)


def get_yes_no(prompt):
    """Ask a yes/no question and return True/False."""
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def get_length():
    """Ask the user for the desired password length, validating the input."""
    while True:
        try:
            length = int(input("Enter the desired password length: "))
            if length <= 0:
                print("Length must be a positive number.")
                continue
            return length
        except ValueError:
            print("Please enter a valid whole number.")


def main():
    print("=== Password Generator ===\n")

    length = get_length()

    print("\nChoose the character types to include in your password:")
    use_upper = get_yes_no("Include uppercase letters (A-Z)?")
    use_lower = get_yes_no("Include lowercase letters (a-z)?")
    use_digits = get_yes_no("Include digits (0-9)?")
    use_symbols = get_yes_no("Include symbols (!@#$...)?")

    if not any([use_upper, use_lower, use_digits, use_symbols]):
        print("\nYou must select at least one character type. Defaulting to all types.")
        use_upper = use_lower = use_digits = use_symbols = True

    try:
        password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        print(f"\nYour generated password is:\n\n    {password}\n")
    except ValueError as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
