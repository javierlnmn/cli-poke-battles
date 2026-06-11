import json
import os
import time

import requests

from config.config import ASSETS_PATH, POKEMON_TYPES_FILE_PATH
from schemas import TypeJson

LAST_TYPE_ID = 16

TYPE_FIELDS = [
    "id",
    "name",
    "names",
    "damage_relations",
]


def trim_type(raw) -> TypeJson:
    return {field: raw[field] for field in TYPE_FIELDS}


def main():
    os.makedirs(ASSETS_PATH, exist_ok=True)
    session = requests.Session()

    types = {}
    for ref in range(1, LAST_TYPE_ID + 1):
        raw = session.get(f"https://pokeapi.co/api/v2/type/{ref}", timeout=20).json()
        types[raw["name"]] = trim_type(raw)
        print(f"[{ref:3}] {raw['name']}")
        time.sleep(0.05)

    with open(POKEMON_TYPES_FILE_PATH, "w") as file:
        json.dump(types, file, indent=4)

    print(f"\nDone. {len(types)} types written to {POKEMON_TYPES_FILE_PATH}.")


if __name__ == "__main__":
    main()
