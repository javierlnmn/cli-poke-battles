import io
import json
import time
from pathlib import Path

import requests
from PIL import Image

from config.config import POKEMON_ASCII_ART_PATH, POKEMON_DATA_FILE_PATH
from repositories import MoveRepository, PokemonRepository
from schemas import MoveLearnDetailJson, PokemonJson, PokemonMoveJson
from utils.files import write_file_data


class PokemonService:
    FIRST_GEN_POKEMON_COUNT = 151

    WIDTH = 53
    HEIGHT = 26
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
        PokemonRepository.clear_cache()

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

    @staticmethod
    def _move_catalog() -> dict:
        try:
            return MoveRepository.load_moves_data()
        except FileNotFoundError:
            return {}

    @staticmethod
    def _type_catalog() -> set[str]:
        try:
            from repositories import TypeRepository
            return set(TypeRepository.load_types_data().keys())
        except FileNotFoundError:
            return set()

    def _resolve_types(self, raw_types: list, name: str) -> list:
        type_catalog = self._type_catalog()
        if not type_catalog:
            return raw_types

        resolved = []
        for slot in raw_types:
            type_name = slot["type"]["name"]
            if type_name in type_catalog:
                resolved.append(slot)
            else:
                if len(raw_types) == 1:
                    print(f"\n  '{name}' has unknown type '{type_name}' (only type).")
                    print(f"  Known types: {', '.join(sorted(type_catalog))}")
                    replacement = input("  Replace with (leave blank to skip): ").strip().lower()
                    if replacement and replacement in type_catalog:
                        new_slot = {"slot": slot["slot"], "type": {"name": replacement, "url": ""}}
                        resolved.append(new_slot)
                else:
                    print(f"  '{name}': dropping unknown type '{type_name}' (has other types).")

        return resolved

    def _trim_pokemon(self, raw) -> PokemonJson:
        data = {field: raw[field] for field in self.POKEMON_FIELDS}

        data["types"] = self._resolve_types(raw["types"], raw["name"])

        move_catalog = self._move_catalog()
        data["moves"] = [
            move
            for move in (self._gen1_move(entry) for entry in raw["moves"])
            if move and (not move_catalog or move["name"] in move_catalog)
        ]

        data["color"] = self._species_color(raw)
        return data


if __name__ == "__main__":
    PokemonService().update_data()
