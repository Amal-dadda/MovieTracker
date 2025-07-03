from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from movie_tracker.tmdb_api import search_movies, get_trending_movies
from movie_tracker.ui.widgets.movie_item import MovieItemWidget
from movie_tracker.ui.widgets.review_dialog import ReviewDialog
from movie_tracker.db import database
from movie_tracker.db.database import add_to_watched

ACCENT = "#ff6a00"
BG     = "#1e1e1e"
FIELD  = "#2c2c2c"

class SearchPage(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Search Movies")
        self.setFixedSize(800, 600)
        self.setStyleSheet(f"background-color: {BG}; color: white;")
        self.init_ui()
        self.load_suggestions()


    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)


        title = QLabel("🔍  Search for Movies")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {ACCENT};")
        layout.addWidget(title)


        subtitle = QLabel("Find something to watch, add to your list, or mark as watched.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 13px; color: #cccccc; margin-bottom: 5px;")
        layout.addWidget(subtitle)


        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter movie title…")
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {FIELD};
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
                font-size: 15px;
                color: #f0f0f0;
            }}
            QLineEdit:focus {{ border: 1px solid {ACCENT}; }}
        """)
        search_row.addWidget(self.search_input)

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.perform_search)
        search_btn.setFixedHeight(40)
        search_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                font-size: 15px;
                font-weight: bold;
                border-radius: 8px;
                padding: 0 18px;
            }}
            QPushButton:hover {{ background-color: #e55d00; }}
        """)
        search_row.addWidget(search_btn)
        layout.addLayout(search_row)


        self.list = QListWidget()
        self.list.setViewMode(QListWidget.IconMode)
        self.list.setResizeMode(QListWidget.Adjust)
        self.list.setIconSize(QPixmap(150, 225).size())
        self.list.setSpacing(15)
        self.list.setStyleSheet(f"""
            QListWidget {{
                background-color: {BG};
                border: none;
            }}
            QListWidget::item {{ color: white; font-size: 14px; }}
            QListWidget::item:selected {{ background: {ACCENT}; }}
        """)
        layout.addWidget(self.list)

        self.setLayout(layout)


    def perform_search(self):
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Error", "Please enter a movie title.")
            return

        self.list.clear()
        movies = search_movies(query)
        if not movies:
            QMessageBox.information(self, "No Results", "No movies found.")
            return

        self.populate_list(movies)

    def add_to_watchlist(self, movie):
        if database.add_to_watchlist(self.user_id, movie):
            QMessageBox.information(self, "Success", f"{movie['title']} added to watchlist.")
        else:
            QMessageBox.critical(self, "Error", "Failed to add movie to watchlist.")

    def mark_as_watched(self, movie):
        dialog = ReviewDialog(self.user_id, movie)
        if dialog.exec():
            review, rating = dialog.get_data()
            add_to_watched(self.user_id, movie, rating, review)
            QMessageBox.information(self, "Done", "Movie added to Watched list.")


    def populate_list(self, movies):
        for movie in movies:
            item   = QListWidgetItem()
            widget = MovieItemWidget(movie,
                                     add_callback=self.add_to_watchlist,
                                     watched_callback=self.mark_as_watched)
            item.setSizeHint(widget.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, widget)

    def load_suggestions(self):
        self.list.clear()
        trending = get_trending_movies()[:10]  # first 10 trending
        self.populate_list(trending)
