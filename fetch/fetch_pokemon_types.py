import json
import time

import requests

from config.config import POKEMON_TYPES_FILE_PATH
from schemas import TypeJson
from utils.files import write_file_data

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
    session = requests.Session()

    types = {}
    for ref in range(1, LAST_TYPE_ID + 1):
        raw = session.get(f"https://pokeapi.co/api/v2/type/{ref}", timeout=20).json()
        types[raw["name"]] = trim_type(raw)
        print(f"[{ref:3}] {raw['name']}")
        time.sleep(0.05)

    write_file_data(POKEMON_TYPES_FILE_PATH, json.dumps(types, indent=4))

    print(f"\nDone. {len(types)} types written to {POKEMON_TYPES_FILE_PATH}.")


if __name__ == "__main__":
    main()
