import sys
from PySide6.QtWidgets import QApplication
from ui.login import LoginWindow
from ui.signup import SignupWindow
from ui.main_app import MainAppWindow


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = None
        self.signup_window = None
        self.show_login()


    def show_login(self):
        self.login_window = LoginWindow(
            switch_to_signup_callback=self.show_signup,
            on_login_success=self.on_login_success
        )
        self.login_window.show()

    def show_signup(self):
        self.signup_window = SignupWindow(
            switch_to_login_callback=self.show_login
        )
        self.signup_window.show()

    def on_login_success(self, user_data):
        print("Login successful for:", user_data['full_name'])
        # TODO: open main app window (to-watch list, etc.)

    def run(self):
        sys.exit(self.app.exec())




    def on_login_success(self, user_data):
        self.login_window.close()  # Close login
        self.main_window = MainAppWindow(user_data)
        self.main_window.show()


if __name__ == "__main__":
    App().run()
