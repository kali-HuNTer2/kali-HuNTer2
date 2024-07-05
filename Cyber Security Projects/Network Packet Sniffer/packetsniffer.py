import pyfiglet
from termcolor import colored

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
    border_line = '#' * (max_length + 5)

    # Print the top border line
    print(colored(border_line, 'blue'))

    # Print each line of the ASCII art with side borders
    for line in ascii_art_lines:
        print(colored(f'# {line.ljust(max_length)}  #', 'blue'))

    # Print the bottom border line
    print(colored(border_line, 'blue'))
    
    # Print the author name with a border
    author_name = "Author : Vivek Kumar"
    author_border_line = '#' * (len(author_name) + 4)
    print(colored(author_border_line, 'blue'))
    print(colored(f'# {author_name} #', 'blue'))
    print(colored(author_border_line, 'blue'))

# Call the function to print ASCII art with a border
print_ascii_art_with_border()
# Importing the necessary modules
import logging
from datetime import datetime
import subprocess
import sys

# This will suppress all messages that have less significance
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
logging.getLogger("scapy.interactive").setLevel(logging.ERROR)
logging.getLogger("scapy.loading").setLevel(logging.ERROR)

try:
    from scapy.all import *
except ImportError:
    print("Scapy package for Python is not installed on your system.")
    sys.exit()

# Printing a message to the user; always use "sudo scapy" in Linux!
print("\n! Make sure to run this program as ROOT !\n")

# Asking the user for input - the interface on which to run the sniffer
net_iface = input("* Enter the interface on which to run the sniffer (e.g. 'Wi-Fi'): ")

# Setting network interface in promiscuous mode for Windows using Npcap
try:
    subprocess.call(["netsh", "interface", "set", "interface", net_iface, "admin=enable"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
except:
    print("\nFailed to configure interface as promiscuous.\n")
else:
    print("\nInterface %s was set to PROMISC mode.\n" % net_iface)

# Asking the user for the number of packets to sniff (the "count" parameter)
pkt_to_sniff = input("* Enter the number of packets to capture (0 is infinity): ")

# Consider the case when user enters 0 (infinity)
if int(pkt_to_sniff) != 0:
    print("\nThe program will capture %d packets.\n" % int(pkt_to_sniff))
elif int(pkt_to_sniff) == 0:
    print("\nThe program will capture packets until the timeout expires.\n")

# Asking the user for the time interval to sniff (the "timeout" parameter)
time_to_sniff = input("* Enter the number of seconds to run the capture: ")

# Handling the value entered by the user
if int(time_to_sniff) != 0:
    print("\nThe program will capture packets for %d seconds.\n" % int(time_to_sniff))

# Asking the user for any protocol filter he might want to apply to the sniffing process
proto_sniff = input("* Enter the protocol to filter by (arp|bootp|icmp|0 is all): ")

# Considering the case when the user enters 0 (meaning all protocols)
if proto_sniff in ["arp", "bootp", "icmp"]:
    print("\nThe program will capture only %s packets.\n" % proto_sniff.upper())
elif proto_sniff == "0":
    print("\nThe program will capture all protocols.\n")

# Asking the user to enter the name and path of the log file to be created
file_name = input("* Please give a name to the log file: ")

# Creating the text file (if it doesn't exist) for packet logging and/or opening it for appending
sniffer_log = open(file_name, "a")

# Function to be called for each captured packet
def packet_log(packet):
    now = datetime.now()
    if proto_sniff == "0":
        print(f"Time: {now} Protocol: ALL SMAC: {packet[0].src} DMAC: {packet[0].dst}", file=sniffer_log)
    elif proto_sniff in ["arp", "bootp", "icmp"]:
        print(f"Time: {now} Protocol: {proto_sniff.upper()} SMAC: {packet[0].src} DMAC: {packet[0].dst}", file=sniffer_log)

# Printing an informational message to the screen
print("\n* Starting the capture...")

# Running the sniffing process (with or without a filter)
try:
    if proto_sniff == "0":
        sniff(iface=net_iface, count=int(pkt_to_sniff), timeout=int(time_to_sniff), prn=packet_log)
    elif proto_sniff in ["arp", "bootp", "icmp"]:
        sniff(iface=net_iface, filter=proto_sniff, count=int(pkt_to_sniff), timeout=int(time_to_sniff), prn=packet_log)
    else:
        print("\nCould not identify the protocol.\n")
        sys.exit()
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit()

# Printing the closing message
print(f"\n* Please check the {file_name} file to see the captured packets.\n")

# Closing the log file
sniffer_log.close()
