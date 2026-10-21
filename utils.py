from pathlib import Path
import requests

HEADERS = {"User-Agent": "UrumolAIO Scryfall Interface/1.0 (Joaquin Garcia)"}


def download_file(url: str, destination: Path):
    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    response.raise_for_status()

    destination.write_bytes(response.content)
