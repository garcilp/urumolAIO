import requests
from time import sleep
from utils import HEADERS


SCRYFALL_URL = "https://api.scryfall.com/cards/search"
CARD_CACHE = {}


def get_card_metadata(
        card_name: str,
        premodern: bool = False
) -> tuple[str, str, str]:

    cache_key = (card_name, premodern)

    if cache_key in CARD_CACHE:
        return CARD_CACHE[cache_key]

    query = f'!"{card_name}"'

    if premodern:
        query += " year<=2003 frame:old"

    sleep(0.5)

    response = requests.get(
        SCRYFALL_URL,
        params={"q": query},
        headers=HEADERS,
        timeout=10
    )

    response.raise_for_status()
    card = response.json()["data"][0]

    card_data = (card if "image_uris" in card else card["card_faces"][0])
    result = (card_data["image_uris"]["png"], card_data["type_line"], card_data["image_uris"]["art_crop"])

    CARD_CACHE[cache_key] = result

    return result
