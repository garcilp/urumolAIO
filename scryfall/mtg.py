import requests
from time import sleep


SCRYFALL_URL = "https://api.scryfall.com/cards/search"
HEADERS = {"User-Agent": "UrumolAIO Scryfall Interface/1.0 (Joaquin Garcia)"}
CARD_CACHE = {}


def get_card_metadata(
    card_name: str,
    premodern: bool = False
):
    card_name = '!"' + card_name + '"'

    if premodern:
        card_name += " year<=2003 frame:old"

    sleep(0.5)
    response = requests.get(
        SCRYFALL_URL,
        params={"q": card_name},
        headers=HEADERS
    )

    response.raise_for_status()

    card = response.json()["data"][0]

    if "image_uris" in card:
        return (
            card["image_uris"]["png"],
            card["type_line"],
            card["image_uris"]["art_crop"]
        )

    return (
        card["card_faces"][0]["image_uris"]["png"],
        card["card_faces"][0]["type_line"],
        card["card_faces"][0]["image_uris"]["art_crop"]
    )