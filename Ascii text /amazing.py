import pyfiglet

# Define the word
word = "HuNTer"

# List of selected fonts
fonts = ['slant']

# Print the word in each font
for font in fonts:
    ascii_art = pyfiglet.figlet_format(word, font=font)
    print(f"Font: {font}\n")
    print(ascii_art)
    print("\n" + "#" * 80 + "\n")
