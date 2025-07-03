from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QListWidgetItem, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon, QFont
import requests

from movie_tracker.db.database import (
    get_watchlist, remove_to_watch, move_to_watched
)
from movie_tracker.ui.widgets.review_dialog import ReviewDialog

ACCENT = "#ff6a00"
BG     = "#1e1e1e"
FIELD  = "#2c2c2c"

class ToWatchPage(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id   = user_id
        self.movie_ids = {}

        self.setWindowTitle("My Watchlist")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(f"background-color:{BG}; color:white;")

        self.build_ui()
        self.load_movies()


    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)


        title = QLabel("🎬  Your Movie Watchlist")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size:24px; font-weight:bold; color:{ACCENT};")
        layout.addWidget(title)

        subtitle = QLabel("Manage the films you plan to watch.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size:13px; color:#cccccc; margin-bottom:8px;")
        layout.addWidget(subtitle)


        self.movie_list = QListWidget()
        self.movie_list.setIconSize(QSize(80, 120))
        self.movie_list.setStyleSheet(f"""
            QListWidget {{
                background-color:{FIELD};
                border:1px solid #444;
                border-radius:10px;
                padding:12px;
            }}
            QListWidget::item {{
                padding:10px;
                margin:5px 0;
                color:white;
                font-size:15px;
            }}
            
        """)
        layout.addWidget(self.movie_list)


        btn_row = QHBoxLayout()
        btn_row.setSpacing(15)

        remove_btn = QPushButton("❌  Remove Selected")
        remove_btn.clicked.connect(self.remove_selected)
        remove_btn.setFixedHeight(42)
        remove_btn.setStyleSheet("""
                   QPushButton {
                       background-color: #c62828;
                       color: white;
                       padding: 12px;
                       font-weight: bold;
                       border: none;
                       border-radius: 8px;
                   }
                   QPushButton:hover {
                       background-color: #e53935;
                   }
               """)

        watched_btn = QPushButton("✅  Mark as Watched")
        watched_btn.clicked.connect(self.mark_selected_as_watched)
        watched_btn.setFixedHeight(42)
        watched_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #1976d2;
                        color: white;
                        padding: 12px;
                        font-weight: bold;
                        border: none;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #1e88e5;
                    }
                """)

        btn_row.addWidget(remove_btn)
        btn_row.addWidget(watched_btn)
        layout.addLayout(btn_row)


    def load_movies(self):
        self.movie_list.clear()
        self.movie_ids.clear()

        for i, movie in enumerate(get_watchlist(self.user_id)):
            title  = movie.get("title", "Untitled")
            year   = movie.get("release_year", "")
            poster = movie.get("poster_path")
            mid    = movie.get("id")

            item = QListWidgetItem(f"{title} ({year})")
            if poster:
                try:
                    img = requests.get(f"https://image.tmdb.org/t/p/w185{poster}").content
                    pix = QPixmap()
                    pix.loadFromData(img)
                    item.setIcon(QIcon(pix))
                except Exception:
                    pass

            self.movie_list.addItem(item)
            self.movie_ids[i] = mid


    def remove_selected(self):
        rows = sorted([self.movie_list.row(i) for i in self.movie_list.selectedItems()], reverse=True)
        for row in rows:
            mid = self.movie_ids.get(row)
            if mid:
                remove_to_watch(mid)
            self.movie_list.takeItem(row)
        self.load_movies()

    def mark_selected_as_watched(self):
        for item in self.movie_list.selectedItems():
            row = self.movie_list.row(item)
            mid = self.movie_ids.get(row)
            if mid is None:
                continue

            movies = get_watchlist(self.user_id)
            movie  = next((m for m in movies if m["id"] == mid), None)
            if not movie:
                continue

            dlg = ReviewDialog(self.user_id, movie)
            if dlg.exec():
                review, rating = dlg.get_data()
                move_to_watched(self.user_id, mid, movie, review, rating)
                self.load_movies()
