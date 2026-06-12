from graphics.deck_generator import DeckGenerator

deck_id = "lSwbfCUcE0KIfbnVRnn4Kw"

generator = DeckGenerator()
generator.generate(
    deck_id=deck_id,
    image_file='main.png',
    decklist_file='deck.txt'
)