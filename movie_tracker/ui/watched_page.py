from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QHBoxLayout, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon

import requests
from movie_tracker.db.database import (
    get_watched, remove_from_watched, update_review_rating
)
from movie_tracker.ui.EditReviewDialog import EditReviewDialog



ACCENT = "#ff6a00"
BG     = "#1e1e1e"
FIELD  = "#2c2c2c"



class WatchedPage(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        self.setWindowTitle("Watched Movies")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(f"background-color:{BG}; color:white;")

        self._build_ui()
        self.load_movies()

    #UI
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)


        title = QLabel("✅  Watched Movies")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size:24px; font-weight:bold; color:{ACCENT};")
        layout.addWidget(title)

        sub = QLabel("Your ratings and reviews at a glance.")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("font-size:13px; color:#cccccc; margin-bottom:8px;")
        layout.addWidget(sub)

        # List
        self.list_widget = QListWidget()
        self.list_widget.setIconSize(QSize(80, 120))
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color:{FIELD};
                border:1px solid #444;
                border-radius:10px;
                padding:12px;
                font-size:15px;
            }}
        
        """)
        layout.addWidget(self.list_widget)


        btn_row = QHBoxLayout()
        btn_row.setSpacing(15)

        delete_btn = QPushButton("❌  Delete Selected")
        delete_btn.setFixedHeight(42)
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color:{FIELD};
                color:white;
                font-weight:bold;
                font-size:15px;
                border-radius:8px;
                border:1px solid #666;
            }}
            QPushButton:hover {{ background-color:#444; }}
        """)
        delete_btn.clicked.connect(self.delete_selected)

        edit_btn = QPushButton("✏️  Edit Review / Rating")
        edit_btn.setFixedHeight(42)
        edit_btn.setStyleSheet(f"""
            QPushButton {{
                background-color:{ACCENT};
                color:white;
                font-weight:bold;
                font-size:15px;
                border-radius:8px;
            }}
            QPushButton:hover {{ background-color:#e55d00; }}
        """)
        edit_btn.clicked.connect(self.edit_selected)

        btn_row.addWidget(delete_btn)
        btn_row.addWidget(edit_btn)
        layout.addLayout(btn_row)


    @staticmethod
    def _stars(rating: int) -> str:
        return "⭐" * rating + "☆" * (5 - rating)

    def load_movies(self):
        self.list_widget.clear()
        self.movies = get_watched(self.user_id)

        for movie in self.movies:
            title   = movie.get("title",  "Untitled")
            review  = movie.get("review", "")
            rating  = movie.get("rating", 0)
            poster  = movie.get("poster_path")

            text = f"{title}\n{self._stars(int(rating))}\n📝 {review}"
            item = QListWidgetItem(text)

            if poster:
                try:
                    img = requests.get(f"https://image.tmdb.org/t/p/w92{poster}").content
                    pix = QPixmap(); pix.loadFromData(img)
                    item.setIcon(QIcon(pix))
                except Exception:
                    pass

            self.list_widget.addItem(item)

    # Actions
    def delete_selected(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            movie = self.movies[row]
            if QMessageBox.question(
                self, "Confirm Delete",
                f"Delete '{movie['title']}' from watched movies?") == QMessageBox.Yes:
                remove_from_watched(movie['id'])
                self.load_movies()

    def edit_selected(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            movie = self.movies[row]
            dlg   = EditReviewDialog(movie['review'] or "", movie['rating'] or 0, self)
            if dlg.exec():
                new_review, new_rating = dlg.get_data()
                update_review_rating(movie['id'], new_review, new_rating)
                self.load_movies()
