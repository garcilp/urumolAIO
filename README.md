# UruMOL AIO

A PySide6 desktop tool for preparing Magic: The Gathering match overlays from Moxfield decks. It retrieves deck data from Moxfield, looks up card metadata and images through Scryfall, and writes generated graphics and live score data for streaming.

## Requirements

- Python 3.10 or newer
- Internet access for Moxfield and Scryfall lookups

## Setup

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```powershell
python -m ui.main_window
```

Enter a Moxfield deck URL or deck ID in either deck field. Generated deck files are written under `cache/`; live score and player data are written under `stream/output/`. Both locations are ignored by Git.

## Project layout

- `config/` — paths, player-name mapping, and graphic coordinates
- `moxfield/` and `scryfall/` — deck and card data integrations
- `graphics/` — deck list rendering and overlay generation
- `ui/` — PySide6 interface and Qt Designer source
- `assets/` — fonts and image assets used by the interface and renderers
- `stream/` — live output location

The files in `assets/fonts/` should only be redistributed with permission under their respective font licenses.
