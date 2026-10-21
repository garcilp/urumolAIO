from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from config.coordinates import MARQUEE_PLAYER, MARQUEE_DECK
from config.paths import FONTS_DIR


def add_marquee_text(
    image_path,
    player_short,
    deck_name,
    output_path,
):
    with Image.open(image_path) as source:
        image = source.convert("RGBA")

    # Darken the marquee by 25%
    brightness = ImageEnhance.Brightness(image)
    image = brightness.enhance(0.75)

    draw = ImageDraw.Draw(image)

    player_font = ImageFont.truetype(FONTS_DIR / MARQUEE_PLAYER["font"], MARQUEE_PLAYER["size"],)
    deck_font = ImageFont.truetype(FONTS_DIR / MARQUEE_DECK["font"], MARQUEE_DECK["size"],)
    player_text = player_short.upper()
    deck_text = deck_name.upper()

    # Maximum width for the deck text
    max_text_width = int(image.width * 0.80)

    # Automatically wrap the deck name
    words = deck_text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = word if not current_line else f"{current_line} {word}"

        bbox = draw.textbbox(
            (0, 0),
            test_line,
            font=deck_font,
        )

        line_width = bbox[2] - bbox[0]

        if line_width <= max_text_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    # Measure the player line
    player_bbox = draw.textbbox(
        (0, 0),
        player_text,
        font=player_font,
    )

    player_height = player_bbox[3] - player_bbox[1]

    # Measure each deck line
    deck_heights = []

    for line in lines:
        bbox = draw.textbbox(
            (0, 0),
            line,
            font=deck_font,
        )
        deck_heights.append(bbox[3] - bbox[1])

    spacing = 6
    line_spacing = 4

    deck_height = (sum(deck_heights) + line_spacing * (len(lines) - 1))
    block_height = (player_height + spacing + deck_height)
    bottom_margin = int(image.height * 0.05)
    block_top = (image.height - bottom_margin - block_height)

    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)

    # Shadow settings
    shadow_offset = 4
    shadow_blur = 4
    shadow_opacity = 210

    # Player shadow
    player_y = block_top
    shadow_draw.text(
        (
            image.width / 2 + shadow_offset,
            player_y + shadow_offset,
        ),
        player_text,
        font=player_font,
        fill=(0, 0, 0, shadow_opacity),
        anchor="mt",
    )

    # Deck shadow
    deck_y = player_y + player_height + spacing

    for line, line_height in zip(lines, deck_heights):
        shadow_draw.text(
            (
                image.width / 2 + shadow_offset,
                deck_y + shadow_offset,
            ),
            line,
            font=deck_font,
            fill=(0, 0, 0, shadow_opacity),
            anchor="mt",
        )

        deck_y += line_height + line_spacing

    # Blur the shadow to make it soft
    shadow = shadow.filter(
        ImageFilter.GaussianBlur(shadow_blur)
    )

    # Composite shadow behind the text
    image = Image.alpha_composite(image, shadow)

    # Recreate drawing context after compositing
    draw = ImageDraw.Draw(image)

    # ---------------------------------------------------------
    # Draw actual text
    # ---------------------------------------------------------

    # Player name
    player_y = block_top

    draw.text(
        (image.width / 2, player_y),
        player_text,
        font=player_font,
        fill=MARQUEE_PLAYER["color"],
        anchor="mt",
    )

    # Deck name
    deck_y = player_y + player_height + spacing

    for line, line_height in zip(lines, deck_heights):
        draw.text(
            (image.width / 2, deck_y),
            line,
            font=deck_font,
            fill=MARQUEE_DECK["color"],
            anchor="mt",
        )

        deck_y += line_height + line_spacing

    image.save(output_path)


def create_faded_marquee(
    input_file,
    output_file,
    fade_start=-0.2
):
    image = Image.open(input_file).convert("RGBA")
    width, height = image.size
    mask = Image.new("L", (width, 1))
    start = int(width * fade_start)
    for x in range(width):
        fade_end = 0.5
        progress = min(x / (width * fade_end), 1.0)
        smooth = progress * progress * (3 - 2 * progress)
        alpha = int(255 * smooth)
        mask.putpixel((x, 0), alpha)
    mask = mask.resize((width, height))
    image.putalpha(mask)
    image.save(output_file)
