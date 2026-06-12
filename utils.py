from pathlib import Path
import requests


def download_file(url: str, destination: Path):
    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    destination.write_bytes(
        response.content
    )
