WiFi Deauther and Evil Twin Attack
This project demonstrates the implementation of a WiFi deauthentication attack combined with an Evil Twin attack. The system creates a fake access point (AP) and deauthenticates users from their legitimate AP, tricking them into connecting to the fake AP.

Table of Contents
Introduction
Features
Hardware Requirements
Software Requirements
Installation
Usage
License
Disclaimer
Introduction
The WiFi Deauther and Evil Twin Attack project is designed to simulate a common security threat. By deauthenticating clients from a legitimate WiFi network and offering a rogue AP with the same SSID, this attack can capture sensitive information like passwords or session tokens.

Features
Deauthentication Attack: Continuously sends deauthentication packets to disconnect clients from their current network.
Evil Twin AP: Creates a fake AP with the same SSID as the target network, prompting users to connect.
Web Interface: A web-based control panel to manage deauthentication and Evil Twin attacks.
Hardware Requirements
ESP8266: Any variant (e.g., NodeMCU, WeMos D1 Mini).
Micro USB Cable: For programming the ESP8266.
WiFi-enabled Device: To control the ESP8266 via its web interface.
Software Requirements
Arduino IDE: Version 1.8.9 or later.
ESP8266 Board Package: Installed via Arduino Board Manager.
DNSServer Library: Included in the ESP8266 core package.
ESP8266WebServer Library: Included in the ESP8266 core package.
ESP8266HTTPClient Library: Included in the ESP8266 core package.
Installation


Set Up Arduino IDE:

Install the ESP8266 Board Package via the Board Manager.
Install required libraries if not already included.
Flash the Code:

Open the wifi_deauther_evil_twin.ino file in Arduino IDE.
Select the appropriate board and port in the Tools menu.
Upload the code to your ESP8266.
Usage
Power the ESP8266: Connect it to a USB power source.
Connect to the ESP8266: Use a WiFi-enabled device to connect to the kali-HuNTeR AP.
Access the Web Interface: Open a web browser and go to 192.168.4.1.
Perform a Network Scan: The device will automatically scan for available networks.
Select a Network: Choose the target network for the Evil Twin attack.
Start Deauthing: Begin the deauthentication attack via the web interface.
Launch the Evil Twin: Start the fake AP to capture credentials from unsuspecting users.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Disclaimer
This project is for educational purposes only. Unauthorized use of this tool to interfere with or compromise networks is illegal and unethical. Use responsibly and only on networks for which you have explicit permission.
