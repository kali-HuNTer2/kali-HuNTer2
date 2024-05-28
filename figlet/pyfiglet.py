import pyfiglet
from termcolor import colored
from pynput import keyboard

# Function to print ASCII art in blue
def print_ascii_art():
    # Define the text and the font
    text = "kali-HuNTer"
    font = "speed"

    # Generate ASCII art text
    ascii_art = pyfiglet.figlet_format(text, font=font)

    # Print the ASCII art text in blue color
    print(colored(ascii_art, 'blue'))
    print("Author : Vivek Kumar")
