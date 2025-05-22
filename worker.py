from PyQt5.QtCore import QThread, pyqtSignal
import time

# Importing constants and utility functions from the project
from utils.constants import *  # Includes file paths or image references like ACCEPT_BUTTON, etc.
from utils.image_utils import image_exists, locate_and_click  # Image recognition utilities
from utils.process_utils import is_process_running  # (Not used in this file, can be removed if unused)

class LeagueBotThread(QThread):
    # Signal to send logs/messages back to the GUI (connected to console output)
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = True  # Controls whether the thread should keep running

    def run(self):
        """Main loop for monitoring League client and interacting with it."""
        current_status = None  # Tracks what state the client is in (lobby, queue, etc.)
        match_accepted = False  # Whether a match was accepted
        waiting_for_continue_logged = False  # Avoids spamming the same log repeatedly

        while self.running:
            # Try to accept a match if it's found and hasn't been accepted yet
            if not match_accepted and locate_and_click(ACCEPT_BUTTON, delay=1):
                self.log_signal.emit("Match accepted!")
                match_accepted = True
                current_status = 'match_accepted'
                waiting_for_continue_logged = False

            # If match was accepted, check for the 'Continue' button
            if match_accepted:
                if not waiting_for_continue_logged:
                    self.log_signal.emit("Waiting for continue button...")
                    waiting_for_continue_logged = True

                # Once the continue button appears, wait a bit and click it until it disappears
                if image_exists(CONTINUE_BUTTON):
                    time.sleep(3)  # Give it a moment to become stable
                    while image_exists(CONTINUE_BUTTON):
                        locate_and_click(CONTINUE_BUTTON)
                        time.sleep(1)
                    self.log_signal.emit("Continue button clicked, restarting loop.")
                    # Reset loop state
                    match_accepted = False
                    current_status = None
                    waiting_for_continue_logged = False

            # If not in a match, determine client status (in queue or not)
            if not match_accepted:
                if image_exists(NOT_IN_QUEUE_BUTTON):
                    if current_status != 'lobby':
                        self.log_signal.emit("Status: In lobby (not searching for a match)")
                        current_status = 'lobby'

                elif image_exists(IN_QUEUE_BUTTON):
                    if current_status != 'queue':
                        self.log_signal.emit("Status: In queue (searching for a match)")
                        current_status = 'queue'

                else:
                    if current_status != 'unknown':
                        self.log_signal.emit("Status: Unknown - retrying...")
                        current_status = 'unknown'

            # Wait a bit before looping again to reduce CPU usage
            time.sleep(1)

    def stop(self):
        """Stop the thread and wait for it to fully exit."""
        self.running = False
        self.wait()