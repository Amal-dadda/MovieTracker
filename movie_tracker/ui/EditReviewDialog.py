from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QSpinBox, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class EditReviewDialog(QDialog):
    def __init__(self, current_review, current_rating, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Review and Rating")
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.new_review = None
        self.new_rating = None

        layout = QVBoxLayout()
        layout.setSpacing(15)

        label_review = QLabel("Review:")
        label_review.setFont(QFont("Arial", 12, QFont.Bold))
        self.text_review = QTextEdit()
        self.text_review.setText(current_review or "")
        self.text_review.setStyleSheet("""
            QTextEdit {
                background-color: #2c2c2c;
                color: white;
                padding: 8px;
                border-radius: 8px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 1px solid #ff6a00;
            }
        """)

        label_rating = QLabel("Rating (0 to 5):")
        label_rating.setFont(QFont("Arial", 12, QFont.Bold))
        self.spin_rating = QSpinBox()
        self.spin_rating.setRange(0, 5)
        self.spin_rating.setValue(current_rating or 0)
        self.spin_rating.setStyleSheet("""
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

        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
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
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
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

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addWidget(label_review)
        layout.addWidget(self.text_review)
        layout.addWidget(label_rating)
        layout.addWidget(self.spin_rating)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_data(self):
        return self.text_review.toPlainText().strip(), self.spin_rating.value()
