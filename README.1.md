# Password Generator

A simple command-line password generator built in Python. It lets you choose the length and character complexity of your password — uppercase letters, lowercase letters, digits, and symbols — and generates a strong, random password to match.

## Features

- Custom password length (with input validation)
- Choose which character types to include:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Digits (0-9)
  - Symbols (!@#$...)
- Guarantees at least one character from each selected type
- Randomly shuffles the final password for unpredictability
- Simple, dependency-free — uses only Python's standard library

## Requirements

- Python 3.6 or higher

No external packages are needed. The script only uses Python's built-in `random` and `string` modules.

## Installation

Clone this repository:

```bash
git clone https://github.com/your-username/password-generator.git
cd password-generator
```

## Usage

Run the script from your terminal:

```bash
python3 password_generator.py
```

You'll be prompted to:

1. Enter your desired password length
2. Choose (y/n) whether to include uppercase letters
3. Choose (y/n) whether to include lowercase letters
4. Choose (y/n) whether to include digits
5. Choose (y/n) whether to include symbols

The generated password will then be printed to the screen.

### Example

```
=== Password Generator ===

Enter the desired password length: 12

Choose the character types to include in your password:
Include uppercase letters (A-Z)? (y/n): y
Include lowercase letters (a-z)? (y/n): y
Include digits (0-9)? (y/n): y
Include symbols (!@#$...)? (y/n): y

Your generated password is:

    -/KK,#)Bv6KC
```

## Notes on Security

This project uses Python's `random` module, which is fine for learning purposes and casual use. For generating passwords intended for real-world security (e.g. actual account passwords), consider swapping `random` for Python's [`secrets`](https://docs.python.org/3/library/secrets.html) module, which is designed for cryptographically strong randomness.

## License

This project is open source and available under the [MIT License](LICENSE).
