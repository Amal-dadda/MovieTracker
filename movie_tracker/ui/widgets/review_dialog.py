from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QSpinBox, QPushButton, QHBoxLayout
from movie_tracker.db.database import add_to_watched, remove_to_watch

class ReviewDialog(QDialog):
    def __init__(self, user_id, movie):
        super().__init__()
        self.setWindowTitle("Rate and Review")
        self.setMinimumWidth(300)

        self.user_id = user_id
        self.movie = movie

        layout = QVBoxLayout()

        layout.addWidget(QLabel("📝 Write your review (optional):"))
        self.review_input = QTextEdit()
        self.review_input.setStyleSheet("""
            QTextEdit {
                background-color: #2c2c2c;
                border: 1px solid #444;
                border-radius: 8px;
                color: #f0f0f0;
                padding: 10px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 1px solid #ff6a00;
            }
        """)
        layout.addWidget(self.review_input)

        layout.addWidget(QLabel("⭐ Rate the movie (0–5):"))
        self.rating_input = QSpinBox()
        self.rating_input.setRange(0, 5)
        self.rating_input.setStyleSheet("""
            QSpinBox {
                background-color: #2c2c2c;
                border: 1px solid #444;
                border-radius: 8px;
                color: #f0f0f0;
                padding: 10px;
                font-size: 14px;
            }
            QSpinBox:focus {
                border: 1px solid #ff6a00;
            }
        """)
        layout.addWidget(self.rating_input)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Submit")
        self.ok_btn.setStyleSheet("""
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
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def accept(self):
        review = self.review_input.toPlainText()
        rating = self.rating_input.value()

        remove_to_watch(self.movie["id"])

        super().accept()

    def get_data(self):
        return self.review_input.toPlainText(), self.rating_input.value()

    def get_review(self):
        return self.review_input.toPlainText()

    def get_rating(self):
        return self.rating_input.value()
