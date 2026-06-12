import io
import json
import time
from pathlib import Path

import requests
from PIL import Image

from config.config import POKEMON_ASCII_ART_PATH, POKEMON_DATA_FILE_PATH, POKEMON_MOVES_FILE_PATH
from schemas import MoveLearnDetailJson, PokemonJson, PokemonMoveJson
from utils.files import read_file_data_json, write_file_data


class PokemonService:
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

    def __init__(self):
        self.session = requests.Session()
        self.move_catalog = self._load_move_catalog()

    @staticmethod
    def _load_move_catalog() -> dict:
        try:
            return read_file_data_json(POKEMON_MOVES_FILE_PATH)
        except FileNotFoundError:
            return {}

    def fetch(self) -> tuple[dict[str, PokemonJson], dict[str, str]]:
        pokemons = {}
        ascii_arts = {}
        for dex in range(1, self.FIRST_GEN_POKEMON_COUNT + 1):
            raw = self.session.get(f"https://pokeapi.co/api/v2/pokemon/{dex}", timeout=20).json()
            name = raw["name"].replace("-", "_")
            ascii_art = self._build_ascii(raw)
            if ascii_art is not None:
                ascii_arts[name] = ascii_art
            pokemons[name] = self._trim_pokemon(raw)
            print(f"[{dex:3}] {name}")
            time.sleep(0.05)
        return pokemons, ascii_arts

    def update_data(self) -> None:
        pokemons, ascii_arts = self.fetch()

        for name, ascii_art in ascii_arts.items():
            write_file_data(Path(POKEMON_ASCII_ART_PATH) / name, ascii_art)

        write_file_data(POKEMON_DATA_FILE_PATH, json.dumps(pokemons, indent=4))
        print(f"\nDone. {len(pokemons)} pokemons written to {POKEMON_DATA_FILE_PATH}.")

    @staticmethod
    def get_pokemon_list() -> list[str]:
        return list(read_file_data_json(POKEMON_DATA_FILE_PATH).keys())

    def _build_ascii(self, raw) -> str | None:
        url = self._sprite_url(raw)
        if not url:
            return None
        img = Image.open(io.BytesIO(self.session.get(url, timeout=20).content))
        return self._to_ascii(img)

    def _to_ascii(self, img) -> str:
        img = img.convert("RGBA").resize((self.WIDTH, self.HEIGHT), Image.LANCZOS)
        px = img.load()
        lines = []
        for y in range(self.HEIGHT):
            row = []
            for x in range(self.WIDTH):
                r, g, b, a = px[x, y]
                if a < self.ALPHA_THRESHOLD:
                    row.append(" ")
                    continue
                lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
                idx = int((1 - lum / 255) * (len(self.RAMP) - 1))
                row.append(self.RAMP[idx])
            lines.append("".join(row).rstrip().ljust(self.WIDTH))
        return "\n".join(lines) + "\n"

    @staticmethod
    def _sprite_url(raw) -> str:
        return raw["sprites"]["other"]["official-artwork"]["front_default"] or raw["sprites"]["front_default"]

    def _species_color(self, raw) -> str:
        species = self.session.get(raw["species"]["url"], timeout=20).json()
        return self.COLOR_MAP.get(species["color"]["name"], "white")

    def _gen1_move(self, entry) -> PokemonMoveJson | None:
        by_version_group: dict[str, list[MoveLearnDetailJson]] = {}
        for detail in entry["version_group_details"]:
            version_group = detail["version_group"]["name"]
            if version_group in self.GEN1_VERSION_GROUPS:
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

    def _trim_pokemon(self, raw) -> PokemonJson:
        data = {field: raw[field] for field in self.POKEMON_FIELDS}

        data["moves"] = [
            move
            for move in (self._gen1_move(entry) for entry in raw["moves"])
            if move and (not self.move_catalog or move["name"] in self.move_catalog)
        ]

        data["color"] = self._species_color(raw)
        return data


if __name__ == "__main__":
    PokemonService().update_data()
