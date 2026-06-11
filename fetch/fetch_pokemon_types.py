import json
import os
import time

import requests

from config.config import ASSETS_PATH, POKEMON_TYPES_FILE_PATH
from schemas import TypeJson

TYPES_AMOUNT = 19
EXCLUDE_TYPE_NAMES = {"dark", "fairy", "stellar", "unknown"}

TYPE_FIELDS = [
    "id",
    "name",
    "names",
    "damage_relations",
]


def trim_type(raw) -> TypeJson:
    for _, damage_relations_list in raw["damage_relations"].items():
        for index, relation_type in enumerate(damage_relations_list):
            if relation_type["name"] in EXCLUDE_TYPE_NAMES:
                damage_relations_list.pop(index)

    data = {field: raw[field] for field in TYPE_FIELDS}
    return data


def main():
    os.makedirs(ASSETS_PATH, exist_ok=True)
    session = requests.Session()

    types = {}
    for ref in range(1, TYPES_AMOUNT + 1):
        raw = session.get(f"https://pokeapi.co/api/v2/type/{ref}", timeout=20).json()
        type_name_key = raw["name"]

        if type_name_key in EXCLUDE_TYPE_NAMES:
            continue

        types[type_name_key] = trim_type(raw)
        print(f"[{ref:3}] {raw['name']}")
        time.sleep(0.05)

    with open(POKEMON_TYPES_FILE_PATH, "w") as file:
        json.dump(types, file, indent=4)

    print(f"\nDone. {len(types)} types written to {POKEMON_TYPES_FILE_PATH}.")


if __name__ == "__main__":
    main()
