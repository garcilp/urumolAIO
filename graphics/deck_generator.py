from moxfield.deck import Deck
from graphics.slide_maker import DeckImageGenerator
from graphics.renderers import DecklistImageGenerator
from pathlib import Path


class DeckGenerator:
    def __init__(self):
        self.image_generator = DeckImageGenerator()

    def generate(
        self,
        deck_id: str,
        image_file,
        decklist_file
    ):
        output_folder = Path("cache") / deck_id
        if output_folder.exists():
            return
        deck = Deck.from_moxfield(deck_id)
        deck.export_decklist(output_folder / decklist_file) # Hacer opcional
        generator = DecklistImageGenerator()
        visual_decklist = generator.render(deck.mainboard.cards)

        self.image_generator.create_image( # es aca
            player_name=deck.player.upper(),
            deck_name=deck.name.upper(),
            colors=deck.colors,
            output_file=output_folder / image_file,
            visual_decklist=visual_decklist
        )

        return deck

