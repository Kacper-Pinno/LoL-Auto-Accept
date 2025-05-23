# LoL-Auto-Accept
A Python automation tool that detects in-game states in League of Legends and automatically accepts matches.


## Features
- Detects queue status using image recognition.
- Automatically clicks the accept button.
- Lightweight and fast.

## Description
### Status List:
- "unknown" - image recognition doesn't recognise the status and is searching for available statuses.
- "lobby" - user is currently in the lobby.
- "queue" - user is currently searching for a match.

When match is found and "accept button" appears, the button gets clicked, meaning the match has been accepted.
Next, the application searches for "continue button", when the button appears (when the match ends), the button gets clicked.
Finally the app loops to the first state.

## Installation

1. Clone the repo
```bash
git clone https://github.com/yourusername/LeagueAutoAccept.git
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Run the app
```bash
python main.py
```
### Creating .exe file
To create an .exe file run this from your environment:
```bash
pyinstaller gui.py --noconsole --onefile --add-data "assets;assets" --icon=assets/x9_icon.ico
```
