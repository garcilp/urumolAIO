from dataclasses import dataclass, field
import requests
from config.players import PLAYER_LOOKUP
from scryfall.mtg import get_card_metadata
from utils import download_file
from graphics.image_utils import create_faded_marquee, add_marquee_text
import re
from config.paths import CACHE_DIR


@dataclass
class Card:
    quantity: int
    name: str

    image_url: str | None = None
    type_line: str | None = None


@dataclass
class Board:
    name: str
    cards: list[Card] = field(default_factory=list)

    def to_text(self) -> str:
        return "\n".join(
            f"{card.quantity} {card.name}"
            for card in self.cards
        )


def extract_deck_id(text: str) -> str | None:
    text = text.strip()
    if not text:
        return None
    match = re.search(r"moxfield\.com\/decks\/([A-Za-z0-9\-_]+)", text)
    if match:
        return match.group(1)
    return text


class Deck:
    @classmethod
    def from_moxfield(cls, deck_id):
        return cls(deck_id).load()

    def __init__(self, deck_id: str):
        self.id = deck_id
        self.player = ""
        self.player_short = ""
        self.name = ""
        self.premodern = ""
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

    @staticmethod
    def _parse_board(board_data):
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
                image_url, type_line, art_url = get_card_metadata(card.name, self.premodern)
                card.image_url = image_url
                card.type_line = type_line
                if card.name == self.marquee_card:
                    download_file(art_url, CACHE_DIR / self.id / 'marquee_card.png')
                    create_faded_marquee(
                        CACHE_DIR / self.id / 'marquee_card.png',
                        CACHE_DIR / self.id / 'marquee_card_faded.png'
                    )
                    print(CACHE_DIR / self.id / 'marquee_card.png',)
                    print(self.player_short)
                    print(self.name)
                    print(CACHE_DIR / self.id / 'cockatrice.png')
                    add_marquee_text(
                        CACHE_DIR / self.id / 'marquee_card.png',
                        self.player_short,
                        self.name,
                        CACHE_DIR / self.id / 'cockatrice.png')

    def load(self):
        response = requests.get(
            self.url,
            headers=self.headers,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()
        deck_name = data["name"]

        if " - " in deck_name:
            player, self.name = deck_name.split(" - ", maxsplit=1)
        else:
            player = ""
            self.name = deck_name

        self.player_short = player
        self.player = PLAYER_LOOKUP.get(
            player,
            player
        )

        self.mainboard.cards = self._parse_board(data["boards"]["mainboard"]["cards"])
        self.sideboard.cards = self._parse_board(data["boards"]["sideboard"]["cards"])
        self.marquee_card = data["main"]["name"]
        self.colors = data["colors"]
        self.premodern = (data["format"] == "premodern")
        self.enrich_cards()

        return self
