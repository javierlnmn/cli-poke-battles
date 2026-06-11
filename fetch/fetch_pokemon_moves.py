import json
import time

import requests

from config.config import POKEMON_MOVES_FILE_PATH
from schemas import MoveJson
from utils.files import write_file_data

FIRST_GEN_MOVE_COUNT = 165

EXCLUDED_CATEGORIES = {"force-switch", "unique"}

# The fields kept verbatim from each PokeAPI move object.
MOVE_FIELDS = [
    "accuracy",
    "damage_class",
    "generation",
    "id",
    "meta",
    "name",
    "names",
    "power",
    "pp",
    "priority",
    "stat_changes",
    "target",
    "type",
]


def trim_move(raw) -> MoveJson:
    return {field: raw[field] for field in MOVE_FIELDS}


def main():
    session = requests.Session()

    moves = {}
    for ref in range(1, FIRST_GEN_MOVE_COUNT + 1):
        raw = session.get(f"https://pokeapi.co/api/v2/move/{ref}", timeout=20).json()
        if raw["meta"]["category"]["name"] in EXCLUDED_CATEGORIES:
            print(f"[{ref:3}] skip ({raw['meta']['category']['name']}): {raw['name']}")
            continue
        moves[raw["name"]] = trim_move(raw)
        print(f"[{ref:3}] {raw['name']}")
        time.sleep(0.05)

    write_file_data(POKEMON_MOVES_FILE_PATH, json.dumps(moves, indent=4))

    print(f"\nDone. {len(moves)} moves written to {POKEMON_MOVES_FILE_PATH}.")


if __name__ == "__main__":
    main()
