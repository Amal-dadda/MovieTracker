from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QApplication, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QFont, QPixmap, Qt
import sys
import movie_tracker.db.database as database

class LoginWindow(QWidget):
    def __init__(self, switch_to_signup_callback=None, on_login_success=None):
        super().__init__()
        self.setWindowTitle("Login | Movie Tracker")
        self.setFixedSize(420, 520)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.switch_to_signup_callback = switch_to_signup_callback
        self.on_login_success = on_login_success
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)




        title = QLabel("Welcome Back !!")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #ff6a00; margin-top: 15px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)


        subtitle = QLabel("Login to keep tracking your favorite movies.")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #cccccc; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Email
        self.email_input = self.styled_input("Email")
        layout.addWidget(self.email_input)

        # Password
        self.password_input = self.styled_input("Password", is_password=True)
        layout.addWidget(self.password_input)


        login_btn = QPushButton("Log In")
        login_btn.clicked.connect(self.handle_login)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6a00;
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e55d00;
            }
        """)
        layout.addWidget(login_btn)


        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))


        signup_layout = QHBoxLayout()
        signup_text = QLabel("Don't have an account?")
        signup_text.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        signup_btn = QPushButton("Sign Up")
        signup_btn.setStyleSheet("""
            QPushButton {
                color: #ff6a00;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #ffaa33;
            }
        """)
        signup_btn.clicked.connect(self.switch_signup)
        signup_layout.addWidget(signup_text)
        signup_layout.addWidget(signup_btn)
        layout.addLayout(signup_layout)

        self.setLayout(layout)

    def styled_input(self, placeholder, is_password=False):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2c2c2c;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #f0f0f0;
            }
            QLineEdit:focus {
                border: 1px solid #ff6a00;
            }
        """)
        if is_password:
            input_field.setEchoMode(QLineEdit.Password)
        return input_field

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter both email and password.")
            return

        user = database.validate_login(email, password)
        if user:
            if self.on_login_success:
                self.on_login_success(user)
            self.close()
        else:
            QMessageBox.critical(self, "Login Failed", "Incorrect credentials.")

    def switch_signup(self):
        if self.switch_to_signup_callback:
            self.switch_to_signup_callback()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())
