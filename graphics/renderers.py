from collections import defaultdict
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont
from config.coordinates import FONTS_DIR, CIRCLE_FONT


class CardRenderer:
    CARD_WIDTH = 192
    CARD_HEIGHT = 270

    def __init__(self):
        self.font = ImageFont.truetype(
            FONTS_DIR / CIRCLE_FONT["name"],
            CIRCLE_FONT["size"]
        )

    def create_counter(self, quantity):
        circle = Image.new(
            "RGBA",
            (30, 30),
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(circle)

        draw.ellipse(
            [0, 0, 29, 29],
            fill="#1d1d1d"
        )

        draw.text(
            (15, 15),
            str(quantity),
            anchor="mm" ,
            fill="white",
            font=self.font
        )

        return circle

    def render_card(
        self,
        image_url,
        quantity
    ):
        response = requests.get(image_url)

        card_image = Image.open(BytesIO(response.content))

        card_image = card_image.resize(
            (
                self.CARD_WIDTH,
                self.CARD_HEIGHT
            )
        )

        final_image = Image.new(
            "RGBA",
            (self.CARD_WIDTH, self.CARD_HEIGHT + 5)
        )

        final_image.paste(card_image)

        counter = self.create_counter(quantity)

        final_image.paste(
            counter,
            (
                (self.CARD_WIDTH - 30) // 2,
                self.CARD_HEIGHT - 25
            ),
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
            categories[
                self.get_category(
                    card.type_line
                )
            ].append(card)

        return categories

    @staticmethod
    def get_category(type_line):

        if "Basic Land" in type_line:
            return "Basic Land"

        if "Land" in type_line:
            return "Land"

        if "Creature" in type_line:
            return "Creature"

        if "Planeswalker" in type_line:
            return "Planeswalker"

        if "Enchantment" in type_line:
            return "Enchantment"

        if "Artifact" in type_line:
            return "Artifact"

        if "Sorcery" in type_line:
            return "Sorcery"

        return "Instant"

    def build_rows(
        self,
        cards
    ):
        return [
            cards[i:i + self.MAX_CARDS_PER_ROW]
            for i in range(
                0,
                len(cards),
                self.MAX_CARDS_PER_ROW
            )
        ]

    def render_row(
        self,
        cards
    ):
        rendered_cards = []

        for card in cards:
            rendered_cards.append(
                self.card_renderer.render_card(
                    card.image_url,
                    card.quantity
                )
            )

        row_width = (
            len(rendered_cards)
            * 192
            + (len(rendered_cards) - 1)
            * self.CARD_SPACING
        )

        row_image = Image.new(
            "RGBA",
            (
                row_width,
                275
            )
        )

        current_x = 0

        for image in rendered_cards:

            row_image.paste(
                image,
                (current_x, 0)
            )

            current_x += (
                192
                + self.CARD_SPACING
            )

        return row_image

    def render(
        self,
        cards
    ):
        categorized = self.categorize_cards(
            cards
        )

        sorted_cards = []

        for category in self.CATEGORY_ORDER:
            sorted_cards.extend(categorized.get(category, []))

        rows = self.build_rows(sorted_cards)

        row_images = [
            self.render_row(row)
            for row in rows
        ]

        if not row_images:
            return

        canvas_width = max(
            row.width
            for row in row_images
        )

        canvas_height = (
            sum(
                row.height
                for row in row_images
            )
            + (
                len(row_images) - 1
            )
            * self.ROW_SPACING
        )

        final_image = Image.new(
            "RGBA",
            (
                canvas_width,
                canvas_height
            )
        )

        current_y = 0

        for row in row_images:

            x = (
                canvas_width
                - row.width
            ) // 2

            final_image.paste(
                row,
                (x, current_y)
            )

            current_y += (
                row.height
                + self.ROW_SPACING
            )

        return final_image

