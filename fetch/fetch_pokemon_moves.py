"""One-off helper: fetch all Gen-1 moves (#1-165) from PokeAPI.

Keeps only the subset of fields the game cares about (see MOVE_FIELDS),
stored raw and keyed by move name in pokemon_moves.json. The raw->domain
flattening happens on load in utils/json_parsers/moves.py, mirroring the
types pipeline.
"""

import json
import os
import time

import requests

from config.config import ASSETS_PATH, POKEMON_MOVES_FILE_PATH

FIRST_GEN_MOVE_COUNT = 165

# The fields kept verbatim from each PokeAPI move object.
MOVE_FIELDS = [
    "accuracy",
    "damage_class",
    "effect_chance",
    "effect_changes",
    "generation",
    "id",
    "meta",
    "name",
    "names",
    "past_values",
    "power",
    "pp",
    "priority",
    "stat_changes",
    "target",
    "type",
]


def trim_move(raw):
    return {field: raw[field] for field in MOVE_FIELDS}


def main():
    os.makedirs(ASSETS_PATH, exist_ok=True)
    session = requests.Session()

    moves = {}
    for ref in range(1, FIRST_GEN_MOVE_COUNT + 1):
        raw = session.get(f"https://pokeapi.co/api/v2/move/{ref}", timeout=20).json()
        moves[raw["name"]] = trim_move(raw)
        print(f"[{ref:3}] {raw['name']}")
        time.sleep(0.05)

    with open(POKEMON_MOVES_FILE_PATH, "w") as file:
        json.dump(moves, file, indent=4)

    print(f"\nDone. {len(moves)} moves written to {POKEMON_MOVES_FILE_PATH}.")


if __name__ == "__main__":
    main()
