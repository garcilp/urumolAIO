from pathlib import Path
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton
from config.paths import ASSETS_DIR


class ManaButton(QPushButton):
    def __init__(
        self,
        color,
        parent=None
    ):
        super().__init__(parent)

        self.setStyleSheet("""
                    QPushButton {
                        border: none;
                        background: transparent;
                    }

                    QPushButton:focus {
                        border: none;
                        outline: none;
                    }

                    QPushButton:pressed {
                        background: transparent;
                    }

                    QPushButton:checked {
                        background: transparent;
                    }
                """)

        self.color = color.upper()
        icon_dir = Path(ASSETS_DIR / "mana")

        self.on_icon = QIcon(str(icon_dir / f"{self.color.lower()}_on.png"))
        self.off_icon = QIcon(str(icon_dir / f"{self.color.lower()}_off.png"))

        self.setCheckable(True)
        self.setFixedSize(24, 24)
        self.setIconSize(QSize(24, 24))
        self.setFlat(True)
        self.toggled.connect(
            self.update_icon
        )
        self.update_icon(False)

    def update_icon(
        self,
        checked
    ):
        self.setIcon(
            self.on_icon
            if checked
            else self.off_icon
        )


class MatchPointButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        icon_dir = Path(ASSETS_DIR / "wins")
        self.on_icon = QIcon(str(icon_dir / "win_on.png"))
        self.off_icon = QIcon(str(icon_dir / "win_off.png"))

        self.setCheckable(True)
        self.setFixedSize(20, 20)
        self.setIconSize(QSize(20, 20))
        self.setFlat(True)

        self.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }

            QPushButton:focus {
                border: none;
            }

            QPushButton:checked {
                background: transparent;
            }
        """)

        self.toggled.connect(self.update_icon)
        self.update_icon(False)

    def update_icon(self, checked):
        self.setIcon(
            self.on_icon
            if checked
            else self.off_icon
        )
