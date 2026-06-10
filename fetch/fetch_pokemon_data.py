import io
import json
import os
import time

import requests
from PIL import Image

from config.config import POKEMON_ASCII_ART_PATH, POKEMON_DATA_FILE_PATH

FIRST_GEN_POKEMON_COUNT = 151

WIDTH = 70
HEIGHT = 35
RAMP = " .:-=+*#%@"
ALPHA_THRESHOLD = 96

POKEMON_FIELDS = [
    "id",
    "name",
    "height",
    "weight",
    "base_experience",
    "stats",
    "types",
    "abilities",
]

GEN1_VERSION_GROUPS = {"red-blue", "yellow"}

COLOR_MAP = {
    "black": "white",
    "blue": "blue",
    "brown": "yellow",
    "gray": "white",
    "green": "green",
    "pink": "magenta",
    "purple": "magenta",
    "red": "red",
    "white": "white",
    "yellow": "yellow",
}


def to_ascii(img):
    img = img.convert("RGBA").resize((WIDTH, HEIGHT), Image.LANCZOS)
    px = img.load()
    lines = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            r, g, b, a = px[x, y]
            if a < ALPHA_THRESHOLD:
                row.append(" ")
                continue
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            idx = int((1 - lum / 255) * (len(RAMP) - 1))
            row.append(RAMP[idx])
        lines.append("".join(row).rstrip().ljust(WIDTH))
    return "\n".join(lines) + "\n"


def sprite_url(raw):
    return raw["sprites"]["other"]["official-artwork"]["front_default"] or raw["sprites"]["front_default"]


def save_ascii(session, raw, name):
    url = sprite_url(raw)
    if not url:
        return
    img = Image.open(io.BytesIO(session.get(url, timeout=20).content))
    with open(os.path.join(POKEMON_ASCII_ART_PATH, name), "w") as file:
        file.write(to_ascii(img))


def species_color(session, raw):
    species = session.get(raw["species"]["url"], timeout=20).json()
    return COLOR_MAP.get(species["color"]["name"], "white")


def gen1_move(entry):
    by_version_group = {}
    for detail in entry["version_group_details"]:
        version_group = detail["version_group"]["name"]
        if version_group in GEN1_VERSION_GROUPS:
            by_version_group.setdefault(version_group, []).append(
                {
                    "move_learn_method": detail["move_learn_method"]["name"],
                    "level_learned_at": detail["level_learned_at"],
                }
            )

    learn_details = by_version_group.get("red-blue") or by_version_group.get("yellow")
    if not learn_details:
        return None

    return {"name": entry["move"]["name"], "learn_details": learn_details}


def trim_pokemon(session, raw):
    data = {field: raw[field] for field in POKEMON_FIELDS}
    data["moves"] = [move for move in (gen1_move(entry) for entry in raw["moves"]) if move]
    data["color"] = species_color(session, raw)
    return data


def main():
    os.makedirs(POKEMON_ASCII_ART_PATH, exist_ok=True)
    session = requests.Session()

    pokemons = {}
    for dex in range(1, FIRST_GEN_POKEMON_COUNT + 1):
        raw = session.get(f"https://pokeapi.co/api/v2/pokemon/{dex}", timeout=20).json()
        name = raw["name"].replace("-", "_")
        save_ascii(session, raw, name)
        pokemons[name] = trim_pokemon(session, raw)
        print(f"[{dex:3}] {name}")
        time.sleep(0.05)

    with open(POKEMON_DATA_FILE_PATH, "w") as file:
        json.dump(pokemons, file, indent=4)

    print(f"\nDone. {len(pokemons)} pokemons written to {POKEMON_DATA_FILE_PATH}.")


if __name__ == "__main__":
    main()
