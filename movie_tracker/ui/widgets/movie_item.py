from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPixmap
import requests
from io import BytesIO

class MovieItemWidget(QWidget):
    def __init__(self, movie, add_callback, watched_callback):
        super().__init__()
        self.movie = movie
        self.add_callback = add_callback
        self.watched_callback = watched_callback
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        # Poster
        poster_label = QLabel()
        poster_path = self.movie.get("poster_path")
        if poster_path:
            url = f"https://image.tmdb.org/t/p/w92{poster_path}"
            try:
                response = requests.get(url)
                pixmap = QPixmap()
                pixmap.loadFromData(BytesIO(response.content).read())
                poster_label.setPixmap(pixmap)
            except:
                pass
        layout.addWidget(poster_label)


        info_layout = QVBoxLayout()
        title = self.movie.get("title", "Unknown Title")
        year = self.movie.get("release_date", "")[:4]
        overview = self.movie.get("overview", "No overview.")[:150]

        title_label = QLabel(f"<b>{title} ({year})</b>")
        desc_label = QLabel(overview)
        desc_label.setWordWrap(True)

        info_layout.addWidget(title_label)
        info_layout.addWidget(desc_label)


        add_btn = QPushButton("➕ Add to Watchlist")
        add_btn.setStyleSheet("background-color: #4caf50; color: white; padding: 5px; border-radius: 5px;")
        add_btn.clicked.connect(self.add_to_watchlist)
        info_layout.addWidget(add_btn)

        watched_btn = QPushButton("✔ Watched")
        watched_btn.setStyleSheet("background-color: #2196f3; color: white; padding: 5px; border-radius: 5px;")
        watched_btn.clicked.connect(self.mark_as_watched)
        info_layout.addWidget(watched_btn)


        layout.addLayout(info_layout)

        self.setLayout(layout)

    def add_to_watchlist(self):
        self.add_callback(self.movie)

    def mark_as_watched(self):
        self.watched_callback(self.movie)