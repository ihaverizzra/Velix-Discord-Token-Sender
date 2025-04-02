<p align="center">
    <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="center" width="30%">
</p>
<p align="center"><h1 align="center">VELIX-DISCORD-TOKEN-SENDER</h1></p>
<p align="center">
	<em><code>❯ type shii gang</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/ihaverizzra/Velix-Discord-Token-Sender?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/ihaverizzra/Velix-Discord-Token-Sender?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/ihaverizzra/Velix-Discord-Token-Sender?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/ihaverizzra/Velix-Discord-Token-Sender?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

##  Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

##  Overview

<code>❯ this project is really useless, because in theory its not possible to generate a token, but it was a fun project!</code>

---

##  Features

<code>❯ It can generate fake tokens and sends it to the server and channel you want.</code>

---

##  Project Structure

```sh
└── Velix-Discord-Token-Sender/
    └── Velix.py
```


###  Project Index
<details open>
	<summary><b><code>VELIX-DISCORD-TOKEN-SENDER/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/ihaverizzra/Velix-Discord-Token-Sender/blob/master/Velix.py'>Velix.py</a></b></td>
				<td><code>❯ import random
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
    print(f"{Fore.RED}[-] Exiting without sending messages.\n")</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with Velix-Discord-Token-Sender, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python


###  Installation

Install Velix-Discord-Token-Sender using one of the following methods:

**Build from source:**

1. Clone the Velix-Discord-Token-Sender repository:
```sh
❯ git clone https://github.com/ihaverizzra/Velix-Discord-Token-Sender
```

2. Navigate to the project directory:
```sh
❯ cd Velix-Discord-Token-Sender
```

3. Install the project dependencies:

Use this command to install "pip install random string os requests time threading keyboard tkinter colorama"



###  Usage
Run Velix-Discord-Token-Sender using the following command:
python Velix.py

###  Testing
Run the test suite using the following command:
Run the start.bat file

---
##  Project Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

##  Contributing

- **💬 [Join the Discussions](https://github.com/ihaverizzra/Velix-Discord-Token-Sender/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/ihaverizzra/Velix-Discord-Token-Sender/issues)**: Submit bugs found or log feature requests for the `Velix-Discord-Token-Sender` project.
- **💡 [Submit Pull Requests](https://github.com/ihaverizzra/Velix-Discord-Token-Sender/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/ihaverizzra/Velix-Discord-Token-Sender
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/ihaverizzra/Velix-Discord-Token-Sender/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=ihaverizzra/Velix-Discord-Token-Sender">
   </a>
</p>
</details>

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

---
