from collections import defaultdict
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont
from config.coordinates import CIRCLE_FONT
from config.paths import FONTS_DIR
from utils import HEADERS


class CardRenderer:
    CARD_WIDTH = 192
    CARD_HEIGHT = 270

    COUNTER_SIZE = 30
    COUNTER_RADIUS = COUNTER_SIZE - 1
    COUNTER_TEXT_CENTER = COUNTER_SIZE // 2
    COUNTER_COLOR = "#1d1d1d"
    COUNTER_TEXT_COLOR = "white"
    COUNTER_BOTTOM_OFFSET = 25

    CARD_PADDING_BOTTOM = 5

    def __init__(self):
        self.font = ImageFont.truetype(
            FONTS_DIR / CIRCLE_FONT["name"],
            CIRCLE_FONT["size"]
        )

    def create_counter(self, quantity):
        circle = Image.new(
            "RGBA",
            (self.COUNTER_SIZE, self.COUNTER_SIZE),
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(circle)

        draw.ellipse(
            [0, 0, self.COUNTER_RADIUS, self.COUNTER_RADIUS],
            fill=self.COUNTER_COLOR
        )

        draw.text(
            (
                self.COUNTER_TEXT_CENTER,
                self.COUNTER_TEXT_CENTER
            ),
            str(quantity),
            anchor="mm",
            fill=self.COUNTER_TEXT_COLOR,
            font=self.font
        )

        return circle

    def render_card(
        self,
        image_url,
        quantity
    ):
        response = requests.get(image_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        card_image = Image.open(BytesIO(response.content))
        card_image = card_image.resize((self.CARD_WIDTH, self.CARD_HEIGHT), Image.Resampling.LANCZOS)

        final_image = Image.new(
            "RGBA",
            (
                self.CARD_WIDTH,
                self.CARD_HEIGHT + self.CARD_PADDING_BOTTOM
            )
        )

        final_image.paste(card_image)
        counter = self.create_counter(quantity)
        counter_x = (self.CARD_WIDTH - self.COUNTER_SIZE) // 2
        counter_y = (self.CARD_HEIGHT - self.COUNTER_BOTTOM_OFFSET)

        final_image.paste(
            counter,
            (counter_x, counter_y),
            counter
        )

        return final_image


class DecklistImageGenerator:
    CARD_SPACING = 6
    ROW_SPACING = 15
    MAX_CARDS_PER_ROW = 8

    CATEGORY_ORDER = [
        "Creature",
        "Planeswalker",
        "Sorcery",
        "Instant",
        "Enchantment",
        "Artifact",
        "Land",
        "Basic Land",
    ]

    def __init__(self):
        self.card_renderer = CardRenderer()

    def categorize_cards(self, cards):
        categories = defaultdict(list)
        for card in cards:
            categories[self.get_category(card.type_line)].append(card)
        return categories

    @classmethod
    def get_category(cls, type_line):
        for category in cls.CATEGORY_ORDER:
            if category == "Land":
                match = ("Land" in type_line and "Basic Land" not in type_line)
            else:
                match = category in type_line
            if match:
                return category
        return "Instant"

    def build_rows(self, cards):
        return [
            cards[i:i + self.MAX_CARDS_PER_ROW]
            for i in range(0, len(cards), self.MAX_CARDS_PER_ROW)
        ]

    def render_row(self, cards):
        rendered_cards = []
        card_width = self.card_renderer.CARD_WIDTH
        card_height = (self.card_renderer.CARD_HEIGHT + self.card_renderer.CARD_PADDING_BOTTOM)

        for card in cards:
            rendered_cards.append(self.card_renderer.render_card(card.image_url, card.quantity))
        row_width = (
                len(rendered_cards) * card_width
                + (len(rendered_cards) - 1) * self.CARD_SPACING
        )

        row_image = Image.new("RGBA", (row_width, card_height))

        current_x = 0

        for image in rendered_cards:
            row_image.paste(image, (current_x, 0))
            current_x += (card_width + self.CARD_SPACING)
        return row_image

    def render_decklist(self, cards):
        categorized = self.categorize_cards(cards)
        sorted_cards = []

        for category in self.CATEGORY_ORDER:
            sorted_cards.extend(categorized.get(category, []))

        rows = self.build_rows(sorted_cards)
        row_images = [self.render_row(row) for row in rows]

        if not row_images:
            return

        canvas_width = max(row.width for row in row_images)
        canvas_height = (
                sum(row.height for row in row_images)
                + (len(row_images) - 1)
                * self.ROW_SPACING
        )

        final_image = Image.new("RGBA", (canvas_width, canvas_height))
        current_y = 0
        for row in row_images:
            x = (canvas_width - row.width) // 2
            final_image.paste(row, (x, current_y))
            current_y += (row.height + self.ROW_SPACING)
        return final_image
