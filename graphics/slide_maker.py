from PIL import Image, ImageDraw, ImageFont
from config.coordinates import PLAYER_NAME, FONTS_DIR, DECK_NAME
from pathlib import Path


def center_paste(
        canvas,
        image,
        center
):
    x = center[0] - image.width // 2
    y = center[1] - image.height // 2

    canvas.paste(
        image,
        (x, y),
        image
    )


class DeckImageGenerator:
    CANVAS_SIZE = (1920, 1080)

    MANA_SYMBOLS = {
        "W": ((97, 139), "#f1f4d8", "#242420"),
        "U": ((146, 139), "#66c1f2", "#0f1d24"),
        "B": ((195, 139), "#827f82", "#131313"),
        "R": ((244, 139), "#f95451", "#250d0c"),
        "G": ((293, 139), "#26b46b", "#061b10"),
        "C": ((342, 139), "#b9b9b9", "#1c1c1c"),
    }

    def __init__(self):
        self.player_name_font = ImageFont.truetype(
            FONTS_DIR / PLAYER_NAME["font"],
            PLAYER_NAME["size"]
        )

        self.deck_name_font = ImageFont.truetype(
            FONTS_DIR / DECK_NAME["font"],
            DECK_NAME["size"]
        )

        self.mana_font = ImageFont.truetype(
            FONTS_DIR / "MAGICSYMBOLS2020.otf",
            58
        )

    def draw_text(
        self,
        canvas,
        text,
        position,
        font,
        color
    ):
        canvas.text(
            position,
            text,
            font=font,
            fill=color
        )

    def draw_mana_symbols(
        self,
        canvas,
        active_colors
    ):
        active_colors = {
            color.upper()
            for color in active_colors
        }

        for symbol, (position, active, inactive) in self.MANA_SYMBOLS.items():
            canvas.text(
                position,
                "o",
                font=self.mana_font,
                fill=active if symbol in active_colors else inactive
            )

            canvas.text(
                position,
                symbol,
                font=self.mana_font,
                fill="#000000"
            )

    def create_image(
        self,
        player_name,
        deck_name,
        colors,
        output_file,
        visual_decklist
    ):
        img = Image.new(
            "RGBA",
            self.CANVAS_SIZE,
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(img)

        self.draw_text(
            draw,
            player_name,
            PLAYER_NAME["position"],
            self.player_name_font,
            PLAYER_NAME["color"]
        )

        self.draw_text(
            draw,
            deck_name,
            DECK_NAME["position"],
            self.deck_name_font,
            DECK_NAME["color"]
        )

        self.draw_mana_symbols(
            draw,
            colors
        )

        center_paste(
            img,
            visual_decklist,
            (960, 640))

        img.save(output_file)
