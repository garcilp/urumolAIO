from config.paths import LIVE_DATA_DIR


class LivePlayer:
    def __init__(self, slot):
        self.slot = slot

    @property
    def folder(self):
        return LIVE_DATA_DIR / f"player{self.slot}"

    def copy_deck(self, deck_id):
        ...

    def update_name(self, name):
        ...

    def update_deck_name(self, deck_name):
        ...

    def update_colors(self, colors):
        ...

    def update_score(self, score):
        ...
