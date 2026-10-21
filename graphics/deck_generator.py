from moxfield.moxfield import Deck
from graphics.slide_maker import DeckImageGenerator
from graphics.renderers import DecklistImageGenerator
from config.paths import CACHE_DIR
from shutil import rmtree


class DeckGenerator:
    def __init__(self):
        self.image_generator = DeckImageGenerator()
        self.decklist_renderer = DecklistImageGenerator()

    def generate(
        self,
        deck_id: str,
        image_file: str,
        decklist_file: str
    ):
        output_folder = CACHE_DIR / deck_id
        complete_marker = output_folder / 'mainboard.png'

        if complete_marker.exists():
            return

        if output_folder.exists():
            rmtree(output_folder)

        output_folder.mkdir(parents=True, exist_ok=True)
        deck = Deck.from_moxfield(deck_id)

        deck.export_decklist(output_folder / decklist_file)
        (output_folder / "player_name.txt").write_text(deck.player)
        (output_folder / "player_short.txt").write_text(deck.player_short)
        (output_folder / "deck_name.txt").write_text(deck.name)
        (output_folder / "colors.txt").write_text(",".join(deck.colors))
        visual_decklist = self.decklist_renderer.render_decklist(deck.mainboard.cards)
        self.image_generator.create_image(
            player_name=deck.player.upper(),
            deck_name=deck.name.upper(),
            colors=deck.colors,
            output_file=output_folder / image_file,
            visual_decklist=visual_decklist
        )

        if deck.sideboard and deck.sideboard.cards:
            visual_sideboard = self.decklist_renderer.render_decklist(deck.sideboard.cards)
            is_two_rows = len(deck.sideboard.cards) > 8
            self.image_generator.create_sideboard_image(visual_sideboard, is_two_rows, output_folder / "sideboard.png")

        return deck
