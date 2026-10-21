import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow)
from ui.ui_mainwindow import Ui_MainWindow
from graphics.widgets import ManaButton, MatchPointButton
import qt_themes
from moxfield.moxfield import extract_deck_id
from graphics.deck_generator import DeckGenerator
from config.paths import LIVE_DATA_DIR, CACHE_DIR
import shutil


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        qt_themes.set_theme('nord')
        self.loading_data = False

        self.ui.deckId1.returnPressed.connect(lambda: self.load_deck(1))
        self.ui.deckId2.returnPressed.connect(lambda: self.load_deck(2))

        self.create_marquees()
        self.marquee_paths = {
            1: None,
            2: None
        }
        self.marquee_labels = {
            1: self.marquee1,
            2: self.marquee2
        }

        self.player1_mana = {}
        self.player2_mana = {}

        self.player_name_fields = {
            1: self.ui.playerName1,
            2: self.ui.playerName2
        }

        self.deck_name_fields = {
            1: self.ui.deckName1,
            2: self.ui.deckName2
        }

        self.scores = {
            1: 0,
            2: 0
        }

        self.ui.bo3Button.clicked.connect(lambda: self.set_best_of(3))
        self.ui.bo5Button.clicked.connect(lambda: self.set_best_of(5))
        self.ui.swapButton.clicked.connect(self.swap_players)

        self.ui.playerName1.textChanged.connect(lambda: self.update_live_player_state(1, "name"))
        self.ui.playerName2.textChanged.connect(lambda: self.update_live_player_state(2, "name"))
        self.ui.deckName1.textChanged.connect(lambda: self.update_live_player_state(1, "deck"))
        self.ui.deckName2.textChanged.connect(lambda: self.update_live_player_state(2, "deck"))

        for color in "WUBRGC":
            p1_button = ManaButton(color)
            p2_button = ManaButton(color)
            self.ui.player1ManaLayout.addWidget(p1_button)
            self.ui.player2ManaLayout.addWidget(p2_button)
            self.player1_mana[color] = p1_button
            self.player2_mana[color] = p2_button

        self.player1_points = (self.create_match_points(self.ui.player1WinsLayout))
        self.player2_points = (self.create_match_points(self.ui.player2WinsLayout))
        self.set_best_of(3)
        self.setup_score_buttons(self.player1_points, 1)
        self.setup_score_buttons(self.player2_points, 2)

        self.load_player_data(1)
        self.load_player_data(2)

    def refresh_scores(self):
        self.set_score(self.player1_points, self.scores[1])
        self.set_score(self.player2_points, self.scores[2])
        (LIVE_DATA_DIR / "player1_score.txt").write_text(str(self.scores[1]))
        (LIVE_DATA_DIR / "player2_score.txt").write_text(str(self.scores[2]))

    # ============
    # WINS BUTTONS
    # ============
    def set_best_of(self, best_of):
        self.best_of = best_of
        max_wins = 2 if best_of == 3 else 3
        for i in range(3):
            visible = i < max_wins
            self.player1_points[i].setVisible(visible)
            self.player2_points[i].setVisible(visible)
        self.scores[1] = min(self.scores[1], max_wins)
        self.scores[2] = min(self.scores[2], max_wins)
        self.refresh_scores()

    def create_match_points(self, layout):
        buttons = []
        for _ in range(3):
            button = MatchPointButton()
            layout.addWidget(button)
            buttons.append(button)
        return buttons

    def setup_score_buttons(self, buttons, player):
        for index, button in enumerate(buttons):
            button.clicked.connect(
                lambda checked,
                       i=index,
                       p=player:
                self.toggle_score(p, i + 1)
            )

    def set_score(self, buttons, wins):
        for i, button in enumerate(buttons):
            button.setChecked(i < wins)

    def toggle_score(self, player, clicked_score):
        current = self.scores[player]

        buttons = {
            1: self.player1_points,
            2: self.player2_points
        }[player]

        if clicked_score == current:
            current = 0
        else:
            current = clicked_score

        self.scores[player] = current
        self.set_score(buttons, current)
        (LIVE_DATA_DIR / f"player{player}_score.txt").write_text(str(self.scores[player]))

    # ===========
    # DECK LOADER
    # ===========
    def load_deck(self, player):
        field = {
            1: self.ui.deckId1,
            2: self.ui.deckId2
        }[player]

        text = field.text().strip()
        if not text:
            return
        deck_id = extract_deck_id(text)
        field.setText(deck_id)
        if not deck_id:
            return
        try:
            generator = DeckGenerator()
            generator.generate(
                deck_id=deck_id,
                image_file="mainboard.png",
                decklist_file="decklist.txt"
            )

        except Exception as e:
            print(f"Failed to load deck: {e}")
            return
        self.on_deck_loaded(player, deck_id)

    def on_deck_loaded(self, player, deck_id):
        self.copy_deck_assets_to_stream(player, deck_id)
        self.load_player_data(player)

    # ===============
    # STREAM HANDLING
    # ===============
    def copy_deck_assets_to_stream(self, player, deck_id):
        source = CACHE_DIR / deck_id
        destination = (LIVE_DATA_DIR / f"player{player}")
        destination.mkdir(parents=True, exist_ok=True)
        for file in source.iterdir():
            if file.is_file():
                shutil.copy2(file, destination / file.name)

    def load_player_data(self, player):
        self.loading_data = True
        try:
            folder = (LIVE_DATA_DIR / f"player{player}")
            if not folder.exists():
                return
            player_file = folder / "player_name.txt"
            deck_file = folder / "deck_name.txt"
            colors_file = folder / "colors.txt"
            marquee_file = (folder / "marquee_card_faded.png")

            if player_file.exists():
                self.player_name_fields[player].setText(player_file.read_text().strip())
            if deck_file.exists():
                self.deck_name_fields[player].setText(deck_file.read_text().strip())
            if colors_file.exists():
                colors = (colors_file.read_text().strip().split(","))
                buttons = {
                    1: self.player1_mana,
                    2: self.player2_mana
                }[player]

                for button in buttons.values():
                    button.setChecked(False)

                for color in colors:
                    if color in buttons:
                        buttons[color].setChecked(True)

            if marquee_file.exists():
                self.marquee_paths[player] = str(marquee_file)
                self.set_marquee_image(self.marquee_labels[player], self.marquee_paths[player])
        finally:
            self.loading_data = False
        self.loading_data = False

    def update_live_player_state(self, player, field):
        if self.loading_data:
            return
        folder = (LIVE_DATA_DIR / f"player{player}")
        folder.mkdir(parents=True, exist_ok=True)
        if field == "name":
            (folder / "player_name.txt").write_text(self.player_name_fields[player].text())
        elif field == "deck":
            (folder / "deck_name.txt").write_text(self.deck_name_fields[player].text())

    def swap_scores(self):
        self.scores[1], self.scores[2] = (self.scores[2], self.scores[1])
        self.refresh_scores()

    def swap_players(self):
        player1 = LIVE_DATA_DIR / "player1"
        player2 = LIVE_DATA_DIR / "player2"
        temp = LIVE_DATA_DIR / "_temp"

        if temp.exists():
            shutil.rmtree(temp)

        if player1.exists():
            player1.rename(temp)

        if player2.exists():
            player2.rename(player1)

        if temp.exists():
            temp.rename(player2)

        self.swap_scores()
        self.load_player_data(1)
        self.load_player_data(2)

    # ===========
    # DECK IMAGES
    # ===========
    def create_marquees(self):
        self.marquee1 = QLabel(self.ui.centralwidget)
        self.marquee2 = QLabel(self.ui.centralwidget)
        self.marquee1.setStyleSheet("background: transparent;")
        self.marquee2.setStyleSheet("background: transparent;")
        self.marquee1.lower()
        self.marquee2.lower()
        self.position_marquees()

    def position_marquees(self):
        width = self.ui.centralwidget.width()
        height = self.ui.centralwidget.height()

        half_height = height // 2
        marquee_width = width * 0.4

        self.marquee1.setGeometry(
            width - marquee_width,
            0,
            marquee_width,
            half_height
        )

        self.marquee2.setGeometry(
            width - marquee_width,
            half_height,
            marquee_width,
            half_height
        )

    def set_marquee_image(self, label, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return
        pixmap = pixmap.scaled(
            label.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        label.setPixmap(pixmap)
        label.setAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.position_marquees()
        for player, label in {
            1: self.marquee1,
            2: self.marquee2
        }.items():
            path = self.marquee_paths[player]
            if path:
                self.set_marquee_image(label, path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
