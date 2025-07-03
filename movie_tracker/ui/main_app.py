from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpacerItem, QSizePolicy, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve ,QSize
from PySide6.QtGui import QIcon, QFont, QColor, QLinearGradient, QPainter
import movie_tracker.db.database as db

from ui.to_watch_page import ToWatchPage
from ui.watched_page import WatchedPage
from ui.search_page import SearchPage


class GradientButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(60)
        self.setCursor(Qt.PointingHandCursor)

        # Animation setup
        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(300)
        self.color = QColor("#ff6a00")

        self.normal_gradient = self.create_gradient("#ff6a00", "#ff8c42")
        self.hover_gradient = self.create_gradient("#ff8c42", "#ff6a00")

    def create_gradient(self, color1, color2):
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(color1))
        gradient.setColorAt(1, QColor(color2))
        return gradient

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)


        if self.underMouse():
            gradient = self.hover_gradient
        else:
            gradient = self.normal_gradient

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)


        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

    def enterEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(QColor("#ff6a00"))
        self.animation.setEndValue(QColor("#ff8c42"))
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(QColor("#ff8c42"))
        self.animation.setEndValue(QColor("#ff6a00"))
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()


class FilmStripCard(QFrame):


    def __init__(self, number: int, title: str, icon_path: str = None):
        super().__init__()
        self.setFixedSize(200, 140)


        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
        """)


        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)


        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)

        if icon_path:
            icon_label = QLabel()
            icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
            title_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #666666;
            font-size: 14px;
            font-weight: bold ;
            font-weight: medium;
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        layout.addLayout(title_layout)


        self.num_lbl = QLabel(str(number))
        self.num_lbl.setStyleSheet("""
            font-size: 42px;
            font-weight: bold;
            color: #ff6a00;
        """)
        self.num_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.num_lbl)


        self.bottom_bar = QFrame()
        self.bottom_bar.setFixedHeight(4)
        self.bottom_bar.setStyleSheet("background-color: #ff6a00; border-radius: 2px;")
        layout.addWidget(self.bottom_bar)

    def update_number(self, value: int):
        self.num_lbl.setText(str(value))



class MainAppWindow(QWidget):
    def __init__(self, user_data: dict):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Movie Tracker · Dashboard")
        self.setFixedSize(1000, 700)


        self.setStyleSheet("""
            background-color: #121212;
            color: #ffffff;
        """)

        self.build_ui()
        self.refresh_stats()

    def build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(25)


        header = QVBoxLayout()
        header.setSpacing(10)

       #refresh
        refresh_layout = QHBoxLayout()
        refresh_layout.setAlignment(Qt.AlignCenter)

        refresh_btn = QPushButton("Refresh Dashboard")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ff6a00;
                        color: white;
                        padding: 8px 20px;
                        border-radius: 8px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #ff8533;
                    }
                """)
        refresh_btn.clicked.connect(self.refresh_stats)
        refresh_layout.addWidget(refresh_btn)

        main_layout.addLayout(refresh_layout)

        # Titre et sous-titre
        title = QLabel(f"✨ {self.user_data['full_name']}'s Movie Dashboard ✨")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #ff6a00;
            margin-bottom: 5px;
            text-shadow: 0 0 10px rgba(255, 106, 0, 0.5);
        """)
        header.addWidget(title)


        subtitle = QLabel("Your personal movie collection manager")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 16px; 
            color: #aaaaaa;
            margin-bottom: 20px;
        """)
        header.addWidget(subtitle)

        main_layout.addLayout(header)

        #les cards
        cards_row = QHBoxLayout()
        cards_row.setSpacing(30)
        cards_row.setContentsMargins(0, 20, 0, 20)
        cards_row.setAlignment(Qt.AlignCenter)

        self.watched_card = FilmStripCard(
            0, "Movies Watched"
        )
        self.watchlist_card = FilmStripCard(
            0, "Watchlist"
        )

        cards_row.addWidget(self.watched_card)
        cards_row.addWidget(self.watchlist_card)
        main_layout.addLayout(cards_row)

        # les bouttons
        actions_title = QLabel("Quick Actions")
        actions_title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #ff6a00;
            margin-top: 20px;
        """)
        main_layout.addWidget(actions_title)

        actions_sub = QLabel("What would you like to do today?")
        actions_sub.setStyleSheet("""
            font-size: 14px; 
            color: #aaaaaa; 
            margin-bottom: 15px;
        """)
        main_layout.addWidget(actions_sub)


        buttons_grid = QHBoxLayout()
        buttons_grid.setSpacing(20)

        buttons = [
            {
                "text": "To-Watch List",
                "action": self.to_watch
            },
            {
                "text": "Watched List",
                "action": self.watched
            },
            {
                "text": "Search Movies",
                "action": self.search_movies
            }
        ]

        for btn_info in buttons:
            btn = GradientButton(btn_info["text"])
            btn.setIconSize(QSize(24, 24))
            btn.clicked.connect(btn_info["action"])
            buttons_grid.addWidget(btn)

        main_layout.addLayout(buttons_grid)

        # logout
        footer = QHBoxLayout()
        footer.addStretch()

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet("""
            QPushButton {
                color: #ff6a00; 
                font-size: 14px; 
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 106, 0, 0.2);
                text-decoration: underline;
            }
        """)
        logout_btn.setCursor(Qt.PointingHandCursor)
        footer.addWidget(logout_btn)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addLayout(footer)

    def refresh_stats(self):
        uid = self.user_data["id"]
        self.watched_card.update_number(db.get_watched_count(uid))
        self.watchlist_card.update_number(db.get_watchlist_count(uid))

    def to_watch(self):
        self.to_watch_page = ToWatchPage(user_id=self.user_data["id"])
        self.to_watch_page.show()

    def watched(self):
        self.watched_page = WatchedPage(user_id=self.user_data["id"])
        self.watched_page.show()

    def search_movies(self):
        self.search_page = SearchPage(user_id=self.user_data["id"])
        self.search_page.show()

    def logout(self):
        self.close()