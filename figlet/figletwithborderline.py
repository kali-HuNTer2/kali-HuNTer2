import pyfiglet
from termcolor import colored
from pynput import keyboard

# Function to print ASCII art with a border in blue
def print_ascii_art_with_border():
    # Define the text and the font
    text = "kali-HuNTer"
    font = "speed"

    # Generate ASCII art text
    ascii_art = pyfiglet.figlet_format(text, font=font)

    # Split the ASCII art into lines
    ascii_art_lines = ascii_art.split('\n')

    # Find the maximum length of the ASCII art lines
    max_length = max(len(line) for line in ascii_art_lines)

    # Create a border line with '*' characters
    border_line = '*' * (max_length + 4)

    # Print the top border line
    print(colored(border_line, 'blue'))

    # Print each line of the ASCII art with side borders
    for line in ascii_art_lines:
        print(colored(f'* {line.ljust(max_length)} *', 'blue'))

    # Print the bottom border line
    print(colored(border_line, 'blue'))
    
    # Print the author name
    print(colored("Author : Vivek Kumar", 'blue'))

# Call the function to print ASCII art with a border
print_ascii_art_with_border()
