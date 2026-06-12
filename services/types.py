import json
import time

import requests

from config.config import POKEMON_TYPES_FILE_PATH
from schemas import TypeJson
from utils.files import write_file_data


class TypeService:
    LAST_TYPE_ID = 16

    TYPE_FIELDS = [
        "id",
        "name",
        "names",
        "damage_relations",
    ]

    def __init__(self):
        self.session = requests.Session()

    def fetch(self) -> dict[str, TypeJson]:
        types = {}
        for ref in range(1, self.LAST_TYPE_ID + 1):
            raw = self.session.get(f"https://pokeapi.co/api/v2/type/{ref}", timeout=20).json()
            types[raw["name"]] = self._trim_type(raw)
            print(f"[{ref:3}] {raw['name']}")
            time.sleep(0.05)
        return types

    def update_data(self) -> None:
        types = self.fetch()
        write_file_data(POKEMON_TYPES_FILE_PATH, json.dumps(types, indent=4))
        print(f"\nDone. {len(types)} types written to {POKEMON_TYPES_FILE_PATH}.")

    def _trim_type(self, raw) -> TypeJson:
        return {field: raw[field] for field in self.TYPE_FIELDS}


if __name__ == "__main__":
    TypeService().update_data()
