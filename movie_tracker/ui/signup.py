from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QSpinBox, QMessageBox, QApplication, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
import sys
import movie_tracker.db.database as database

class SignupWindow(QWidget):
    def __init__(self, switch_to_login_callback=None):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.setFixedSize(420, 520)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.switch_to_login_callback = switch_to_login_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)


        logo = QLabel()
        pixmap = QPixmap("assets/logo.png")  # Assure-toi que ce fichier existe
        pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)


        title = QLabel("Create Your Account")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #ff6a00; margin-top: 15px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)


        subtitle = QLabel("Join the Movie Tracker community and save your favorites.")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #cccccc; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)


        self.name_input = self.styled_input("Full Name")
        layout.addWidget(self.name_input)


        self.age_input = QSpinBox()
        self.age_input.setRange(10, 120)
        self.age_input.setStyleSheet(self.input_style())
        layout.addWidget(self.age_input)


        self.gender_input = QComboBox()
        self.gender_input.addItems(["Select Gender", "Male", "Female", "Other"])
        self.gender_input.setStyleSheet(self.combo_style())
        layout.addWidget(self.gender_input)


        self.email_input = self.styled_input("Email")
        layout.addWidget(self.email_input)


        self.password_input = self.styled_input("Password", is_password=True)
        layout.addWidget(self.password_input)


        signup_btn = QPushButton("Sign Up")
        signup_btn.clicked.connect(self.handle_signup)
        signup_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6a00; color: white;
                padding: 12px; border-radius: 8px;
                font-size: 15px; font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e55d00;
            }
        """)
        layout.addWidget(signup_btn)


        back_btn = QPushButton("← Back to Login")
        back_btn.clicked.connect(self.switch_back)
        back_btn.setStyleSheet("color: #aaaaaa; font-size: 12px; border: none; margin-top: 15px;")
        layout.addWidget(back_btn)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

    def styled_input(self, placeholder, is_password=False):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet(self.input_style())
        if is_password:
            input_field.setEchoMode(QLineEdit.Password)
        return input_field

    def input_style(self):
        return """
            QLineEdit, QSpinBox {
                background-color: #2c2c2c;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #f0f0f0;
            }
            QLineEdit:focus, QSpinBox:focus {
                border: 1px solid #ff6a00;
            }
            QSpinBox {
                height: 35px;
            }
        """

    def combo_style(self):
        return """
            QComboBox {
                background-color: #2c2c2c;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #f0f0f0;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: url(data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'><path fill='gray' d='M7 10l5 5 5-5z'/></svg>);
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #ff6a00;
                border-radius: 6px;
                padding: 4px;
            }
        """

    def handle_signup(self):
        full_name = self.name_input.text().strip()
        age = self.age_input.value()
        gender = self.gender_input.currentText()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not all([full_name, email, password]) or gender == "Select Gender":
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return

        if database.create_user(full_name, age, gender, email, password):
            QMessageBox.information(self, "Success", "Account created!")
            if self.switch_to_login_callback:
                self.switch_to_login_callback()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Signup failed. Try a different email.")

    def switch_back(self):
        if self.switch_to_login_callback:
            self.switch_to_login_callback()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SignupWindow()
    win.show()
    sys.exit(app.exec())
