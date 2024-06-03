
import pyfiglet
from termcolor import colored
import random
import string

def print_ascii_art_with_border():
    text = "kali-HuNTer"
    font = "speed"
    ascii_art = pyfiglet.figlet_format(text, font=font)
    ascii_art_lines = ascii_art.split('\n')
    max_length = max(len(line) for line in ascii_art_lines)
    border_line = '#' * (max_length + 4)

    print(colored(border_line, 'blue'))
    for line in ascii_art_lines:
        print(colored(f'# {line.ljust(max_length)} #', 'blue'))
    print(colored(border_line, 'blue'))

    author_name = "Author : Vivek Kumar"
    author_border_line = '#' * (len(author_name) + 4)
    print(colored(author_border_line, 'blue'))
    print(colored(f'# {author_name} #', 'blue'))
    print(colored(author_border_line, 'blue'))

def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True):
    characters = ''
    if use_uppercase: characters += string.ascii_uppercase
    if use_lowercase: characters += string.ascii_lowercase
    if use_digits: characters += string.digits
    if use_symbols: characters += string.punctuation

    if not characters:
        raise ValueError("At least one character type should be selected")

    return ''.join(random.choice(characters) for _ in range(length))

def main():
    print_ascii_art_with_border()
    print("Welcome to the Password Generator!")
    length = int(input("Enter the length of the password: "))
    use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
    use_digits = input("Include digits? (y/n): ").lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").lower() == 'y'

    try:
        password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols)
        print("Generated Password:", password)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
