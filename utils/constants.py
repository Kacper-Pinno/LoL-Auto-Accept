import os

base_path = os.path.dirname(os.path.dirname(__file__))

ACCEPT_BUTTON = os.path.join(base_path, 'assets', 'accept_button.png')
IN_QUEUE_BUTTON = os.path.join(base_path, 'assets', 'in_queue_button.png')
NOT_IN_QUEUE_BUTTON = os.path.join(base_path, 'assets', 'not_in_queue_button.png')
CONTINUE_BUTTON = os.path.join(base_path, 'assets', 'continue_button.png')

CLIENT_PROCESS = "LeagueClient.exe"
GAME_PROCESS = "League of Legends.exe"