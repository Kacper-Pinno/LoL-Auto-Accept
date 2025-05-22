import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel,
    QPushButton, QTextEdit
)
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import Qt
from worker import LeagueBotThread  # Custom thread handling League automation logic


# Custom stream to redirect stdout/stderr to QTextEdit
class EmittingStream:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        # Move cursor to the end and append new text
        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.insertPlainText(text)
        self.text_edit.ensureCursorVisible()

    def flush(self):
        pass  # Required to support file-like behavior


# Main application window class
class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Set window title and icon
        self.setWindowTitle("X9 Esports")
        self.setWindowIcon(QIcon("C:\\Users\\Kacpe\\Documents\\MyCodes\\LeagueAutoAccept\\assets\\x9_icon2.png"))

        # Center the window and set a fixed size
        self.center_the_window()
        self.setFixedSize(512, 288)

        # Enable minimize and close buttons
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # Create main widget and layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Console output area (read-only)
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.layout.addWidget(QLabel("Console Output:"))
        self.layout.addWidget(self.output_console)

        # Start button to launch the bot
        self.test_button = QPushButton("Start")
        self.test_button.clicked.connect(self.start_bot)
        self.layout.addWidget(self.test_button)

        # Instantiate the bot thread (does the background work)
        self.bot_thread = LeagueBotThread()
        self.bot_thread.log_signal.connect(self.log_to_console)  # Connect signal to print logs to UI

        # Finalize layout
        self.main_widget.setLayout(self.layout)
        self.addWidget(self.main_widget)

        # Redirect standard output and error to the console widget
        sys.stdout = EmittingStream(self.output_console)
        sys.stderr = EmittingStream(self.output_console)

        # Initial log message
        print("App started successfully!")

    def center_the_window(self):
        """Center the application window on the primary screen."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def start_bot(self):
        """Start the background bot thread if it’s not already running."""
        if not self.bot_thread.isRunning():
            print("Starting League automation...")
            self.bot_thread.start()
        else:
            print("Bot is already running.")

    def log_to_console(self, message):
        """Log messages from the bot thread to the console output."""
        print(message)  # Automatically goes to QTextEdit via EmittingStream

    def closeEvent(self, event):
        """Handle window close event by stopping the bot thread if needed."""
        if self.bot_thread.isRunning():
            print("Stopping bot thread...")
            self.bot_thread.stop()
        event.accept()


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())