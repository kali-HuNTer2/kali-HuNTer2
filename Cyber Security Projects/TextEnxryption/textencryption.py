import tkinter as tk
from tkinter import messagebox
import pyfiglet
from termcolor import colored

# Define the encrypt function
def encrypt(text, shift):
    """Encrypt the text using Caesar cipher with the specified shift."""
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr(start + (ord(char) - start + shift) % 26)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

# Define the decrypt function
def decrypt(text, shift):
    """Decrypt the text using Caesar cipher with the specified shift."""
    return encrypt(text, -shift)

# Function to print ASCII art with a border in blue
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

    author_name = "Author: Vivek Kumar"
    author_border_line = '#' * (len(author_name) + 4)
    print(colored(author_border_line, 'blue'))
    print(colored(f'# {author_name} #', 'blue'))
    print(colored(author_border_line, 'blue'))

# Print ASCII art when the application starts
print_ascii_art_with_border()

# Initialize the Tkinter window
root = tk.Tk()
root.title("Caesar Cipher Encryptor/Decryptor")
root.geometry("400x300")

# Create widgets
tk.Label(root, text="Enter your message:").pack(pady=10)
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=5)

tk.Label(root, text="Enter shift value:").pack(pady=10)
shift_entry = tk.Entry(root, width=10)
shift_entry.pack(pady=5)

result_label = tk.Label(root, text="", wraplength=300)
result_label.pack(pady=20)

# Define the encryption handler
def handle_encrypt():
    try:
        message = message_entry.get()
        shift = int(shift_entry.get())
        encrypted_message = encrypt(message, shift)
        result_label.config(text=f"Encrypted Message: {encrypted_message}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid shift value.")

# Define the decryption handler
def handle_decrypt():
    try:
        message = message_entry.get()
        shift = int(shift_entry.get())
        decrypted_message = decrypt(message, shift)
        result_label.config(text=f"Decrypted Message: {decrypted_message}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid shift value.")

# Add buttons to the window
tk.Button(root, text="Encrypt", command=handle_encrypt).pack(pady=5)
tk.Button(root, text="Decrypt", command=handle_decrypt).pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
