from dataclasses import dataclass, field
import requests
from config.players import PLAYER_LOOKUP
from scryfall.mtg import get_card_metadata
from utils import download_file
from pathlib import Path


@dataclass
class Card:
    quantity: int
    name: str

    image_url: str | None = None
    art_url: str | None = None
    type_line: str | None = None
    colors: list[str] | None = None


@dataclass
class Board:
    name: str
    cards: list[Card] = field(default_factory=list)

    def to_text(self) -> str:
        return "\n".join(
            f"{card.quantity} {card.name}"
            for card in self.cards
        )


class Deck:
    @classmethod
    def from_moxfield(cls, deck_id):
        return cls(deck_id).load()

    def __init__(self, deck_id: str):
        self.id = deck_id
        self.player = ""
        self.name = ""
        self.marquee_card = ""
        self.colors = []
        self.mainboard = Board("main")
        self.sideboard = Board("side")

    @property
    def url(self):
        return f"https://api2.moxfield.com/v3/decks/all/{self.id}"

    @property
    def headers(self):
        return {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Referer": f"https://moxfield.com/decks/{self.id}",
            "Origin": "https://moxfield.com",
        }

    def _parse_board(self, board_data):
        return [
            Card(
                quantity=card["quantity"],
                name=card["card"]["name"]
            )
            for card in board_data.values()
        ]

    def export_decklist(self, filename):
        text = (
                self.mainboard.to_text()
                + "\n\nSIDEBOARD:\n"
                + self.sideboard.to_text()
        )

        with open(
                filename,
                "w",
                encoding="utf-8"
        ) as f:
            f.write(text)

    def enrich_cards(self):
        for board in (
                self.mainboard,
                self.sideboard
        ):
            for card in board.cards:
                metadata = get_card_metadata(
                    card.name
                )

                card.image_url = metadata[0]
                card.type_line = metadata[1]
                if card.name == self.marquee_card:
                    download_file(metadata[2], Path("cache") / self.id / 'marquee_card.png')

    def load(self):
        folder = Path("cache") / self.id
        folder.mkdir(parents=True, exist_ok=True)

        response = requests.get(
            self.url,            # URL de Moxfield del mazo
            headers=self.headers
        )

        response.raise_for_status()
        data = response.json()
        player, self.name = data["name"].split(" - ", maxsplit=1)

        self.player = PLAYER_LOOKUP.get(
            player,
            player
        )

        self.mainboard.cards = self._parse_board(data["boards"]["mainboard"]["cards"])
        self.sideboard.cards = self._parse_board(data["boards"]["sideboard"]["cards"])
        self.marquee_card = data["main"]["name"]
        self.colors = data["colors"]
        self.enrich_cards()

        return self
